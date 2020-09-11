import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
import math
import sys

sys.path.insert(0,'./Utils/')
import plot_membership
# df = pd.read_csv('../new paper/bpic2015/ltl1/BPIC15_1prep.csv')

def normalize_atts(df,att,prefix):
    df = df.rename(columns={'case_id':'Case ID','timestamp':'Complete Timestamp'})
    df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'])
    groups = df.groupby('Case ID')
    time_by_index={}
    for _,group in groups:
        duration = [0]
        cum_duration = [0]
        group = group.sort_values(by='Complete Timestamp')
        timelist = list(group['Complete Timestamp'])

        time_by_index['Time'+'_'+'0'] = {'duration':[0],'cum_duration':[0]}
        for t in range(1, len(timelist)):
            if 'Time'+'_'+str(t) not in list(time_by_index.keys()):
                time_by_index['Time'+'_'+str(t)] = {'duration':[],'cum_duration':[]}
            time_by_index['Time'+'_'+str(t)]['duration'].append((timelist[t]-timelist[t-1]).total_seconds())
            time_by_index['Time'+'_'+str(t)]['cum_duration'].append((timelist[t]-timelist[0]).total_seconds())
        

    onlyduration = {t:time_by_index[t]['duration'] for t in list(time_by_index.keys())[:10]}
    onlycumduration = {t:time_by_index[t]['cum_duration'] for t in list(time_by_index.keys())[:10]}
    durationlist = np.array(onlyduration['Time_'+str(prefix)])
    # t = preprocessing.scale(durationlist)
    t = [x/max(durationlist) for x in durationlist]
    t = np.round_(t,5)    
    durationlist  =[float(x) for x in t] 
    
    cumdurationlist = np.array(onlycumduration['Time_'+str(prefix)])
    # t = preprocessing.scale(cumdurationlist)
    t = [x/max(durationlist) for x in durationlist]
    t = np.round_(t,5)
    cumdurationlist  =[float(x) for x in t] 

    return durationlist,cumdurationlist

if __name__ =='__main__':
    prefix = 3
    df = pd.read_csv('../special_topics/data/hospital_billing.csv')
    # df = pd.read_csv('../new paper/bpic2011/ltl1/bpic2011prep.csv')
    duration,cumduration =normalize_atts(df,'Complete Timestamp',prefix)    
    # print(duration)
    membership_function = plot_membership.membership_f(plot_membership.uniform_plotting_membership(5))
    locs = [x[0] for x in plot_membership.uniform_plotting_membership(5).values()]
    alloc =[]
    for loc in locs:
        alloc +=loc
    minloc = min(alloc)    
    maxloc = max(alloc)
    # print([x.values() for x in membership_function.values()])
    membership_names = list(membership_function.keys())

    fuzzy_set ={}
    for pos,dur in enumerate(duration):
        fuzzy_result = []
        if dur <= minloc:
            membership_value = (membership_names[0],1)
            fuzzy_result.append(membership_value)
        elif dur > maxloc:
            membership_value = (membership_names[-1],1)
            fuzzy_result.append(membership_value)
        else:
            for membership in membership_names:
                for pos, interval in enumerate(membership_function[membership]['Split_interval']):
                    if interval[1] >= dur > interval[0]:
                        membership_value = membership_function[membership]['Value'][pos][0] * dur + membership_function[membership]['Value'][pos][1]
                        totalmembership_value = (membership, membership_value)
                        # print(dur, membership, membership_value)

                        fuzzy_result.append(totalmembership_value)
        print(fuzzy_result)



