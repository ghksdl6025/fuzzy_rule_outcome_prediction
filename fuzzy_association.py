import pandas as pd
from itertools import combinations
import numpy as np
import os
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

    length = len(df)
    collist =[]
    for col in list(df.columns.values):
        if sum(df[col])/length >=min_supp:
            collist.append(col)
    df = df.loc[:,collist]

    dfrule_value = df.values.tolist()
    dfcolumn = np.array(df.columns.values)
    registerd_items=set()
    itemset_frequency = {}
    rowposition_dict ={}
    for pos,k in enumerate(dfrule_value):
        rowposition = [x for x in range(len(k)) if k[x] != 0]
        rowposition_dict[pos] = rowposition
    print('Getting sub itemset for FIM')
    for pos,k in enumerate(dfrule_value):
        if pos % 10 ==0:
            print(pos,'/', len(dfrule_value))
        rowposition = rowposition_dict[pos]
        itemset = dfcolumn[rowposition]
        itemset = itemset[itemset != target_label]
        for x in range(1,len(itemset)+1):
            itemset_group =set()
            for item in list(combinations(itemset,x)):
                item = set(sorted(item))
                item.add(target_label)
                if frozenset(item) not in registerd_items:
                    itemset_group.add(frozenset(item))
                    registerd_items.add(frozenset(item))

            for item in itemset_group:
                frequency_score = 0
                for pos,k in enumerate(dfrule_value):
                    rowposition = rowposition_dict[pos]
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
    for rnd in range(0,1):
        for prefix in range(5,6):
            print('Prefix', prefix, 'Random',rnd)
            dirname = './bpic2015/rule1/prefix'+str(prefix)
            try:
                os.makedirs(dirname+'/rules')
            except:
                pass
            df = pd.read_csv(dirname+'/train_rndst'+str(rnd)+'.csv')
            # dft = divide_label(df)
            df = df.drop(columns=['Case ID','Label'],axis=1)
            label1rule = df[df['Label_1']==1].drop(columns=['Label_0'],axis=1)
            label0rule = df[df['Label_0']==1].drop(columns=['Label_1'],axis=1)
            
            min_supp = 0.7
            target_label = 'Label_1'
            df = fuzzy_frequent_itemset_mining(label1rule, target_label, min_supp)
            
            association_rule_pos= []        
            antecedent_label1 = []
            for x in list(df['Itemset']):
                t = list(x)
                t.remove(target_label)
                antecedent_label1.append(sorted(t))

            label1df = pd.DataFrame(columns=['Antecedents','Consequent','Support'])
            label1df['Antecedents'] = antecedent_label1
            label1df['Consequent'] = [target_label]*len(antecedent_label1)
            label1df['Support'] = df['Support']
            
            target_label = 'Label_0'
            df = fuzzy_frequent_itemset_mining(label0rule, target_label, min_supp)

            association_rule_pos= []
            antecedent_label0 = []
            for x in list(df['Itemset']):
                t = list(x)
                t.remove(target_label)
                antecedent_label0.append(sorted(t))

            label0df= pd.DataFrame(columns=['Antecedents','Consequent','Support'])
            label0df['Antecedents'] = antecedent_label0
            label0df['Consequent'] = [target_label]*len(antecedent_label0)
            label0df['Support'] = df['Support']

            commonantecedent = []
            for common in antecedent_label1:
                if common in antecedent_label0:
                    commonantecedent.append(common)
            
            antecedent_label1 = [x for x in antecedent_label1 if x not in commonantecedent]
            antecedent_label0 = [x for x in antecedent_label0 if x not in commonantecedent]

            uniqueposition0 = [pos for pos,x in enumerate(list(label0df['Antecedents'])) if x in antecedent_label0]
            uniqueposition1 = [pos for pos,x in enumerate(list(label1df['Antecedents'])) if x in antecedent_label1]
            
            label0df = label0df.iloc[uniqueposition0,:].reset_index(drop=True)
            label1df = label1df.iloc[uniqueposition1,:].reset_index(drop=True)


            label0df.to_csv(dirname+'/rules/association_rule_df_label0_rnd'+str(rnd)+'.csv',index=False)    
            label1df.to_csv(dirname+'/rules/association_rule_df_label1_rnd'+str(rnd)+'.csv',index=False)    



