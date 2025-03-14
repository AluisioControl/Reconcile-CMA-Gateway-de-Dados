from typing import Dict

import pandas as pd

from app.logger import logger
from app.reconcile2.core.data_synchronizer import BaseDataSynchronizer
from app.reconcile2.core.db_connection import DatabaseConnection
from app.scadalts import (
    import_datapoint_modbus,
    import_datasource_modbus,
)
from app.reconcile2.scadalts.mutations import (
    DATAPOINT_MODBUS_FIELDS,
    DATASOURCE_MODBUS_FIELDS,
    # import_datapoint_modbus,
    # import_datasource_modbus,
    # send_data_to_scada,
    send_to_scada,
)


class DpModbusDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados Modbus"""

    def __init__(self):
        super().__init__(table_name="DP_MODBUS_IP", primary_key="xid_sensor")

    def _apply_changes(
        self, changes: Dict[str, any], df: pd.DataFrame, db: DatabaseConnection
    ):
        """Aplica as alterações no banco de dados"""
        print("DpModbusDataSynchronizer... Applying changes")
        if changes["remove"]:  # se houver registros a remover
            records = self._get_record_by_ids(changes["remove"], db)
            # disable records
            records = records.copy()  # evitar problemas de referência
            records["enabled"] = False
            self._sync_datapoint_scada(df=records)
            self._remove_records(changes["remove"], db)
            logger.info(f"Removidos {len(changes['remove'])} registros.")
        else:
            logger.info("Nenhum dispositivo foi remover.")

        if not changes["update"].empty:  # se houver registros a atualizar
            for _, row in changes["update"].iterrows():
                update_query = f"""
                    UPDATE {self.table_name} SET
                        xid_equip = ?, range = ?, modbusDataType = ?, additive = ?,
                        offset = ?, bit = ?, multiplier = ?, slaveId = ?, enabled = ?,
                        nome = ?, tipo = ?, classificacao = ?
                    WHERE xid_sensor = ?
                """
                values = (
                    str(row["xid_equip"]),
                    str(row["range"]),
                    str(row["modbusDataType"]),
                    int(row["additive"]) if pd.notnull(row["additive"]) else None,
                    int(row["offset"]) if pd.notnull(row["offset"]) else None,
                    int(row["bit"]) if pd.notnull(row["bit"]) else None,
                    float(row["multiplier"]) if pd.notnull(row["multiplier"]) else None,
                    int(row["slaveId"]) if pd.notnull(row["slaveId"]) else None,
                    bool(row["enabled"]),
                    str(row["nome"]),
                    str(row["tipo"]),
                    str(row["classificacao"]),
                    str(row["xid_sensor"]),
                )
                db.execute(update_query, values)
            logger.info(f"Atualizados {len(changes['update'])} registros.")
            # send data to update in scada
            self._sync_datapoint_scada(df=changes["update"])
        else:
            logger.info("Nenhum dispositivo foi atualizado.")

        if not changes["new"].empty:  # se houver registros a inserir
            changes["new"].to_sql(
                self.table_name, db.connection, if_exists="append", index=False
            )
            logger.info(f"Inseridos {len(changes['new'])} novos registros.")
            # send data to insert in scada
            self._sync_datapoint_scada(df=changes["new"])
        else:
            logger.info("Nenhum novo dispositivo foi inserido.")

    def _sync_datapoint_scada(self, df: pd.DataFrame):
        """Sincroniza os dados com o ScadaLTS"""
        print("DpModbusDataSynchronizer... Syncing with ScadaLTS")
        df = df[DATAPOINT_MODBUS_FIELDS]
        send_to_scada(df=df, import_function=import_datapoint_modbus)
        logger.info(f"Enviados {len(df)} registros para o ScadaLTS, usando {import_datapoint_modbus} como função de importação.")