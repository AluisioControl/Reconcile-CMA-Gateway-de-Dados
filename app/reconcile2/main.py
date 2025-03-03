from app.reconcile2.core.data_loader import GatewayDataLoader, JsonDataLoader
from app.reconcile2.core.data_translator import DataTranslator
from app.reconcile2.core.db_connection import DatabaseConnection
from app.reconcile2.core.db_schema import GenericSchema
from app.reconcile2.domain.gateway_sync import GatewayDataSynchronizer
from app.reconcile2.domain.modbus_sync import DpModbusDataSynchronizer
from app.reconcile2.domain.equipment_sync import ModbusEquipmentSynchronizer

from app.getters.gateway import parse_gateway_data
from app.settings import configs
from app.logger import logger
from app.translator import (
    gateway_translate,
    map_fields,
    registradores_modbus_translate,
    sensores_modbus_translate,
    hardware_translate,
)


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
            "marca": "VARCHAR",
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

    print("\nAtualização gateway concluída!")


def sync_dp_modbus():
    logger.info("Sincronizando dados Modbus...")
    loader = JsonDataLoader("./data.json")
    translator = DataTranslator(
        map_fields(
            registradores_modbus_translate + sensores_modbus_translate,
            "Lógica de montagem",
            "Banco Middlware",
        )
    )
    schema = create_modbus_schema()
    synchronizer = DpModbusDataSynchronizer()

    df = loader.load() # carregar dados do arquivo json
    df = df.drop_duplicates(subset=["id_reg_mod"]) # remover registros duplicados
    df["id_reg_mod"] = df["id_reg_mod"].astype(str) # converter para string evitando erros
    df = df[df["id_reg_mod"].notnull() & (df["id_reg_mod"] != "")] # remover registros nulos ou vazios
    df_translated = translator.translate(df) # traduzir campos cma_web to cma_gateway
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
    df_final = df_translated[out_fields] # manter apenas as colunas desejadas

    with DatabaseConnection(configs.sqlite_db_path) as db:
        schema.initialize(db)
        synchronizer.synchronize(df_final, db)

    print("\nAtualização dp modbus concluída!")

def sync_eqp_modbus():
    logger.info("Sincronizando dados de equipamentos Modbus...")
    loader = JsonDataLoader("./data.json")
    translator = DataTranslator(
        map_fields(
            gateway_translate + hardware_translate + sensores_modbus_translate,
            "Lógica de montagem",
            "Banco Middlware",
        )
    )
    schema = create_modbus_equipment_schema()
    synchronizer = ModbusEquipmentSynchronizer()

    df = loader.load() # carregar dados do arquivo json
    df = df.drop_duplicates(subset=["id_sen"]) # remover registros duplicados
    df["id_sen"] = df["id_sen"].astype(str) # converter para string evitando erros
    df = df[df["id_sen"].notnull() & (df["id_sen"] != "")] # remover registros nulos ou vazios
    df_translated = translator.translate(df) # traduzir campos cma_web to cma_gateway
    # show columns after translation

    df_final = df_translated[synchronizer.OUTPUT_FIELDS] # manter apenas as colunas desejadas
    print("Sensorres traduzidos:")
    # mostrar o primeiro registro traduzido em formato de dicionário
    print(df_final.iloc[0].to_dict())
    # remover colunas duplicadas depois da
    with DatabaseConnection(configs.sqlite_db_path) as db:
        schema.initialize(db)
        synchronizer.synchronize(df_final, db)
    print("\nAtualização equipamento modbus concluída!")

if __name__ == "__main__":
    print("Iniciando sincronização...")
    logger.info("Iniciando sincronização...")
    # sync_gateways()
    # sync_dp_modbus()
    sync_eqp_modbus()
    # Adicionar outras sincronizações aqui
