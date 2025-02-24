import json
import sqlite3

import pandas as pd

from app.getters.gateway import parse_gateway_data
from app.settings import configs
from app.translator import gateway_translate, map_fields, translate

with open("./gateways.json") as f:
    data = [parse_gateway_data(gw) for gw in json.load(f)]

# DataFrame dos dados coletados
df = pd.DataFrame(data)

# traduzir os campos do json para o banco de dados
base_in = "Lógica de montagem"
base_out = "Gateway de Dados"
mapping = map_fields(
    base_translate=gateway_translate, base_in=base_in, base_out=base_out
)

# traduzir os campos
df = translate(df, mapping)

# Conectar ao banco SQLite
conn = sqlite3.connect(configs.sqlite_db_path)
cursor = conn.cursor()
db_table = "CMA_GD"  # Nome da tabela no banco de dados

# Criar tabela (se não existir)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS "CMA_GD" (
        xid_gateway VARCHAR NOT NULL, 
        subestacao VARCHAR, 
        regional VARCHAR, 
        host VARCHAR, 
        status BOOLEAN, 
        PRIMARY KEY (xid_gateway)
    );
"""
)

# 1. Obter os dados atuais da tabela SQLite
df_sqlite = pd.read_sql_query(f"SELECT * FROM {db_table}", conn)

# 2. Identificar registros novos, atualizados e a serem removidos

primary_key = "xid_gateway"  # Definir a chave primária

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

print("\nRealizado:")
# 3. Remover registros que não estão no DataFrame
if ids_remover:
    query = f"DELETE FROM {db_table} WHERE {primary_key} IN (\"{'","'.join(map(str, ids_remover))}\")"
    print("\n\tquery:", query)
    cursor.execute(query)
    print(f"\tRemovidos {len(ids_remover)} registros.")

# 4. Atualizar registros existentes
if not df_comuns.empty:
    # Criar uma tabela temporária com os dados do DataFrame
    df_comuns.to_sql(db_table, conn, if_exists="replace", index=False)
    print(f"\tAtualizados {len(df_comuns)} registros.")

# 5. Inserir novos registros
if not df_novos.empty:
    df_novos.to_sql(db_table, conn, if_exists="append", index=False)
    print(f"\n\tInseridos {len(df_novos)} novos registros.")

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()

print("\nAtualização concluída!")
