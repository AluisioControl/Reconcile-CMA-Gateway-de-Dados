import json
from time import sleep

import pandas as pd

from app.logger import logger
from app.scadalts import (
    auth_ScadaLTS,
    import_datapoint_dnp3,
    import_datapoint_modbus,
    import_datasource_dnp3,
    import_datasource_modbus,
    send_data_to_scada,
)
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
        print(f"Erro ao carregar o arquivo {file_path}: {e}")
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
        print("DataFrame vazio.")
        return
    for _, row in df.iterrows():
        try:
            if row.isnull().values.any():
                logger.error(f"Faltando dados: {row.to_dict()}")
                continue
            data = import_function(**row.to_dict())
            print(f"Dados: {row.to_dict()}\n")
            send_data_to_scada(data)
            sleep(0.3)
        except Exception as e:
            logger.error(f"Erro ao enviar dados: {e}")


def main():
    """Função principal que coordena o processamento e envio de dados para o ScadaLTS."""

    # Processar e importar fontes de dados
    print("Processando dados de Sensores...")
    df_data_all = load_json_data("./data.json")

    # Autenticação
    print("Login ScadaLTS")
    auth_ScadaLTS()

    # Carregar mapeamento de campos
    mapping = map_fields(
        base_translate=all_translates,
        base_in="Lógica de montagem",
        base_out="Import ScadaLTS",
    )

    # Processar e importar datasources (sensores modbus)
    if "id_sen" in df_data_all.columns:
        print("\nProcessando datasources modbus...")
        df_datasources = process_data(
            df_data_all, mapping, DATASOURCE_MODBUS_FIELDS, unique_key="id_sen"
        )
        print("\nEnviando datasources modbus para o ScadaLTS...")
        send_to_scada(df_datasources, import_datasource_modbus)

    # Processar e importar datapoints (registradores modbus)
    print(df_data_all["id_reg_mod"])
    print(df_data_all.columns)
    if "id_reg_mod" in df_data_all.columns:
        print("\nProcessando datapoints modbus...")
        df_datapoints = process_data(
            df_data_all, mapping, DATAPOINT_MODBUS_FIELDS, filter_column="id_reg_mod"
        )
        print("\nEnviando datapoint modbus para o ScadaLTS...")
        send_to_scada(df_datapoints, import_datapoint_modbus)
    else:
        print("Não há dados de datapoints modbus.")

    # Processar e importar datasources (sensores dnp3)
    if "id_sen_dnp3" in df_data_all.columns:
        print("\nProcessando datasources dnp3...")
        df_datasources = process_data(
            df_data_all, mapping, DATASOURCE_DNP3_FIELDS, unique_key="id_sen_dnp3"
        )
        print("n\Enviando datasource dnp3 para o ScadaLTS...")
        send_to_scada(df_datasources, import_datasource_dnp3)
    else:
        print("Não há dados de datasources dnp3.")

    # Processar e importar datapoints (registradores dnp3)
    if "id_reg_dnp3" in df_data_all.columns:
        print("\nProcessando datapoints dnp3...")
        df_datapoints = process_data(
            df_data_all, mapping, DATAPOINT_DNP3_FIELDS, filter_column="id_reg_dnp3"
        )
        print("n\Enviando datapoint dnp3 para o ScadaLTS...")
        send_to_scada(df_datapoints, import_datapoint_dnp3)
    else:
        print("Não há dados de datapoints dnp3.")

    print("Processamento concluído!")


if __name__ == "__main__":
    main()
