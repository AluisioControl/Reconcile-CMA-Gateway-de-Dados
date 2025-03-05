from typing import Dict

import pandas as pd

from app.reconcile2.core.data_synchronizer import BaseDataSynchronizer
from app.reconcile2.core.db_connection import DatabaseConnection
from app.translator import gateway_translate, map_fields

from app.logger import logger


class GatewayDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados de gateways"""

    def __init__(self):
        super().__init__(table_name="CMA_GD", primary_key="xid_gateway")

    def _apply_changes(
        self, changes: Dict[str, any], df: pd.DataFrame, db: DatabaseConnection
    ):
        if changes["remove"]:
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} IN (\"{'","'.join(map(str, changes['remove']))}\")"
            db.execute(query)
            logger.info(f"Removido o gateway de id: {changes['remove']}")
        else:
            logger.info("Nenhum gateway removido")

        if not changes["update"].empty:
            changes["update"].to_sql(
                self.table_name, db.connection, if_exists="replace", index=False
            )
            logger.info(f"Atualizado gateway: {changes['update']["xid_gateway"].to_list()}")
        else:
            logger.info("Nenhum gateway atualizado")

        if not changes["new"].empty:
            changes["new"].to_sql(
                self.table_name, db.connection, if_exists="append", index=False
            )
            logger.info(f"Inserido novo gateway {changes['new']["xid_gateway"].to_list()}")
        else:
            logger.info("Nenhum novo gateway inserido")
