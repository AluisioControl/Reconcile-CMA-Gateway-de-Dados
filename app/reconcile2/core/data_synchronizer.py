from abc import ABC, abstractmethod
from typing import Dict, Set
from app.logger import logger
import pandas as pd

from .db_connection import DatabaseConnection


class DataSynchronizer(ABC):
    """Interface para sincronização de dados"""

    @abstractmethod
    def synchronize(self, df: pd.DataFrame, db: DatabaseConnection):
        pass


class BaseDataSynchronizer(DataSynchronizer):
    """Implementação base para sincronização"""

    def __init__(self, table_name: str, primary_key: str):
        self.table_name = table_name
        self.primary_key = primary_key

    def synchronize(self, df: pd.DataFrame, db: DatabaseConnection):
        existing_data = self._get_existing_data(db)
        changes = self._analyze_changes(df, existing_data)

        self._log_changes(changes)
        self._apply_changes(changes, df, db)

    def _get_existing_data(self, db: DatabaseConnection) -> pd.DataFrame:
        return db.fetch_dataframe(f"SELECT * FROM {self.table_name}")

    def _analyze_changes(
        self, df: pd.DataFrame, existing_data: pd.DataFrame
    ) -> Dict[str, any]:
        """
        Analisa as diferenças entre os DataFrames e retorna um dicionário com as alterações.

        args:
            df: DataFrame com os novos dados
            existing_data: DataFrame com os dados existentes no banco de dados
        
        returns:
            Dicionário com 'new' (novos registros), 'update' (registros a atualizar),
            'remove' (IDs a remover) e 'total' (total de registros de entrada)
        """
        new_records = df[~df[self.primary_key].isin(existing_data[self.primary_key])]
        common_records = df[df[self.primary_key].isin(existing_data[self.primary_key])]

        # Normalizar os tipos de dados entre os DataFrames novos e existentes (se necessário)
        if list(common_records.dtypes) != list(existing_data.dtypes):
            for column in common_records.columns: # analisar cada coluna
                if common_records[column].dtype != existing_data[column].dtype: # se o tipo de dado for diferente
                    # converter o tipo de dado da coluna do DataFrame comum para o tipo de dado do DataFrame existente
                    existing_data[column] = existing_data[column].astype(common_records[column].dtype)

        # regra de negócio: só atualizar registros que possuem diferenças
        # remover do common_records os registros que são iguais ao existing_data
        common_records = common_records[~common_records.eq(existing_data).all(axis=1)]

        df_ids = set(df[self.primary_key]) # conjunto de IDs do DataFrame
        db_ids = set(existing_data[self.primary_key]) # conjunto de IDs do banco de dados
        records_to_remove = db_ids - df_ids # IDs a remover são os IDs do banco de dados que não estão no DataFrame

        return {
            "new": new_records, # novos registros para inserir
            "update": common_records, # registros necessitando atualizar
            "remove": records_to_remove, # IDs a remover (registros que não estão no DataFrame são desnecessários)
            "total": len(df), # total de registros de entrada
        }

    def _log_changes(self, changes: Dict[str, any]):
        """Exibe um resumo das alterações identificadas"""
        mgs = (
            f"Registros no DataFrame: {changes['total']}\n"
            f"\tNovos: {len(changes['new'])}\n"
            f"\tAtualizar: {len(changes['update'])}\n"
            f"\tRemover: {len(changes['remove'])}\n"
        )
        logger.info(mgs)
        print(mgs)

    @abstractmethod
    def _apply_changes(
        self, changes: Dict[str, any], df: pd.DataFrame, db: DatabaseConnection
    ):
        """
        Aplica as alterações identificadas ao banco de dados.

        Args:
            changes: Dicionário com 'new' (novos registros), 'update' (registros a atualizar),
                    'remove' (IDs a remover) e 'total' (total de registros)
            df: DataFrame original com todos os dados
            db: Conexão com o banco de dados
        """
        # 1. Remover registros que não estão mais no DataFrame
        if changes["remove"]:
            self._remove_records(changes["remove"], db)

        # 2. Atualizar registros existentes
        if not changes["update"].empty:
            self._update_records(changes["update"], db)

        # 3. Inserir novos registros
        if not changes["new"].empty:
            self._insert_records(changes["new"], db)

    def _remove_records(self, record_ids: set, db: DatabaseConnection):
        """Remove registros do banco de dados"""
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} IN (\"{'","'.join(map(str, record_ids))}\")"
        db.execute(query)
        print(f"\tRemovidos {len(record_ids)} registros.")

    def _update_records(self, records: pd.DataFrame, db: DatabaseConnection):
        """Atualiza registros existentes no banco de dados"""
        records.to_sql(self.table_name, db.connection, if_exists="replace", index=False)
        print(f"\tAtualizados {len(records)} registros.")

    def _insert_records(self, records: pd.DataFrame, db: DatabaseConnection):
        """Insere novos registros no banco de dados"""
        records.to_sql(self.table_name, db.connection, if_exists="append", index=False)
        print(f"\n\tInseridos {len(records)} novos registros.")
