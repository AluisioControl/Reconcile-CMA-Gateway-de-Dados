from app.reconcile import dp_modbus, eqp_modbus, eqp_tags, gateway

# from app.reconcile import dp_tags

# import json
# import sqlite3

# import pandas as pd
# from settings import configs

# with open("./data.json") as f:
#     data = json.load(f)

# # DataFrame dos dados coletados
# df = pd.DataFrame(data)

# # Conectar ao banco SQLite
# conn = sqlite3.connect(configs.sqlite_db_path)
# cursor = conn.cursor()

# # Criar tabela (se não existir)
# cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS pessoas (
#         id INTEGER PRIMARY KEY,
#         nome TEXT,
#         idade INTEGER
#     )
# """
# )

# # 1. Obter os dados atuais da tabela SQLite
# df_sqlite = pd.read_sql_query("SELECT * FROM pessoas", conn)

# # 2. Identificar registros novos, atualizados e a serem removidos
# # Chave primária é 'id'
# df_novos = df[~df["id"].isin(df_sqlite["id"])]  # Registros novos (INSERT)
# df_comuns = df[df["id"].isin(df_sqlite["id"])]  # Registros existentes (UPDATE)
# ids_df = set(df["id"])
# ids_sqlite = set(df_sqlite["id"])
# ids_remover = ids_sqlite - ids_df  # Registros a remover (DELETE)

# # 3. Inserir novos registros
# if not df_novos.empty:
#     df_novos.to_sql("pessoas", conn, if_exists="append", index=False)
#     print(f"Inseridos {len(df_novos)} novos registros.")

# # 4. Atualizar registros existentes
# if not df_comuns.empty:
#     # Criar uma tabela temporária com os dados do DataFrame
#     df_comuns.to_sql("temp_pessoas", conn, if_exists="replace", index=False)

#     # Atualizar a tabela principal com base na tabela temporária
#     cursor.execute(
#         """
#         UPDATE pessoas
#         SET nome = (SELECT nome FROM temp_pessoas WHERE temp_pessoas.id = pessoas.id),
#             idade = (SELECT idade FROM temp_pessoas WHERE temp_pessoas.id = pessoas.id)
#         WHERE id IN (SELECT id FROM temp_pessoas)
#     """
#     )
#     print(f"Atualizados {len(df_comuns)} registros.")

#     # Remover a tabela temporária
#     cursor.execute("DROP TABLE temp_pessoas")

# # 5. Remover registros que não estão no DataFrame
# if ids_remover:
#     cursor.execute(
#         f"DELETE FROM pessoas WHERE id IN ({','.join(map(str, ids_remover))})"
#     )
#     print(f"Removidos {len(ids_remover)} registros.")

# # Confirmar as alterações e fechar a conexão
# conn.commit()
# conn.close()

# print("Atualização concluída!")
