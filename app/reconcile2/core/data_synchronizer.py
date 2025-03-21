from abc import ABC, abstractmethod
from typing import Dict, Set

import pandas as pd

from app.logger import logger

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
        if df.empty:
            return {
                "new": df,  # df vazio não há novos registros
                "update": df,  # df vazio não há registros a atualizar
                "remove": set(
                    existing_data[self.primary_key]
                ),  # remover todos os registros existentes
                "total": len(df),  # total de registros de entrada
            }
        # verificar se o df tem totas as colunas do existing_data
        if not df.columns.equals(existing_data.columns):
            # quais colunas estão faltando no df
            missing_columns = existing_data.columns.difference(df.columns)
            # criar as colunas faltantes no df com valores string vazios
            for column in missing_columns:
                df[column] = ""
                print(f"Coluna {column} criada no DataFrame com valores vazios")

        # só manter as colunas que existem no existing_data
        df = df[existing_data.columns]

        new_records = df[~df[self.primary_key].isin(existing_data[self.primary_key])]
        common_records = df[df[self.primary_key].isin(existing_data[self.primary_key])]

        # IDs a remover (registros que não estão no DataFrame são desnecessários)
        df_ids = set(df[self.primary_key])  # conjunto de IDs do DataFrame
        db_ids = set(
            existing_data[self.primary_key]
        )  # conjunto de IDs do banco de dados
        records_to_remove = (
            db_ids - df_ids
        )  # IDs a remover são os IDs do banco de dados que não estão no DataFrame

        # Regra de negócio: só atualizar registros que possuem diferenças
        if not common_records.empty:
            # Normalizar os tipos de dados entre os DataFrames novos e existentes (se necessário)
            if list(common_records.dtypes) != list(existing_data.dtypes):
                for column in common_records.columns:  # analisar cada coluna
                    if (
                        common_records[column].dtype != existing_data[column].dtype
                    ):  # se o tipo de dado for diferente
                        # converter o tipo de dado da coluna do DataFrame comum para o tipo de dado do DataFrame existente
                        try:
                            existing_data[column] = existing_data[column].astype(
                                common_records[column].dtype
                            )
                            logger.warning(
                                f"{column} convertido para {common_records[column].dtype}"
                            )
                        except ValueError as e:
                            logger.error(
                                f"Erro ao converter {column} para {existing_data[column].dtype}: {e}"
                            )
                            # converter o tipo de ambos os DataFrames para o tipo para string
                            common_records[column] = common_records[column].astype(str)
                            existing_data[column] = existing_data[column].astype(str)

            # regra de negócio: só atualizar registros que possuem diferenças
            merged_df = existing_data.merge(
                common_records, indicator=True, how="outer"
            )  # merge dos DataFrames
            changed_rows_df = merged_df[
                merged_df["_merge"] == "right_only"
            ]  # registros que possuem diferenças
            diff_df = changed_rows_df.drop("_merge", axis=1)  # remover a coluna _merge
            common_records = diff_df  # atualizar common_records para os registros que possuem diferenças

        return {
            "new": new_records,  # novos registros para inserir
            "update": common_records,  # registros necessitando atualizar
            "remove": records_to_remove,  # IDs a remover (registros que não estão no DataFrame são desnecessários)
            "total": len(df),  # total de registros de entrada
        }

    def _log_changes(self, changes: Dict[str, any]):
        """Exibe um resumo das alterações identificadas"""
        mgs = (
            f"Total de {changes['total']} para a tabela {self.table_name} sendo: "
            f"Novos: {len(changes['new'])}, "
            f"Atualizar: {len(changes['update'])} e "
            f"Remover: {len(changes['remove'])}."
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
            logger.info(
                f"Removidos {len(changes['remove'])} registros da tabela {self.table_name}."
            )
        else:
            logger.info(f"Nenhum registro removido da tabela {self.table_name}.")

        # 2. Atualizar registros existentes
        if not changes["update"].empty:
            self._update_records(changes["update"], db)
            logger.info(
                f"Atualizados {len(changes['update'])} registros da tabela {self.table_name}."
            )
        else:
            logger.info(f"Nenhum registro atualizado da tabela {self.table_name}.")

        # 3. Inserir novos registros
        if not changes["new"].empty:
            self._insert_records(changes["new"], db)
            logger.info(
                f"Inseridos {len(changes['new'])} novos registros na tabela {self.table_name}."
            )
        else:
            logger.info(f"Nenhum novo registro inserido na tabela {self.table_name}.")

    def _remove_records(self, record_ids: set, db: DatabaseConnection):
        """Remove registros do banco de dados"""
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} IN (\"{'","'.join(map(str, record_ids))}\")"
        db.execute(query)

    def _update_records(self, records: pd.DataFrame, db: DatabaseConnection):
        """Atualiza registros existentes no banco de dados"""
        records.to_sql(self.table_name, db.connection, if_exists="replace", index=False)

    def _insert_records(self, records: pd.DataFrame, db: DatabaseConnection):
        """Insere novos registros no banco de dados"""
        print("Inserindo registros no banco de dados")
        records.to_sql(self.table_name, db.connection, if_exists="append", index=False)

    def _get_record_by_ids(self, ids: list, db: DatabaseConnection) -> Set[str]:
        """Obtém os registros dos IDs fornecidos"""
        query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} IN (\"{'","'.join(map(str, ids))}\")"
        return db.fetch_dataframe(query)
