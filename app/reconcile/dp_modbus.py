import json
import os

# from app.settings import configs
import sqlite3

import pandas as pd

from app.logger import logger
from app.translator import (
    map_fields,
    registradores_modbus_translate,
    sensores_modbus_translate,
    translate,
)

sqlite_db_path = os.environ.get("SQLITE_MIDDLEWARE_PATH")


# Load hardware data from JSON files
with open("./data.json") as f:
    data = json.load(f)

data_fields = list(data[0].keys())
df = pd.DataFrame(data)

# Filtrar únicos pela coluna id_reg_mod
df = df.drop_duplicates(subset=["id_reg_mod"])

# convert col id_reg_mod to string
df["id_reg_mod"] = df["id_reg_mod"].astype(str)

# Filter por id_reg_mod não nulo ou vazio
df = df[df["id_reg_mod"].notnull() & (df["id_reg_mod"] != "")]


mapping = map_fields(
    base_translate=registradores_modbus_translate + sensores_modbus_translate,
    base_in="Lógica de montagem",
    base_out="Banco Middlware",
)
# Reduzir o mapping para os campos que existem em data_fields
# mapping = {k: v for k, v in mapping.items() if k in data_fields}
df = translate(df, mapping)

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
df = df[out_fields]  # Selecionar apenas os campos de saída
# remover coluna duplicada por conta da tradução
df = df.loc[:, ~df.columns.duplicated()]


# Conectar ao banco SQLite
logger.info(f"Conectando ao banco de dados SQLite em {sqlite_db_path}")
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()
db_table = "DP_MODBUS_IP"  # Nome da tabela no banco de dados

# Criar tabela (se não existir)
cursor.execute(
    f"""
    CREATE TABLE IF NOT EXISTS "{db_table}" (
        xid_sensor VARCHAR NOT NULL, 
        xid_equip VARCHAR, 
        range VARCHAR, 
        "modbusDataType" VARCHAR, 
        additive INTEGER, 
        "offset" INTEGER, 
        bit INTEGER, 
        multiplier FLOAT, 
        "slaveId" INTEGER, 
        enabled BOOLEAN, 
        nome VARCHAR, 
        tipo VARCHAR, 
        classificacao VARCHAR, 
        PRIMARY KEY (xid_sensor)
    );
"""
)


# 1. Obter os dados atuais da tabela SQLite
df_sqlite = pd.read_sql_query(f"SELECT * FROM {db_table}", conn)

print(len(df_sqlite), "registros no banco de dados.")

# 2. Identificar registros novos, atualizados e a serem removidos
primary_key = "xid_sensor"  # Definir a chave primária


df_novos = df[~df[primary_key].isin(df_sqlite[primary_key])]  # Registros novos (INSERT)
df_comuns = df[
    df[primary_key].isin(df_sqlite[primary_key])
]  # Registros existentes (UPDATE)
ids_df = set(df[primary_key])  # Conjunto de PKs do DataFrame
ids_sqlite = set(df_sqlite[primary_key])  # Conjunto de PKs do SQLite
ids_remover = ids_sqlite - ids_df  # Registros a remover (DELETE)

print(f"\nRegistros no DataFrame: {len(df)}")
print(f"\tNovos: {len(df_novos)}")
print(f"\tAtualizar: {len(df_comuns)}")
print(f"\tRemover: {len(ids_remover)}")

print("Realizado:")
# 3. Remover registros que não estão no DataFrame
if ids_remover:
    query = f"DELETE FROM {db_table} WHERE {primary_key} IN (\"{'","'.join(map(str, ids_remover))}\")"
    print("\n\tRemovidos", len(ids_remover), "registros.")

    cursor.execute(query)

# 4. Atualizar registros existentes
# Update existing records
if not df_comuns.empty:
    update_count = 0
    for index, row in df_comuns.iterrows():
        update_query = f"""
            UPDATE {db_table} SET
                xid_equip = ?,
                range = ?,
                modbusDataType = ?,
                additive = ?,
                offset = ?,
                bit = ?,
                multiplier = ?,
                slaveId = ?,
                enabled = ?,
                nome = ?,
                tipo = ?,
                classificacao = ?
            WHERE xid_sensor = ?
        """
        # Convert values to Python scalar types explicitly
        values = (
            str(row["xid_equip"]) if pd.notnull(row["xid_equip"]) else None,
            str(row["range"]) if pd.notnull(row["range"]) else None,
            str(row["modbusDataType"]) if pd.notnull(row["modbusDataType"]) else None,
            int(row["additive"]) if pd.notnull(row["additive"]) else None,
            int(row["offset"]) if pd.notnull(row["offset"]) else None,
            int(row["bit"]) if pd.notnull(row["bit"]) else None,
            float(row["multiplier"]) if pd.notnull(row["multiplier"]) else None,
            int(row["slaveId"]) if pd.notnull(row["slaveId"]) else None,
            bool(row["enabled"]) if pd.notnull(row["enabled"]) else None,
            str(row["nome"]) if pd.notnull(row["nome"]) else None,
            str(row["tipo"]) if pd.notnull(row["tipo"]) else None,
            str(row["classificacao"]) if pd.notnull(row["classificacao"]) else None,
            str(row["xid_sensor"]) if pd.notnull(row["xid_sensor"]) else None,
        )
        cursor.execute(update_query, values)
        update_count += 1
    print("\n\tAtualizados", update_count, "registros.")

# 5. Inserir novos registros
if not df_novos.empty:
    df_novos.to_sql(db_table, conn, if_exists="append", index=False)
    print("\n\tInseridos", len(df_novos), "novos registros.")

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()

print("\n\tFim.")
