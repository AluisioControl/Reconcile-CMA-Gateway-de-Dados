from typing import Dict, Any

import pandas as pd

from app.logger import logger
from app.reconcile2.core.data_synchronizer import BaseDataSynchronizer
from app.reconcile2.core.db_connection import DatabaseConnection
from app.reconcile2.scadalts.mutations import (  # import_datapoint_modbus,; import_datasource_modbus,; send_data_to_scada,
    DATAPOINT_MODBUS_FIELDS,
    # DATASOURCE_MODBUS_FIELDS,
    send_to_scada,
)
from app.scadalts import (
    import_datapoint_modbus,
    # import_datasource_modbus,
)
from app.settings import configs

pd.options.mode.copy_on_write = True

class DpModbusDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados Modbus"""

    def __init__(self):
        super().__init__(table_name="DP_MODBUS_IP", primary_key="xid_sensor")

    def _apply_changes(self, changes: Dict[str, Any], df: pd.DataFrame, db: DatabaseConnection):
        """Aplica as alterações ao banco de dados"""
        if changes["remove"]:
            self._remove_records_scada_lts(record_ids=changes["remove"], db=db)
            self._remove_records(changes["remove"], db=db)

        if not changes["update"].empty:
            self._update_records(changes["update"], db=db)
            self._sync_datapoint_scada(df=changes["update"])

        if not changes["new"].empty:
            self._insert_records(changes["new"], db=db)
            self._sync_datapoint_scada(df=changes["new"])

    def _sync_datapoint_scada(self, df: pd.DataFrame):
        """Sincroniza os dados com o ScadaLTS"""
        print("DpModbusDataSynchronizer... Syncing with ScadaLTS")
        df = df[DATAPOINT_MODBUS_FIELDS]
        # garanta que o xid_equip seja uma string
        df["xid_equip"] = df["xid_equip"].astype(str)
        # use o xid_equip_to_host para substituir o xid_equip por host
        df["xid_equip"] = df["xid_equip"].map(configs.xid_equip_to_host)
        send_to_scada(df=df, import_function=import_datapoint_modbus)
        logger.info(
            f"Enviados {len(df)} registros para o ScadaLTS, usando {import_datapoint_modbus} como função de importação."
        )
