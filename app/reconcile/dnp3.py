import json
import sqlite3

import pandas as pd

from app.getters.gateway import parse_gateway_data
from app.settings import configs
from app.translator import gateway_translate, map_fields, translate

with open("./gateways.json") as f:
    data = [parse_gateway_data(gw) for gw in json.load(f)]

# DataFrame dos dados coletados
print("Carregando dados...")
df = pd.DataFrame(data)

# traduzir os campos do json para o banco de dados
base_in = "Lógica de montagem"
base_out = "Gateway de Dados"
mapping = map_fields(
    base_translate=gateway_translate, base_in=base_in, base_out=base_out
)

# print o mapping: de -> para
print(f"\nTradução\n{base_in} para {base_out}")
for k, v in mapping.items():
    print(f"\t{k} -> {v}")

# traduzir os campos
df = translate(df, mapping)
print("\nDados traduzidos\n", df)

# Conectar ao banco SQLite
print("\n\tconfigs.sqlite_db_path", configs.sqlite_db_path)
conn = sqlite3.connect(configs.sqlite_db_path)
cursor = conn.cursor()

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
df_sqlite = pd.read_sql_query("SELECT * FROM CMA_GD", conn)

# 2. Identificar registros novos, atualizados e a serem removidos

primary_key = "xid_gateway"  # Definir a chave primária

df_novos = df[~df[primary_key].isin(df_sqlite[primary_key])]  # Registros novos (INSERT)
df_comuns = df[
    df[primary_key].isin(df_sqlite[primary_key])
]  # Registros existentes (UPDATE)
ids_df = set(df[primary_key])  # Conjunto de PKs do DataFrame
ids_sqlite = set(df_sqlite[primary_key])  # Conjunto de PKs do SQLite
ids_remover = ids_sqlite - ids_df  # Registros a remover (DELETE)

db_table = "CMA_GD"  # Nome da tabela no banco de dados

# 3. Remover registros que não estão no DataFrame
if ids_remover:
    query = f"DELETE FROM {db_table} WHERE {primary_key} IN ({'","'.join(map(str, ids_remover))})"
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
