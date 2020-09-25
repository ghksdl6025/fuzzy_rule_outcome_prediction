import sys
import csv
sys.path.insert(0,'./fuzzy-association-rule-mining-master/')

import pandas as pd
file = './bpic2015_concatanated_fuzzy_tx.csv'

support = 0.7
confidence = 0.7

df =  pd.read_csv(file)

df = df.drop(columns=['Case ID'],axis=1)
label1 = df[df['Label_1']==1]
label0 = df[df['Label_0']==1]
length = len(label1)
collist =[]
for col in list(label1.columns.values):
    if sum(label1[col])/length >=0.7:
        collist.append(col)
label1 = label1.loc[:,collist]
print(label1.head)
print(label1.columns.values)