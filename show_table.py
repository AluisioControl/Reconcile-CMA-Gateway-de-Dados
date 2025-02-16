import pandas as pd
import json

with open('data.json') as f:
    data = f.read()

data = json.loads(data)

print(data)
df = pd.DataFrame(data)

print(df)
df.to_csv('output.csv')