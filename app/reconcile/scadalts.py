import json
import pandas as pd
from app.scadalts import auth_ScadaLTS, send_data_to_scada, import_datasource_modbus, import_datapoint_modbus
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


# Load hardware data from JSON files
with open("./data.json") as f:
    # Parse each hardware data
    data = json.load(f)

data_fields = list(data[0].keys())

df = pd.DataFrame(data)
print("len(df):", len(df))

# filtar unicos pela coluna id_sen
df = df.drop_duplicates(subset=["id_sen"])
print("len(df):", len(df))

mapping = map_fields(
    base_translate=all_translates,
    base_in="Lógica de montagem",
    base_out="Import ScadaLTS",
)
# reduzir o mapping para os campos que existem data_fields
mapping = {k: v for k, v in mapping.items() if k in data_fields}

print("\nMapping:", mapping)

print("converted to: Import ScadaLTS")
# in_fields = list(mapping.keys())
# print("\nin_fields:", in_fields)
df = df.rename(columns=mapping)

out_fields = [
    "xid_equip", "updatePeriodType", "enabled", "host", 
    "maxReadBitCount", "maxReadRegisterCount", 
    "maxWriteRegisterCount", "port", "retries", "timeout", "updatePeriods"
]
df = df[out_fields]
print(df)
# print(df[out_fields])

# remover os xid_equip com valores nulos ou vazios
df = df[df['xid_equip'].notna() & df['xid_equip'].str.strip().astype(bool)]
print(df)
print("len(df):", len(df))

print("login ScadaLTS")
try:
    auth_ScadaLTS()
except Exception as e:
    print("Error:", e)

# import datapoints
for index, row in df.iterrows():
    datasource = import_datasource_modbus(row['xid_equip'], row['updatePeriodType'], row['enabled'], row['host'],
                             row['maxReadBitCount'], row['maxReadRegisterCount'],
                             row['maxWriteRegisterCount'], row['port'], row['retries'], row['timeout'], row['updatePeriods'])
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
print("len(df):", len(df))

# remover os id_reg_mod com valores nulos ou vazios -isolar os dos modbus
df = df[df['id_reg_mod'].notna() & df['id_reg_mod'].str.strip().astype(bool)]

mapping = map_fields(
    base_translate=all_translates,
    base_in="Lógica de montagem",
    base_out="Import ScadaLTS",
)
# reduzir o mapping para os campos que existem data_fields
mapping = {k: v for k, v in mapping.items() if k in data_fields}

print("\nMapping:", mapping)

print("converted to: Import ScadaLTS")
# in_fields = list(mapping.keys())
# print("\nin_fields:", in_fields)
df = df.rename(columns=mapping)

out_fields = [
    "xid_equip", "updatePeriodType", "enabled", "host", 
    "maxReadBitCount", "maxReadRegisterCount", 
    "maxWriteRegisterCount", "port", "retries", "timeout", "updatePeriods"
]
df = df[out_fields]
print(df)
# print(df[out_fields])

# remover os xid_equip com valores nulos ou vazios
df = df[df['xid_equip'].notna() & df['xid_equip'].str.strip().astype(bool)]
print(df)
print("len(df):", len(df))

for index, row in df.iterrows():
    datasource = import_datapoint_modbus(row['xid_equip'], row['updatePeriodType'], row['enabled'], row['host'],
                             row['maxReadBitCount'], row['maxReadRegisterCount'],
                             row['maxWriteRegisterCount'], row['port'], row['retries'], row['timeout'], row['updatePeriods'])
    send_data_to_scada(datasource)






