import pandas as pd

import sys
import os
from functools import reduce
from sklearn.model_selection import train_test_split

from tqdm import tqdm

for prefix in range(2,11):
    dir_path = './bpic2015/rule1/prefix'+str(prefix)
    df = pd.read_csv(dir_path+'/bpic2015_concatanated_fuzzy_tx.csv')
    for rndst in range(0,5):
        df_train,df_test = train_test_split(df,test_size=0.3,random_state=rndst) #Random State 0,1,2,3,4,5,6,7,8,9 10 numbers
        # filename = dir_path+'/indexbase/prefix'+str(prefix)+'/simple_timediscretize/'
        droplist = []
        for t in df_train.columns.values:
            if '.1' not in t:
                droplist.append(t)
        df_train = df_train.loc[:,droplist]
        df_test = df_test.loc[:,droplist]
        df_train.to_csv(dir_path+'/train_rndst'+str(rndst)+'.csv',index=False)
        df_test.to_csv(dir_path+'/test_rndst'+str(rndst)+'.csv',index=False)


