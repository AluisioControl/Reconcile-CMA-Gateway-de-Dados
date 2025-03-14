import json

import pandas as pd

from app.scadalts import (
    auth_ScadaLTS,
    import_datapoint_modbus,
    import_datasource_modbus,
    send_data_to_scada,
)
from app.translator import all_translates, map_fields, translate

"""
dp = datapoint = registers
eqp = equipment = datasource = sensores

Este script processa dados de hardware a partir de arquivos JSON e os importa para o ScadaLTS.

O script executa os seguintes passos:
1. Carrega dados de hardware de um arquivo JSON.
2. Filtra e mapeia os campos de dados de acordo com traduções predefinidas.
3. Renomeia as colunas com base no mapeamento.
4. Filtra linhas com valores nulos ou vazios em 'xid_equip'.
5. Autentica no ScadaLTS.
6. Importa os dados como fontes de dados no ScadaLTS.
7. Repete o processo para pontos de dados.

Funções:
- auth_ScadaLTS: Autentica no ScadaLTS.
- send_data_to_scada: Envia dados para o ScadaLTS.
- import_datasource_modbus: Importa uma fonte de dados para o ScadaLTS.
- import_datapoint_modbus: Importa um ponto de dados para o ScadaLTS.
- all_translates: Fornece todos os mapeamentos de tradução.
- map_fields: Mapeia campos com base nos mapeamentos de tradução.
- translate: Traduza campos individuais.

Processamento de Dados:
- Carrega dados de 'data.json'.
- Filtra linhas únicas com base em 'id_sen'.
- Mapeia e renomeia colunas com base em traduções predefinidas.
- Filtra linhas com valores nulos ou vazios em 'xid_equip'.
- Importa os dados processados para o ScadaLTS como fontes de dados e pontos de dados.

Nota:
- O script assume a presença de 'data.json' no diretório atual.
- O script usa pandas para manipulação de dados e json para análise de arquivos JSON.

"""

print("Processando dados de Sensores...")
# Load hardware data from JSON files
with open("./data.json") as f:
    # Parse each hardware data
    data = json.load(f)

data_fields = list(data[0].keys())

df = pd.DataFrame(data)

# filtar unicos pela coluna id_sen
df = df.drop_duplicates(subset=["id_sen"])

mapping = map_fields(
    base_translate=all_translates,
    base_in="Lógica de montagem",
    base_out="Import ScadaLTS",
)
# reduzir o mapping para os campos que existem data_fields
mapping = {k: v for k, v in mapping.items() if k in data_fields}
df = df.rename(columns=mapping)
# remover coluna duplicada por conta da tradução
df = df.loc[:, ~df.columns.duplicated()]
out_fields = [
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
df = df[out_fields]  # Selecionar apenas os campos de saída

# remover os xid_equip com valores nulos ou vazios
df = df[df["xid_equip"].notna() & df["xid_equip"].str.strip().astype(bool)]

print("login ScadaLTS")
auth_ScadaLTS()

# import datapoints
for index, row in df.iterrows():
    print("\nsend datasource to ScalaLTS:", row.to_dict(), "\n")
    datasource = import_datasource_modbus(
        xid_equip=row["xid_equip"],
        updatePeriodType=row["updatePeriodType"],
        enabled=row["enabled"],
        host=row["host"],
        maxReadBitCount=row["maxReadBitCount"],
        maxReadRegisterCount=row["maxReadRegisterCount"],
        maxWriteRegisterCount=row["maxWriteRegisterCount"],
        port=row["port"],
        retries=row["retries"],
        timeout=row["timeout"],
        updatePeriods=row["updatePeriods"],
    )
    send_data_to_scada(datasource)

##########################
# PROCESSAR OS REGISTROS #
##########################

# Load hardware data from JSON files
with open("./data.json") as f:
    # Parse each hardware data
    data = json.load(f)

data_fields = list(data[0].keys())

df = pd.DataFrame(data)

# remover os id_reg_mod com valores nulos ou vazios -isolar os dos modbus
df = df[df["id_reg_mod"].notna() & df["id_reg_mod"].str.strip().astype(bool)]

mapping = map_fields(
    base_translate=all_translates,
    base_in="Lógica de montagem",
    base_out="Import ScadaLTS",
)
# reduzir o mapping para os campos que existem data_fields
mapping = {k: v for k, v in mapping.items() if k in data_fields}

df = df.rename(columns=mapping)

# remover coluna duplicada por conta da tradução
df = df.loc[:, ~df.columns.duplicated()]

out_fields = [
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
df = df[out_fields]

# remover os xid_equip com valores nulos ou vazios
df = df[df["xid_equip"].notna() & df["xid_equip"].str.strip().astype(bool)]

for index, row in df.iterrows():
    print("\nSend datapoint to ScadaLTS:", row.to_json(), "\n")
    datasource = import_datapoint_modbus(
        xid_sensor=row["xid_sensor"],
        range=row["range"],
        modbusDataType=row["modbusDataType"],
        additive=row["additive"],
        bit=row["bit"],
        multiplier=row["multiplier"],
        offset=row["offset"],
        slaveId=row["slaveId"],
        xid_equip=row["xid_equip"],
        enabled=row["enabled"],
        nome=row["nome"],
    )
    send_data_to_scada(datasource)
