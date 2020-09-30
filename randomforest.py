import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt
from playsound import playsound
import numpy as np
import json
import os

def cuttinginput(df,alpha):
    try:
        df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
    except:
        pass

    df_cols =df.columns.values
    df_collist=['Case ID','Label_1','Label_0']
    for k in df_cols:
        if round(len(df[df[k]==1])/len(df),2) >alpha:
            if k not in df_collist:
                df_collist.append(k)

    df = df.loc[:,df_collist]
    return df, df_collist

def rfclassifer():
    for prefix in range(2,11):
        resultdict={}
        print(prefix)
        resultdict['Label 0'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}
        resultdict['Label 1'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}
        for rndst in [0]:
            
            train = './bpic2015/rule1/prefix'+str(prefix)+'/train_rndst'+str(rndst)+'.csv'
            test = './bpic2015/rule1/prefix'+str(prefix)+'/test_rndst'+str(rndst)+'.csv'
            
            label = []
            train = pd.read_csv(train)
            test = pd.read_csv(test)
            print(train.shape, test.shape)
            try:
                train = train.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
            except:
                pass

            try:
                test = test.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
            except:
                pass

            for k in list(train['Label_1']):
                if k==1:
                    label.append(1)
                else:
                    label.append(0)
            y_train = label

            train = train.drop(['Label_1','Label_0','Case ID'],axis=1)
            try:
                test = test.drop(['Unnamed: 0'],axis=1)
            except:
                pass
            x_train = train

            label = []
            for k in list(test['Label_1']):
                if k==1:
                    label.append(1)
                else:
                    label.append(0)

            y_test = label
            test = test.drop(['Label_1','Label_0','Case ID'],axis=1)
            x_test = test

            rf = RandomForestClassifier(n_estimators=100,oob_score=True,random_state=123456)
            rf.fit(x_train,y_train)
            rf_pred = rf.predict(x_test)
            result =classification_report(y_test,rf_pred,target_names=['Label 0','Label 1'],output_dict=True)
            resultdict['Label 0']['precision'].append(result['Label 0']['precision'])
            resultdict['Label 0']['recall'].append(result['Label 0']['recall'])
            resultdict['Label 0']['f1-score'].append(result['Label 0']['f1-score'])
            resultdict['Label 0']['support'].append(result['Label 0']['support'])
            resultdict['Label 1']['precision'].append(result['Label 1']['precision'])
            resultdict['Label 1']['recall'].append(result['Label 1']['recall'])
            resultdict['Label 1']['f1-score'].append(result['Label 1']['f1-score'])
            resultdict['Label 1']['support'].append(result['Label 1']['support'])

        for pre in resultdict.keys():
            for col in resultdict[pre].keys():
                resultdict[pre][col] = [np.mean(resultdict[pre][col]),np.std(resultdict[pre][col])]

        
        resultdir = './bpic2015/rule1/ruleresult/randomforest'
        try:
            os.makedirs(resultdir)
        except:
            pass
        jsonname = resultdir+'/prefix'+str(prefix)+'result.json'
        print(resultdict)
        with open(jsonname ,'w') as f:
            json.dump(resultdict,f)


def rfreader():
    alpha = 0
    for prefixlength in range(2,3):
        # print(prefixlength)
        resultdir = './sepsis/rule1/ruleresult/randomforest/withoutsparse_'+str(alpha)+'/'
        jsonname = resultdir+'/prefix'+str(prefixlength)+'result.json'
        
        with open(jsonname ,'r') as f:
            data = json.load(f)
        print(data['Label 1']['f1-score'][0])
        # print(data['Label 1']['f1-score'][0])

if __name__=='__main__':
    rfclassifer()
# rfreader()

