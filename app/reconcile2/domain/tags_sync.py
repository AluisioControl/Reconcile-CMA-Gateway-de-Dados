from typing import Dict

from app.reconcile2.core.data_synchronizer import BaseDataSynchronizer
from app.reconcile2.core.db_connection import DatabaseConnection
from app.logger import logger

import pandas as pd


class DpTagsDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados de gateways"""

    def __init__(self):
        super().__init__(table_name="DP_TAGS", primary_key="id")

    def _apply_changes(
        self, changes: Dict[str, any], df: pd.DataFrame, db: DatabaseConnection
    ):
        if changes["remove"]:
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} IN ({','.join(map(str, changes['remove']))})"
            db.execute(query)
            logger.info(f"Removido o DP_TAG de id: {changes['remove']}")
        else:
            logger.info("Nenhum DP_TAG removido")

        if not changes["update"].empty:
            changes["update"].to_sql(
            self.table_name, db.connection, if_exists="replace", index=False
            )
            logger.info(f"Atualizado DP_TAG: {changes['update']['id'].to_list()}")
        else:
            logger.info("Nenhum DP_TAG atualizado")

        if not changes["new"].empty:
            changes["new"].to_sql(
            self.table_name, db.connection, if_exists="append", index=False
            )
            logger.info(f"Inserido novo DP_TAG {changes['new']['id'].to_list()}")
        else:
            logger.info("Nenhum novo DP_TAG inserido")


class EqpTagsDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados de equipamentos"""

    def __init__(self):
        super().__init__(table_name="EQP_TAGS", primary_key="id")

    def _apply_changes(
        self, changes: Dict[str, any], df: pd.DataFrame, db: DatabaseConnection
    ):
        if changes["remove"]:
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} IN ({','.join(map(str, changes['remove']))})"
            db.execute(query)
            logger.info(f"Removido o EQP_TAG de id: {changes['remove']}")
        else:
            logger.info("Nenhum EQP_TAG removido")

        if not changes["update"].empty:
            changes["update"].to_sql(
            self.table_name, db.connection, if_exists="replace", index=False
            )
            logger.info(f"Atualizado EQP_TAG: {changes['update']['id'].to_list()}")
        else:
            logger.info("Nenhum EQP_TAG atualizado")

        if not changes["new"].empty:
            changes["new"].to_sql(
            self.table_name, db.connection, if_exists="append", index=False
            )
            logger.info(f"Inserido novo EQP_TAG {changes['new']['id'].to_list()}")
        else:
            logger.info("Nenhum novo EQP_TAG inserido")
