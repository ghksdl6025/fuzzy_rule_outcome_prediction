import pandas as pd

fuzzified_df = pd.read_csv('./fuzzified.csv')
ohe_df = pd.read_csv('../new paper/sepsis/rule1/indexbase/prefix5/simple_timediscretize/ARMinput_preprocessed.csv')
# print(fuzzified_df.columns.values)
droplist = []
for t in list(ohe_df.columns.values):
    if 'Time' in t or 'Duration' in t or 'Cumduration' in t:
        droplist.append(t)
ohe_df = ohe_df.drop(columns=droplist,axis=1)
dfn = pd.merge(fuzzified_df,ohe_df,on='Case ID')
dfn.to_csv('./concatanated_fuzzy_tx.csv',index=False)