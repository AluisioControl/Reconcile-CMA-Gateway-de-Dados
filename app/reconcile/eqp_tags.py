import json
import sqlite3
import pandas as pd
from app.settings import configs
from app.translator import all_translates, map_fields, translate
from app.utils.data import combine_primary_with_secondary

# Carregar dados do JSON
with open("./data.json") as f:
    data = json.load(f)

data_fields = list(data[0].keys())

df = pd.DataFrame(data)

df = df[['id_reg_mod','reg_mod_tags']]

# remover os id_reg_mod com valores nulos ou vazios
df = df[df['id_reg_mod'].notna() & df['id_reg_mod'].str.strip().astype(bool)]

# precisamos pegar o valor de reg_mod_tags que é um json e transformar em um DataFrame
combined_tags = []
df['reg_mod_tags'] = df['reg_mod_tags'].apply(lambda x: json.loads(x))
for index, row in df.iterrows():
    combined_tags += combine_primary_with_secondary({'id_reg_mod': row['id_reg_mod']}, row['reg_mod_tags'])

df_tags = pd.DataFrame(combined_tags)
mapping = {
    'id_reg_mod': 'xid_equip',
    'id': 'id',
    'name': 'nome',
    'value': 'valor'
}
df_tags.rename(columns=mapping, inplace=True)


# Conectar ao banco SQLite
print("\nconfigs.sqlite_db_path:", configs.sqlite_db_path)
conn = sqlite3.connect(configs.sqlite_db_path)
cursor = conn.cursor()

db_table = "EQP_TAGS"
# Criar tabela EQP_TAGS (se não existir)
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS "{db_table}" (
        id VARCHAR NOT NULL, 
        xid_equip VARCHAR, 
        nome VARCHAR, 
        valor VARCHAR, 
        PRIMARY KEY (id)
    );
""")

df_sqlite_eqp_tgas = pd.read_sql_query(f"SELECT * FROM {db_table}", conn)
primary_key = "id"

df_novas_tags = df_tags[~df_tags[primary_key].isin(df_sqlite_eqp_tgas[primary_key])]
df_tags_atuializar = df_tags[df_tags[primary_key].isin(df_sqlite_eqp_tgas[primary_key])]
ids_df_tags = set(df_tags[primary_key])
ids_sqlite_tags = set(df_sqlite_eqp_tgas[primary_key])
ids_remover_modbus = ids_sqlite_tags - ids_df_tags

print("Resumo:")
print(f"\tNovos registros: {len(df_novas_tags)}")
print(f"\tRegistros comuns: {len(df_tags_atuializar)}")
print(f"\tRegistros a remover: {len(ids_remover_modbus)}")

if ids_remover_modbus:
    query = f"DELETE FROM {db_table} WHERE {primary_key} IN (\"{'',''.join(map(str, ids_remover_modbus))}\")"
    cursor.execute(query)
    print(f"\n\tRemovidos {len(ids_remover_modbus)} registros de {db_table}.")

if not df_tags_atuializar.empty:
    for index, row in df_tags_atuializar.iterrows():
        cursor.execute(f"""
            UPDATE {db_table}
            SET xid_equip = ?, nome = ?, valor = ?
            WHERE id = ?
        """, (row['xid_equip'], row['nome'], row['valor'], row['id']))
    print(f"\n\tAtualizados {len(df_tags_atuializar)} registros em {db_table}.")

if not df_novas_tags.empty:
    try:
        df_novas_tags.to_sql(db_table, conn, if_exists="append", index=False)
        print(f"\n\tInseridos {len(df_novas_tags)} novos registros em {db_table}.")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao inserir registros: {e}")
        print("Dados problemáticos:")
        print(df_novas_tags)


# Confirmar alterações e fechar conexão
conn.commit()
conn.close()

print("Atualização concluída!")