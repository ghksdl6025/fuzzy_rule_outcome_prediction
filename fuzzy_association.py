import pandas as pd
from itertools import combinations
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)

def divide_label(df):
    print(set(df['Label']))
    label_dict= {}
    for x in set(df['Label']): label_dict['Label_'+str(int(x))]  =[]
    for l in list(df['Label']):
        if int(l) == 1:
            label_dict['Label_1'].append(1)
            label_dict['Label_0'].append(0)
        elif int(l) == 0:
            label_dict['Label_1'].append(0)
            label_dict['Label_0'].append(1)
    
    df['Label_1'] = label_dict['Label_1']
    df['Label_0'] = label_dict['Label_0']
    df = df.drop(columns=['Label'],axis=1)
    
    return df
if __name__ =='__main__':
    df = pd.read_csv('./fuzzyified_eventlog.csv')
    dft = divide_label(df)
    dft = dft.drop(columns=['Case ID'],axis=1)
    label1rule = dft[dft['Label_1']==1].drop(columns=['Label_0'],axis=1)
    label0rule = dft[dft['Label_0']==1].drop(columns=['Label_1'],axis=1)
    
    taget_candidate = [x for x in list(combinations(label1rule,2)) if 'Label_1' in x]
    
    for k in range(len(label1rule)):
        print()