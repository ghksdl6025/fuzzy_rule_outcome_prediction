import pandas as pd

df = pd.read_csv('./bpic2015_concatanated_fuzzy_tx.csv')
print(df.head)

recol = []
for col in df.columns.values:
    if 'Activity' in col or 'duration' in col or 'Duration' in col:
        recol.append(col)
recol.append('Label')
recol.append('Case ID')

df = df.loc[:,recol]
df.to_csv('./bpic2015_concatanated_fuzzy_tx_short.csv')