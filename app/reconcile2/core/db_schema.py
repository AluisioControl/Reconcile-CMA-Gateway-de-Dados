from abc import ABC, abstractmethod
from typing import Dict

from .db_connection import DatabaseConnection


class DatabaseSchema(ABC):
    """Define esquema de banco de dados"""

    @abstractmethod
    def initialize(self, db: DatabaseConnection):
        pass


class GenericSchema(DatabaseSchema):
    """Esquema genérico para tabelas"""

    def __init__(self, table_name: str, fields: Dict[str, str], primary_key: str):
        self.table_name = table_name
        self.fields = fields
        self.primary_key = primary_key

    def initialize(self, db: DatabaseConnection):
        """Cria a tabela no banco de dados, se não existir"""	
        fields_str = ", ".join(f"{k} {v}" for k, v in self.fields.items())
        query = f"""
            CREATE TABLE IF NOT EXISTS "{self.table_name}" (
                {fields_str},
                PRIMARY KEY ({self.primary_key})
            );
        """
        db.execute(query)
