from typing import Dict

import pandas as pd

from app.reconcile2.core.data_synchronizer import BaseDataSynchronizer
from app.reconcile2.core.db_connection import DatabaseConnection
from app.translator import gateway_translate, map_fields


class GatewayDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados de gateways"""

    def __init__(self):
        super().__init__(table_name="CMA_GD", primary_key="xid_gateway")

    def _apply_changes(
        self, changes: Dict[str, any], df: pd.DataFrame, db: DatabaseConnection
    ):
        if changes["remove"]:
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} IN (\"{'","'.join(map(str, changes['remove']))}\")"
            print("\n\tquery:", query)
            db.execute(query)
            print(f"\tRemovidos {len(changes['remove'])} registros.")

        if not changes["update"].empty:
            changes["update"].to_sql(
                self.table_name, db.connection, if_exists="replace", index=False
            )
            print(f"\tAtualizados {len(changes['update'])} registros.")

        if not changes["new"].empty:
            print("\n\tInserindo novos registros:")
            print(changes["new"])
            changes["new"].to_sql(
                self.table_name, db.connection, if_exists="append", index=False
            )
            print(f"\n\tInseridos {len(changes['new'])} novos registros.")
