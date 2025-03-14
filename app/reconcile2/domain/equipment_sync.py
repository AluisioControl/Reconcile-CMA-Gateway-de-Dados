from typing import Any, Dict, List, Optional

import pandas as pd

from app.logger import logger
from app.reconcile2.core.data_synchronizer import BaseDataSynchronizer
from app.reconcile2.core.db_connection import DatabaseConnection
from app.reconcile2.scadalts.mutations import (
    DATASOURCE_DNP3_FIELDS,
    DATASOURCE_MODBUS_FIELDS,
    send_to_scada
)
from app.scadalts import (
    import_datasource_dnp3,
    import_datasource_modbus,
)
from app.utils.data import combine_primary_with_secondary


class EquipmentDataSynchronizer(BaseDataSynchronizer):
    """Sincroniza dados de equipamentos com o banco de dados"""

    def __init__(
        self,
        table_name: str,
        primary_key: str,
        output_fields: List[str],
        unique_key: str,
    ):
        """
        Inicializa o sincronizador de equipamentos.

        Args:
            table_name: Nome da tabela no banco de dados
            primary_key: Nome da chave primária
            output_fields: Lista de campos a serem sincronizados
            unique_key: Campo usado para remover duplicatas
        """
        super().__init__(table_name=table_name, primary_key=primary_key)
        self.output_fields = output_fields
        self.unique_key = unique_key

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Pré-processa os dados antes da sincronização.

        Args:
            df: DataFrame bruto vindo do loader

        Returns:
            DataFrame processado e filtrado
        """
        # Remover duplicatas pelo campo único
        df = df.drop_duplicates(subset=[self.unique_key])

        # Converter a chave primária para string
        df[self.primary_key] = df[self.primary_key].astype(str)

        # Remover registros com chave primária nula ou vazia
        df = df[
            df[self.primary_key].notna() & df[self.primary_key].str.strip().astype(bool)
        ]

        # Selecionar apenas os campos de saída
        df = df[self.output_fields]

        return df

    def synchronize(self, df: pd.DataFrame, db: DatabaseConnection):
        """
        Sincroniza os dados de equipamentos após pré-processamento.

        Args:
            df: DataFrame com os dados a sincronizar
            db: Conexão com o banco de dados
        """
        processed_df = self.preprocess_data(df)
        super().synchronize(processed_df, db)

    def _apply_changes(
        self, changes: Dict[str, Any], df: pd.DataFrame, db: DatabaseConnection
    ):
        """Aplica as alterações ao banco de dados"""
        if changes["remove"]:
            records = self._get_record_by_ids(changes["remove"], db)
            records = records.copy()  # evitar problemas de referência
            records["enabled"] = False
            self._sync_datapoint_scada(df=records)
            self._remove_records(changes["remove"], db)

        if not changes["update"].empty:
            self._update_records(changes["update"], db)
            self._sync_datapoint_scada(df=changes["update"])

        if not changes["new"].empty:
            self._insert_records(changes["new"], db)
            self._sync_datapoint_scada(df=changes["new"])

    def _sync_datapoint_scada(self, df: pd.DataFrame):
        """Sincroniza os dados com o ScadaLTS"""
        print("_sync_datapoint_scada... Syncing with ScadaLTS")
        import_function = import_datasource_modbus
        if self.table_name == "EQP_MODBUS_IP":
            df = df[DATASOURCE_MODBUS_FIELDS]
        elif self.table_name == "EQP_DNP3":
            df = df[DATASOURCE_DNP3_FIELDS]
            import_function = import_datasource_dnp3
        else:
            raise ValueError(f"Tabela não suportada: {self.table_name}")
        send_to_scada(df=df, import_function=import_function)
        logger.info(f"Enviados {len(df)} registros para o ScadaLTS, usando {import_function.__name__}.")


class ModbusEquipmentSynchronizer(EquipmentDataSynchronizer):
    """Sincroniza equipamentos Modbus"""

    OUTPUT_FIELDS = [
        "xid_equip",
        "xid_gateway",
        "fabricante",
        "modelo",
        "type",
        "sap_id",
        "enabled",
        "updatePeriodType",
        "maxReadBitCount",
        "maxReadRegisterCount",
        "maxWriteRegisterCount",
        "host",
        "port",
        "retries",
        "timeout",
        "updatePeriods",
    ]

    def __init__(self):
        super().__init__(
            table_name="EQP_MODBUS_IP",
            primary_key="xid_equip",
            output_fields=self.OUTPUT_FIELDS,
            unique_key="xid_equip",
        )


class DNP3EquipmentSynchronizer(EquipmentDataSynchronizer):
    """Sincroniza equipamentos DNP3"""

    OUTPUT_FIELDS = [
        "xid_equip",
        "xid_gateway",
        "fabricante",
        "modelo",
        "type",
        "sap_id",
        "enabled",
        "updatePeriodType",
        "maxReadBitCount",
        "maxReadRegisterCount",
        "maxWriteRegisterCount",
        "host",
        "port",
        "retries",
        "timeout",
        "updatePeriods",
    ]

    def __init__(self):
        super().__init__(
            table_name="EQP_DNP3",
            primary_key="xid_equip",
            output_fields=self.OUTPUT_FIELDS,
            unique_key="id_sen_dnp3",
        )
