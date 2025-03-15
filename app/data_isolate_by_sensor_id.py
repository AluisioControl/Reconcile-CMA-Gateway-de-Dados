import json

import pandas as pd

# Ler o arquivo JSON
with open("data.json") as f:
    data = json.load(f)

# Criar um DataFrame
df = pd.DataFrame(data)

# Agrupar os dados pelo id do sensor (id_sen)
grouped = df.groupby("id_sen")

# Salvar cada grupo em um arquivo JSON
for sensor_id, group in grouped:
    group.to_json(f"data_by_sensor_{sensor_id}.json", orient="records")
    print(f"Salvo sensor_{sensor_id}.json")
