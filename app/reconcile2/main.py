import json
import sys

import pandas as pd

from app.getters.gateway import parse_gateway_data
from app.logger import logger
from app.reconcile2.core.data_loader import GatewayDataLoader, JsonDataLoader
from app.reconcile2.core.data_translator import DataTranslator
from app.reconcile2.core.db_connection import DatabaseConnection
from app.reconcile2.core.db_schema import GenericSchema
from app.reconcile2.domain.equipment_sync import ModbusEquipmentSynchronizer
from app.reconcile2.domain.gateway_sync import GatewayDataSynchronizer
from app.reconcile2.domain.modbus_sync import DpModbusDataSynchronizer
from app.reconcile2.domain.tags_sync import (
    DpTagsDataSynchronizer,
    EqpTagsDataSynchronizer,
)
from app.scadalts import auth_ScadaLTS
from app.settings import configs
from app.translator import (
    gateway_translate,
    hardware_translate,
    map_fields,
    registradores_modbus_translate,
    sensores_modbus_translate,
)
from app.utils.data import combine_primary_with_secondary


def create_gateway_schema() -> GenericSchema:
    return GenericSchema(
        table_name="CMA_GD",
        fields={
            "xid_gateway": "VARCHAR NOT NULL",
            "subestacao": "VARCHAR",
            "regional": "VARCHAR",
            "host": "VARCHAR",
            "status": "BOOLEAN",
        },
        primary_key="xid_gateway",
    )


def create_modbus_schema() -> GenericSchema:
    return GenericSchema(
        table_name="DP_MODBUS_IP",
        fields={
            "xid_sensor": "VARCHAR NOT NULL",
            "xid_equip": "VARCHAR",
            "range": "VARCHAR",
            "modbusDataType": "VARCHAR",
            "additive": "INTEGER",
            "offset": "INTEGER",
            "bit": "INTEGER",
            "multiplier": "FLOAT",
            "slaveId": "INTEGER",
            "enabled": "BOOLEAN",
            "nome": "VARCHAR",
            "tipo": "VARCHAR",
            "classificacao": "VARCHAR",
        },
        primary_key="xid_sensor",
    )


def create_modbus_equipment_schema() -> GenericSchema:
    return GenericSchema(
        table_name="EQP_MODBUS_IP",
        fields={
            "xid_equip": "VARCHAR NOT NULL",
            "xid_gateway": "VARCHAR",
            "fabricante": "VARCHAR",
            "modelo": "VARCHAR",
            "type": "VARCHAR",
            "sap_id": "VARCHAR",
            "enabled": "BOOLEAN",
            "updatePeriodType": "VARCHAR",
            "maxReadBitCount": "INTEGER",
            "maxReadRegisterCount": "INTEGER",
            "maxWriteRegisterCount": "INTEGER",
            "host": "VARCHAR",
            "port": "INTEGER",
            "retries": "INTEGER",
            "timeout": "INTEGER",
            "updatePeriods": "INTEGER",
        },
        primary_key="xid_equip",
    )


def create_equipment_dnp3_schema() -> GenericSchema:
    return GenericSchema(
        table_name="EQP_DNP3",
        fields={
            "xid_equip": "VARCHAR NOT NULL",
            "xid_gateway": "VARCHAR",
            "fabricante": "VARCHAR",
            "modelo": "VARCHAR",
            "type": "VARCHAR",
            "sap_id": "VARCHAR",
            "enabled": "BOOLEAN",
            "eventsPeriodType": "VARCHAR",
            "host": "VARCHAR",
            "port": "INTEGER",
            "rbePollPeriods": "INTEGER",
            "retries": "INTEGER",
            "slaveAddress": "INTEGER",
            "sourceAddress": "INTEGER",
            "staticPollPeriods": "INTEGER",
            "timeout": "INTEGER",
        },
        primary_key="xid_equip",
    )


def create_eqp_tags_schema() -> GenericSchema:
    return GenericSchema(
        table_name="TAGS_EQP",
        fields={
            "id": "VARCHAR NOT NULL",
            "xid_equip": "VARCHAR",
            "nome": "VARCHAR",
            "valor": "VARCHAR",
        },
        primary_key="id",
    )


def create_dp_tags_schema() -> GenericSchema:
    return GenericSchema(
        table_name="DP_TAGS",
        fields={
            "id": "VARCHAR NOT NULL",
            "xid_sensor": "VARCHAR",
            "nome": "VARCHAR",
            "valor": "VARCHAR",
        },
        primary_key="id",
    )


def sync_gateways():
    logger.info("Sincronizando dados de gateways...")
    loader = GatewayDataLoader("./cma_gateways.json", parse_gateway_data)
    translator = DataTranslator(
        map_fields(gateway_translate, "Lógica de montagem", "Gateway de Dados")
    )
    schema = create_gateway_schema()
    synchronizer = GatewayDataSynchronizer()

    df = loader.load()
    df_translated = translator.translate(df)
    # no df_translated, manter apenas as colunas que existem no schema
    df_translated = df_translated[schema.fields.keys()]

    with DatabaseConnection(configs.sqlite_db_path) as db:
        schema.initialize(db)
        synchronizer.synchronize(df_translated, db)

    print("Atualização gateway concluída!\n")


def sync_dp_modbus(df: pd.DataFrame):
    logger.info("Sincronizando dados Modbus...")
    # loader = JsonDataLoader("./data.json")
    translator = DataTranslator(
        map_fields(
            registradores_modbus_translate + sensores_modbus_translate,
            "Lógica de montagem",
            "Banco Middlware",
        )
    )
    schema = create_modbus_schema()
    synchronizer = DpModbusDataSynchronizer()

    # df = loader.load()  # carregar dados do arquivo json
    df = df.drop_duplicates(subset=["id_reg_mod"])  # remover registros duplicados
    df["id_reg_mod"] = df["id_reg_mod"].astype(
        str
    )  # converter para string evitando erros
    df = df[
        df["id_reg_mod"].notnull() & (df["id_reg_mod"] != "")
    ]  # remover registros nulos ou vazios
    df_translated = translator.translate(df)  # traduzir campos cma_web to cma_gateway
    # remover colunas duplicadas depois da tradução
    df_translated = df_translated.loc[:, ~df_translated.columns.duplicated()]
    out_fields = [
        "xid_sensor",
        "xid_equip",
        "range",
        "modbusDataType",
        "additive",
        "offset",
        "bit",
        "multiplier",
        "slaveId",
        "enabled",
        "nome",
        "tipo",
        "classificacao",
    ]
    df_final = df_translated[out_fields]  # manter apenas as colunas desejadas

    with DatabaseConnection(configs.sqlite_db_path) as db:
        schema.initialize(db)
        synchronizer.synchronize(df_final, db)

    print("Atualização dp modbus concluída!\n")


def sync_eqp_modbus(df: pd.DataFrame):
    logger.info("Sincronizando dados de equipamentos Modbus...")
    # loader = JsonDataLoader("./data.json")
    translator = DataTranslator(
        map_fields(
            gateway_translate + hardware_translate + sensores_modbus_translate,
            "Lógica de montagem",
            "Banco Middlware",
        )
    )
    schema = create_modbus_equipment_schema()
    synchronizer = ModbusEquipmentSynchronizer()

    # df = loader.load()  # carregar dados do arquivo json
    df = df.drop_duplicates(subset=["id_sen"])  # remover sensores duplicados
    df["id_sen"] = df["id_sen"].astype(str)  # converter para string evitando erros
    df = df[
        df["id_sen"].notnull() & (df["id_sen"] != "")
    ]  # remover registros nulos ou vazios
    df_translated = translator.translate(df)  # traduzir campos cma_web to cma_gateway
    # remover colunas duplicadas depois da tradução
    df_translated = df_translated.loc[:, ~df_translated.columns.duplicated()]
    df_final = df_translated[
        synchronizer.OUTPUT_FIELDS
    ]  # manter apenas as colunas desejadas
    # remover colunas duplicadas depois da
    with DatabaseConnection(configs.sqlite_db_path) as db:
        schema.initialize(db)
        synchronizer.synchronize(df_final, db)
    print("Atualização equipamento modbus concluída!\n")


def sync_eqp_tags(df: pd.DataFrame):  # tags dos registradores
    logger.info("Sincronizando tags de equipamentos...")
    # loader = JsonDataLoader("./data.json")
    translator = DataTranslator(
        map_fields(
            gateway_translate + hardware_translate,
            "Lógica de montagem",
            "Banco Middlware",
        )
    )
    schema = create_eqp_tags_schema()
    synchronizer = EqpTagsDataSynchronizer()

    # df = loader.load()  # carregar dados do arquivo json
    df = df.drop_duplicates(subset=["id_sen"])  # remover registros duplicados
    df["id_sen"] = df["id_sen"].astype(str)  # converter para string evitando erros
    # remover os id_sen com valores nulos ou vazios
    df = df[df["id_sen"].notna() & df["id_sen"].str.strip().astype(bool)]

    df["sen_mod_tags"] = df["sen_mod_tags"].apply(lambda x: json.loads(x))

    # precisamos pegar o valor de sen_mod_tags que é um json e transformar em um DataFrame
    combined_tags = []
    for index, row in df.iterrows():
        combined_tags += combine_primary_with_secondary(
            {"id_sen": row["id_sen"]}, row["sen_mod_tags"]
        )

    if not combined_tags:
        logger.warning("Nenhuma tag de equipamento modbus encontrada.")
        return

    df_final = pd.DataFrame(combined_tags)
    df_final.rename(
        columns={"id_sen": "xid_equip", "name": "nome", "value": "valor"}, inplace=True
    )
    df_final["id"] = df_final["id"].astype(str)
    df_final["xid_equip"] = df_final["xid_equip"].astype(str)
    df_final["nome"] = df_final["nome"].astype(str)
    df_final["valor"] = df_final["valor"].astype(str)

    with DatabaseConnection(configs.sqlite_db_path) as db:
        schema.initialize(db)
        synchronizer.synchronize(df_final, db)
    print("Atualização tags de equipamentos concluída!\n")


def sync_dp_tags(df: pd.DataFrame):  # tags dos sensores
    logger.info("Sincronizando tags dos sensores...")
    # loader = JsonDataLoader("./data.json")
    translator = DataTranslator(
        map_fields(
            gateway_translate + hardware_translate,
            "Lógica de montagem",
            "Banco Middlware",
        )
    )
    schema = create_dp_tags_schema()
    synchronizer = DpTagsDataSynchronizer()

    # df = loader.load()  # carregar dados do arquivo json
    df = df.drop_duplicates(subset=["id_sen"])  # remover registros duplicados
    df["id_sen"] = df["id_sen"].astype(str)  # converter para string evitando erros
    # remover os id_sen com valores nulos ou vazios
    df = df[df["id_sen"].notna() & df["id_sen"].str.strip().astype(bool)]

    df["sen_mod_tags"] = df["sen_mod_tags"].apply(lambda x: json.loads(x))

    combined_tags = []
    for index, row in df.iterrows():
        combined_tags += combine_primary_with_secondary(
            {"id_sen": row["id_sen"]}, row["sen_mod_tags"]
        )

    if not combined_tags:
        logger.warning("Nenhuma tag de sensor modbus encontrada.")
        return

    df_final = pd.DataFrame(combined_tags)
    df_final.rename(
        columns={"id_sen": "xid_sensor", "name": "nome", "value": "valor"}, inplace=True
    )
    df_final["id"] = df_final["id"].astype(str)
    df_final["xid_sensor"] = df_final["xid_sensor"].astype(str)
    df_final["nome"] = df_final["nome"].astype(str)
    df_final["valor"] = df_final["valor"].astype(str)

    with DatabaseConnection(configs.sqlite_db_path) as db:
        schema.initialize(db)
        synchronizer.synchronize(df_final, db)
    print("Atualização tags dos sensores concluída!\n")


if __name__ == "__main__":
    print("Iniciando sincronização...\n")
    logger.info("Iniciando sincronização...")
    loader = JsonDataLoader("./data.json")
    collected_data = loader.load()
    sync_gateways()
    auth_ScadaLTS()
    sync_eqp_modbus(df=collected_data.copy())
    # sync_eqp_dnp3() # TODO: implementar sincronização de equipamentos dnp3
    sync_eqp_tags(
        df=collected_data.copy()
    )  # TODO: implementar tags de equipamentos dnp3
    sync_dp_modbus(df=collected_data.copy())
    sync_dp_tags(
        df=collected_data.copy()
    )  # TODO: implementar tags de equipamentos dnp3
    # Adicionar outras sincronizações aqui
    logger.info("Sincronização concluída!")
    print("\nSincronização concluída!\n")
