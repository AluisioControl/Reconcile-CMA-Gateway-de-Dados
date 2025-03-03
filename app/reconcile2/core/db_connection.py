import sqlite3
from typing import Optional

import pandas as pd


class DatabaseConnection:
    """Gerencia conexão com banco de dados"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def execute(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)

    def fetch_dataframe(self, query: str) -> pd.DataFrame:
        return pd.read_sql_query(query, self.connection)
