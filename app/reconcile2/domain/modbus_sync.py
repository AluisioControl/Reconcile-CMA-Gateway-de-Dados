from typing import Dict
from app.logger import logger
import pandas as pd

from app.reconcile2.core.data_synchronizer import BaseDataSynchronizer
from app.reconcile2.core.db_connection import DatabaseConnection


class DpModbusDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados Modbus"""

    def __init__(self):
        super().__init__(table_name="DP_MODBUS_IP", primary_key="xid_sensor")

    def _apply_changes(
        self, changes: Dict[str, any], df: pd.DataFrame, db: DatabaseConnection
    ):
        """ Aplica as alterações no banco de dados """

        if changes["remove"]: # se houver registros a remover
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} IN (\"{'","'.join(map(str, changes['remove']))}\")"
            db.execute(query)
            logger.info(f"\n\tRemovidos {len(changes['remove'])} registros.")

        if not changes["update"].empty: # se houver registros a atualizar
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
            logger.info(f"\n\tAtualizados {len(changes['update'])} registros.")

        if not changes["new"].empty: # se houver registros a inserir
            changes["new"].to_sql(
                self.table_name, db.connection, if_exists="append", index=False
            )
            logger.info(f"\n\tInseridos {len(changes['new'])} novos registros.")
