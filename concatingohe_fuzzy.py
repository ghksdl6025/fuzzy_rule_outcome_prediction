import pandas as pd

fuzzified_df = pd.read_csv('./bpic2015_fuzzified.csv')
ohe_df = pd.read_csv('../new paper/bpic2015/ltl1/bpic2015_1/indexbase/prefix5/simple_timediscretize/ARMinput_preprocessed.csv')
# print(fuzzified_df.columns.values)
droplist = []
for t in list(ohe_df.columns.values):
    if 'Time' in t or 'Duration' in t or 'Cumduration' in t:
        droplist.append(t)
ohe_df = ohe_df.drop(columns=droplist,axis=1)
dfn = pd.merge(fuzzified_df,ohe_df,on='Case ID')
# dfn.to_csv('./concatanated_fuzzy_tx.csv',index=False)
print()
label1df = dfn[dfn['Label_1']==1]
label0df = dfn[dfn['Label_0']==1]

meaningfulcol = set()
for col in dfn.columns.values:
    if len([x for x in list(label1df[col]) if x != 0]) >= int(len(label1df)*0.1):
        meaningfulcol.add(col)

    if len([x for x in list(label0df[col]) if x != 0]) >= int(len(label0df)*0.1):
        meaningfulcol.add(col)

for t in list(meaningfulcol):
    if 'Nan' in t:
        meaningfulcol.remove(t)
dfn = dfn.loc[:,list(meaningfulcol)]


dfn.to_csv('./bpic2015_concatanated_fuzzy_tx.csv')
