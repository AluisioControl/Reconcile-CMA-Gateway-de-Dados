import pandas as pd
import json

with open('data.json') as f:
    data = f.read()

data = json.loads(data)

print(data[0])
df = pd.DataFrame(data[0])

print(df)
df.to_csv('output.csv')