import json
import sqlite3

import pandas as pd

from app.getters.hardware import parse_hardware_data
from app.getters.sensors import parse_sensor_modbus_data
from app.settings import configs
from app.utils.data import combine_primary_with_secondary

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

from app.translator import all_translates, map_fields, translate

mapping = map_fields(
    base_translate=all_translates,
    base_in="Lógica de montagem",
    base_out="Banco Middlware",
)
# reduzir o mapping para os campos que existem data_fields
mapping = {k: v for k, v in mapping.items() if k in data_fields}

print("\nMapping:", mapping)

print("converted to: Banco Middlware")
# in_fields = list(mapping.keys())
# print("\nin_fields:", in_fields)
df = df.rename(columns=mapping)

out_fields = [
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
df = df[out_fields]
print(df)
# print(df[out_fields])

# convert type column xid_equip to string
df["xid_equip"] = df["xid_equip"].astype(str)

# remover os xid_equip com valores nulos ou vazios
df = df[df["xid_equip"].notna() & df["xid_equip"].str.strip().astype(bool)]

# Conectar ao banco SQLite
print("\n\tconfigs.sqlite_db_path", configs.sqlite_db_path)
conn = sqlite3.connect(configs.sqlite_db_path)
cursor = conn.cursor()

# Criar tabela (se não existir)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS "EQP_MODBUS_IP" (
        xid_equip VARCHAR NOT NULL, 
        xid_gateway VARCHAR, 
        fabricante VARCHAR,
        modelo VARCHAR, 
        type VARCHAR, 
        sap_id VARCHAR, 
        enabled BOOLEAN, 
        "updatePeriodType" VARCHAR, 
        "maxReadBitCount" INTEGER, 
        "maxReadRegisterCount" INTEGER, 
        "maxWriteRegisterCount" INTEGER, 
        host VARCHAR, 
        port INTEGER, 
        retries INTEGER, 
        timeout INTEGER, 
        "updatePeriods" INTEGER, 
        PRIMARY KEY (xid_equip)
    );
"""
)

db_table = "EQP_MODBUS_IP"  # Nome da tabela no banco de dados

# 1. Obter os dados atuais da tabela SQLite
df_sqlite = pd.read_sql_query(f"SELECT * FROM {db_table}", conn)

# 2. Identificar registros novos, atualizados e a serem removidos

primary_key = "xid_equip"  # Definir a chave primária

df_novos = df[~df[primary_key].isin(df_sqlite[primary_key])]  # Registros novos (INSERT)
df_comuns = df[
    df[primary_key].isin(df_sqlite[primary_key])
]  # Registros existentes (UPDATE)
ids_df = set(df[primary_key])  # Conjunto de PKs do DataFrame
ids_sqlite = set(df_sqlite[primary_key])  # Conjunto de PKs do SQLite
ids_remover = ids_sqlite - ids_df  # Registros a remover (DELETE)

# 3. Remover registros que não estão no DataFrame
if ids_remover:
    query = f"DELETE FROM {db_table} WHERE {primary_key} IN (\"{'","'.join(map(str, ids_remover))}\")"
    print(f"\n\tquery: {query}")
    cursor.execute(query)
    print(f"\n\tRemovidos {len(ids_remover)} registros.")

# 4. Atualizar registros existentes
if not df_comuns.empty:
    # Criar uma tabela temporária com os dados do DataFrame
    df_comuns.to_sql(db_table, conn, if_exists="replace", index=False)
    print(f"\n\tAtualizados {len(df_comuns)} registros.")

# 5. Inserir novos registros
if not df_novos.empty:
    df_novos.to_sql(db_table, conn, if_exists="append", index=False)
    print(f"\n\tInseridos {len(df_novos)} novos registros.")

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Atualização concluída!")
