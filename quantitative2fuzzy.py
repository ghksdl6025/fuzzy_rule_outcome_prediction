import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
import math
import sys
pd.set_option('display.max_columns',20)
sys.path.insert(0,'./Utils/')
import get_membership

def normalize_atts(df,att,prefix,method):
    '''
    Slice event log by prefix length and normalize target attributes in min max scaling which has range [0,1]

    Parameters
    ----------
    df : Dataframe 
        that used in this fundction
    atts : list
        list that contains attributes to normalize
    prefix : int
        Prefix length for slicing event log that all cases are longer than prefix length.
    In this sample case, only timestamp is used to generate duration and cumulative duration.

    method : str
        Which method to normalize (Minmax, Robust)
    Returns
    ----------
    Dataframe with case id, duration, cumulative duration, and label. 
    '''
    df = df.rename(columns={'case_id':'Case ID','timestamp':'Complete Timestamp'})
    df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'])
    groups = df.groupby('Case ID')
    casegroup = []
    quantitativenames = set()
    for caseid,group in groups:
        if len(group) >prefix:
            group = group.sort_values(by='Complete Timestamp')
            timelist = list(group['Complete Timestamp'])[:prefix]
            label = set(group['Label']).pop()
            case_outcome = {'Case ID':caseid, 'Label':label}
            duration_index={}
            cumduration_index={}

            for t in range(0, len(timelist)):
                if t ==0:

                    pass
                else:        
                    duration_index['Duration_'+str(t+1)] = (timelist[t]-timelist[t-1]).total_seconds()
                    cumduration_index['Cumduration_'+str(t+1)] = (timelist[t]-timelist[0]).total_seconds()
                    quantitativenames.add('Duration_'+str(t+1))
                    quantitativenames.add('Cumduration_'+str(t+1))

            case_outcome.update(duration_index)
            case_outcome.update(cumduration_index)
            casegroup.append(pd.DataFrame.from_dict([case_outcome]))
    dfn = pd.concat(casegroup)
    dfn = dfn.fillna(0)
    

    if method =='Normalize':
        for att in quantitativenames:
            target_att = list(dfn[att])
            target_mean = np.mean(target_att)
            target_std = np.std(target_att)
            target_att = [(x-target_mean)/target_std for x in target_att]
            
            dfn[att] = target_att

    elif method =='SigmoidNormalize':
        for att in quantitativenames:
            target_att = list(dfn[att])
            target_mean = np.mean(target_att)
            target_std = np.std(target_att)
            target_att = [(x-target_mean)/target_std for x in target_att]
            normalized = [1/(1+np.exp(-x)) for x in target_att]
            normalized = np.round_(normalized,5)
            dfn[att] = normalized
    dfn = dfn.reset_index(drop=True)
    return dfn ,quantitativenames

def generate_membership_label(membership_number):
    '''
    Custom function to convert membership label from generate_membership_label to preferred names

    Parameters
    ----------
    membership_number : int
        Number of membership class to make preferred names
    
    Returns
    ----------
    Dictionary which has key as membership label to change and value as preferred name
    '''
    membership_label ={}
    midpoint = (1+(membership_number//2))
    for m in range(1,membership_number+1):
        if m < midpoint:
            label_name = abs(midpoint -m)* 'S'
        elif m == midpoint:
            label_name = 'M'
        elif m > midpoint:
            label_name = abs(midpoint -m)* 'L'
        
        membership_label['Interval_'+str(m)] = label_name 
    return membership_label


def time2fuzzification(df,membership_number,quantitative_atts):
    '''
    Get dataframe with quantitative attributes and fuzzify items and return dataframe with fuzzified itemsets.
    (In this case only time related attributes are used, duration and cumulative duration)

    Parameters
    ----------
    df : pandas dataframe
        Dataframe wtih quantitative attributes
    membership_number : int
        Number of membership class to make preferred names
    
    Returns
    ----------
    Dataframe with fuzzified itemsets
    '''
    membership_label = generate_membership_label(membership_number)    
    membership_function = get_membership.membership_f(get_membership.uniform_plotting_membership(membership_number))
    locs = [x[0] for x in get_membership.uniform_plotting_membership(membership_number).values()]
    alloc =[]
    for loc in locs:
        alloc +=loc
    minloc = min(alloc)    
    maxloc = max(alloc)
    membership_names = list(membership_function.keys())

    for att in quantitative_atts:
        for row in range(len(df)):
            dur = df.loc[row,att]
            fuzzy_set ={}
            mlabel_prefix = att+'_'
            if dur <= minloc:
                fuzzy_set[mlabel_prefix+membership_label[membership_names[0]]] = 1.0
            elif dur > maxloc:
                fuzzy_set[mlabel_prefix+membership_label[membership_names[-1]]] = 1.0
            else:
                for membership in membership_names:
                    for pos, interval in enumerate(membership_function[membership]['Split_interval']):
                        if interval[1] >= dur > interval[0]:
                            membership_value = membership_function[membership]['Value'][pos][0] * dur + membership_function[membership]['Value'][pos][1]
                            fuzzy_set[mlabel_prefix+membership_label[membership]] = membership_value
            for t in fuzzy_set.keys():
                df.loc[row,t] = fuzzy_set[t]
    
    df = df.drop(columns=list(quantitative_atts),axis=1)
    df = df.fillna(0)

    return df

if __name__ =='__main__':
    prefix = 3
    membership_number = 5
    # df = pd.read_csv('../special_topics/data/hospital_billing.csv')

    df = pd.read_csv('../new paper/sepsis/Sepsis Cases_pre.csv')
    df = pd.read_csv('../new paper/bpic2015/ltl1/BPIC15_1prep.csv')
    normalized_time_df,quantitative_atts =normalize_atts(df,'Complete Timestamp',prefix,'SigmoidNormalize')    
    fuzzified_df = time2fuzzification(normalized_time_df,membership_number,quantitative_atts)
    fuzzified_df.to_csv('./bpic2015_fuzzified.csv',index=False)
