import json
from time import sleep

import pandas as pd

from app.logger import logger
from app.scadalts import send_data_to_scada
from app.translator import all_translates, map_fields

# Constantes para campos de saída
DATASOURCE_MODBUS_FIELDS = [
    "xid_equip",
    "updatePeriodType",
    "enabled",
    "host",
    "maxReadBitCount",
    "maxReadRegisterCount",
    "maxWriteRegisterCount",
    "port",
    "retries",
    "timeout",
    "updatePeriods",
]

DATASOURCE_DNP3_FIELDS = [
    "xid_equip",
    "eventsPeriodType",
    "enabled",
    "host",
    "port",
    "rbePollPeriods",
    "retries",
    "slaveAddress",
    "sourceAddress",
    "staticPollPeriods",
]

DATAPOINT_MODBUS_FIELDS = [
    "xid_sensor",
    "range",
    "modbusDataType",
    "additive",
    "bit",
    "multiplier",
    "offset",
    "slaveId",
    "xid_equip",
    "enabled",
    "nome",
]

DATAPOINT_DNP3_FIELDS = [
    "xid_sensor",
    "controlCommand",
    "dnp3DataType",
    "index",
    "timeoff",
    "timeon",
    "xid_equip",
    "enable",
]


def load_json_data(file_path):
    """Carrega dados de um arquivo JSON e retorna um DataFrame."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Erro ao carregar o arquivo {file_path}: {e}")
        raise


def process_data(df, mapping, out_fields, filter_column="xid_equip", unique_key=None):
    """Processa o DataFrame: filtra, mapeia e seleciona campos."""
    if unique_key:
        df = df.drop_duplicates(subset=[unique_key])

    if filter_column in df.columns:
        df[filter_column] = df[filter_column].astype(str)
        df = df[df[filter_column].notna() & df[filter_column].str.strip().astype(bool)]
    df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
    df = df.loc[:, ~df.columns.duplicated()]  # Remove colunas duplicadas
    df = df[out_fields]  # Seleciona apenas os campos desejados
    if filter_column in df.columns:
        df[filter_column] = df[filter_column].astype(str)
        df = df[df[filter_column].notna() & df[filter_column].str.strip().astype(bool)]
    return df


def send_to_scada(df, import_function):
    """Envia cada linha do DataFrame para o ScadaLTS usando a função de importação fornecida."""
    if df is None:
        logger.warning(f"send_to_scada {import_function} com DataFrame vazio.")
        return
    for _, row in df.iterrows():
        try:
            if row.isnull().values.any():
                logger.error(f"Faltando dados: {row.to_dict()}")
                continue
            data = import_function(**row.to_dict())
            send_data_to_scada(data)
            sleep(0.1)  # Aguarda 100 ms
        except Exception as e:
            logger.error(f"Erro ao enviar dados: {e}")
            print(f"Erro ao enviar dados: {e}")
            raise e
