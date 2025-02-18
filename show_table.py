import sqlite3
import pandas as pd
import json

# Ler o arquivo JSON
with open("data.json") as f:
    data = json.load(f)

# Criar um DataFrame
df = pd.DataFrame(data)

# Conectar ao banco SQLite (ou criar um novo se não existir)
conn = sqlite3.connect("dados.db")

# Salvar o DataFrame no banco, criando a tabela "dados" (ou sobrescrevendo se já existir)
df.to_sql("dados", conn, if_exists="replace", index=False)

# Fechar a conexão
conn.close()

print(df)
df.to_csv("output.csv")
