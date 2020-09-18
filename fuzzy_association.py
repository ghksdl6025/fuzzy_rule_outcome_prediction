import pandas as pd
from itertools import combinations
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
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


def fuzzy_frequent_itemset_mining(df,target_label,min_supp):
    '''
    Calcualting itemset frequency 

    Parameters
    ----------
    df : pandasd dataframe
        Pandas dataframe with fuzzified itemset including one hot vectors
    
    target_label : string
        Name of label which is one of columns in df ex) 'Label_1' or 'Label_0'
    
    min_supp : float
        Minimum support thershold to filter itemset which has support level score above than min_supp.

    Returns 
    ----------
    Pandas dataframe which has two column, itemset and Support 
    '''
    dfrule_value = df.values.tolist()
    dfcolumn = np.array(df.columns.values)
    
    itemset_frequency = {}
    print('Getting sub itemset for FIM')
    for pos,k in enumerate(dfrule_value):
       
        print(pos,'/', len(dfrule_value), len(itemset_frequency))
        rowposition = [x for x in range(len(k)) if k[x] != 0]
        itemset = dfcolumn[rowposition]
        itemset = itemset[itemset != target_label]
        for x in range(1,len(itemset)+1):
            itemset_group =set()

            for item in list(combinations(itemset,x)):
                item = set(item)
                item.add(target_label)
                itemset_group.add(frozenset(item))
        
            for item in itemset_group:
                frequency_score = 0
                if item in itemset_frequency.keys():
                    pass
                else:
                    for k in dfrule_value:
                        rowposition = [x for x in range(len(k)) if k[x] != 0]
                        transaction_items = dfcolumn[rowposition]
                        if item.issubset(transaction_items):
                            dfcolumn =  np.array(dfcolumn)
                            columindex = [x for x in range(len(dfcolumn)) if dfcolumn[x] in item]
                            frequency_score += min(np.array(k)[columindex])
                    
                    if frequency_score/len(dfrule_value) >= min_supp:
                        itemset_frequency[item] = round(frequency_score/len(dfrule_value),5)
    print('Calculating support of association rules')
    
    itemsets = list(itemset_frequency.keys())
    itemset_supp = list(itemset_frequency.values())
    df = pd.DataFrame(columns = ['Itemset','Support'])
    df['Itemset'] = itemsets
    df['Support'] = itemset_supp

    return df


if __name__ =='__main__':
    df = pd.read_csv('./concatanated_fuzzy_tx.csv')
    dft = divide_label(df)
    dft = dft.drop(columns=['Case ID'],axis=1)
    label1rule = dft[dft['Label_1']==1].drop(columns=['Label_0'],axis=1)
    label0rule = dft[dft['Label_0']==1].drop(columns=['Label_1'],axis=1)
    
    min_supp = 0.95
    target_label = 'Label_1'
    df = fuzzy_frequent_itemset_mining(label1rule, target_label, min_supp)
    association_rule_pos= []
    supportlist = list(df['Support'])
    for pos,x in enumerate(list(df['Itemset'])):
        if target_label in x:
            association_rule_pos.append(pos)
    association_rule_df_1 = df.loc[association_rule_pos,:]            
    antecedent_label1 = []
    for x in list(association_rule_df_1['Itemset']):
        t = list(x)
        t.remove('Label_1')
        antecedent_label1.append(sorted(t))
    
    # association_rule_df.to_csv('./association_rule_df_label1.csv',index=False)

    min_supp = 0.95
    target_label = 'Label_0'
    df = fuzzy_frequent_itemset_mining(label0rule, target_label, min_supp)
    association_rule_pos= []
    supportlist = list(df['Support'])
    for pos,x in enumerate(list(df['Itemset'])):
        if target_label in x:
            association_rule_pos.append(pos)
    association_rule_df_0 = df.loc[association_rule_pos,:]            
    antecedent_label0 = []
    for x in list(association_rule_df_0['Itemset']):
        t = list(x)
        t.remove('Label_0')
        antecedent_label0.append(sorted(t))
    
    commonantecedent = []
    for common in antecedent_label1:
        if common in antecedent_label0:
            commonantecedent.append(common)
    
    antecedent_label1 = [x for x in antecedent_label1 if x not in commonantecedent]
    antecedent_label0 = [x for x in antecedent_label0 if x not in commonantecedent]
    print(antecedent_label1)
    print(antecedent_label0)

    # association_rule_df.to_csv('./association_rule_df_label0.csv',index=False)

    
