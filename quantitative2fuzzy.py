
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
import math
import sys

sys.path.insert(0,'./Utils/')
import get_membership
# df = pd.read_csv('../new paper/bpic2015/ltl1/BPIC15_1prep.csv')

def normalize_atts(df,att,prefix):
    df = df.rename(columns={'case_id':'Case ID','timestamp':'Complete Timestamp'})
    df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'])
    groups = df.groupby('Case ID')
    caseidlist = []
    durationlist= []
    cumdurationlist = []
    labellist= []
    for caseid,group in groups:
        if len(group) >prefix:
            group = group.sort_values(by='Complete Timestamp')
            timelist = list(group['Complete Timestamp'])[:prefix]
            label = set(group['Label']).pop()
            for t in range(0, len(timelist)):
                caseidlist.append(caseid)
                labellist.append(label)
                if t ==0:
                    durationlist.append(0)
                    cumdurationlist.append(0)
                else:        
                    durationlist.append((timelist[t]-timelist[t-1]).total_seconds())
                    cumdurationlist.append((timelist[t]-timelist[0]).total_seconds())
        

    t = [x/max(durationlist) for x in durationlist]
    t = np.round_(t,5)    
    durationlist  =[float(x) for x in t] 
    
    # t = preprocessing.scale(cumdurationlist)
    t = [x/max(cumdurationlist) for x in cumdurationlist]
    t = np.round_(t,5)
    cumdurationlist  =[float(x) for x in t] 
    df = pd.DataFrame(columns=['Case ID','Duration','Cumduration'])
    df['Case ID'] = caseidlist
    df['Duration'] = durationlist
    df['Cumduration'] = cumdurationlist
    df['Label'] = labellist
    return df

def generate_membership_label(membership_number):

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



def time2fuzzification(df,_):
    pass

if __name__ =='__main__':
    prefix = 3
    membership_number = 5
    # df = pd.read_csv('../special_topics/data/hospital_billing.csv')
    df = pd.read_csv('../new paper/bpic2011/ltl1/bpic2011prep.csv')
    
    normalized_time_df =normalize_atts(df,'Complete Timestamp',prefix)    
    membership_label = generate_membership_label(membership_number)    
    membership_function = get_membership.membership_f(get_membership.uniform_plotting_membership(membership_number))
    
    locs = [x[0] for x in get_membership.uniform_plotting_membership(membership_number).values()]
    alloc =[]
    for loc in locs:
        alloc +=loc
    minloc = min(alloc)    
    maxloc = max(alloc)
    membership_names = list(membership_function.keys())


    membership_labelset = set()
    groups = normalized_time_df.groupby('Case ID')
    fuzzy_set_list = []
    for caseid, group in groups:
        duration = list(group['Duration'])
        label = set(group['Label']).pop()
        fuzzy_set = {}

        #Fuzzify duration
        for pos,dur in enumerate(duration):
            mlabel_prefix = 'Duration_'+str(pos+1)+'_'
            if dur <= minloc:
                fuzzy_set[mlabel_prefix+membership_label[membership_names[0]]] = 1.0
            elif dur > maxloc:
                fuzzy_set[mlabel_prefix+membership_label[membership_names[-1]]] = 1.0
            else:
                for membership in membership_names:
                    for pos, interval in enumerate(membership_function[membership]['Split_interval']):
                        if interval[1] >= dur > interval[0]:
                            membership_value = membership_function[membership]['Value'][pos][0] * dur + membership_function[membership]['Value'][pos][1]
                            totalmembership_value = (mlabel_prefix+membership_label[membership], membership_value)
                            fuzzy_set[mlabel_prefix+membership_label[membership]] = membership_value
            for t in fuzzy_set.keys(): membership_labelset.add(t)

        #Fuzzify cumduration
        duration = list(group['Cumduration'])
        for pos,dur in enumerate(duration):
            mlabel_prefix = 'Cumuration'+str(pos+1)+'_'
            if dur <= minloc:
                fuzzy_set[mlabel_prefix+membership_label[membership_names[0]]] = 1.0
            elif dur > maxloc:
                fuzzy_set[mlabel_prefix+membership_label[membership_names[-1]]] = 1.0
            else:
                for membership in membership_names:
                    for pos, interval in enumerate(membership_function[membership]['Split_interval']):
                        if interval[1] >= dur > interval[0]:
                            membership_value = membership_function[membership]['Value'][pos][0] * dur + membership_function[membership]['Value'][pos][1]
                            totalmembership_value = (mlabel_prefix+membership_label[membership], membership_value)
                            fuzzy_set[mlabel_prefix+membership_label[membership]] = membership_value
            for t in fuzzy_set.keys(): membership_labelset.add(t)

        fuzzy_set['Case ID'] = caseid
        fuzzy_set['Label'] = label
        fuzzy_set_list.append(fuzzy_set)

    df_list =[]
    dfk = pd.DataFrame.from_dict(fuzzy_set_list,orient='columns')
    dfk = dfk.fillna(0)
    dfk.to_csv('./fuzzyified_eventlog.csv',index=False)

