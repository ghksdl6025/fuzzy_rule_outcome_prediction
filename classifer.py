import pandas as pd
import ast
import os
import csv
import json
from tqdm import tqdm
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import classification_report

def loadrule(prefix,rndst,threshold):
    filename = './sepsis/rule1/ruleresult/way3/withoutsparse_0.4/threshold'+str(threshold)+'/Summerized_Rule_prefix'+str(prefix)+'_rnd'+str(rndst)+'.json'
    with open(filename,'r') as f:
        rules = json.load(f)
    label1rulepre = rules['Label_1']
    label0rulepre = rules['Label_0']

    label1rule =[]
    for key in label1rulepre.keys():
        for rule in label1rulepre[key]:
            label1rule.append(rule)
    
    label0rule =[]
    for key in label0rulepre.keys():
        for rule in label0rulepre[key]:
            label0rule.append(rule)
    rules = {'Label_1':label1rule,'Label_0':label0rule}
    return rules

def loadrule2(prefix,rndst):
    
    filename = './bpic2015/rule1/ruleresult/ARM/Summarized_Rule_prefix'+str(prefix)+'_rnd'+str(rndst)+'.json'
    # filename = '../new paper/bpic2015/ltl1/ruleresult/way3/bpic2015_1/threshold0.7/Rule_prefix'+str(prefix)+'_rnd0.json'
    with open(filename,'r') as f:
        rules = json.load(f)
    return rules

def thirdmethod(testset,rules):
    df = pd.read_csv(testset)
    label1 = 'Label_1'
    label0 = 'Label_0'
    label1rules = rules[label1]
    label0rules = rules[label0]
    try:
        df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
    except:
        pass
    caseidlist = list(df['Case ID'])
    label1list = list(df['Label_1'])
    label0list = list(df['Label_0'])

    y_true = {}
    for pos,case in enumerate(caseidlist):
        if label1list[pos] ==1:
            y_true[case] = [1]
        else:
            y_true[case] = [0]

    for pos,k in enumerate(label1rules):
        label1rules[pos] = k.split('/')

    for pos,k in enumerate(label0rules):
        label0rules[pos] = k.split('/')

    df = df.drop(columns=['Case ID'],axis=1)
    cols = df.columns.values
    colindexing={}
    for c in cols:
        for pos,indexing in enumerate(list(df.loc[:,c])):
            if indexing ==1:
                if caseidlist[pos] not in colindexing.keys():
                    colindexing[caseidlist[pos]] = [c]
                else:
                    colindexing[caseidlist[pos]].append(c)
    
    satisfyingrule={} #key = caseid, item = list [0] = # of satisfying label0 rules [1] = # of satisfying label0 rules
    for caseid in colindexing.keys():
        satisfyingrule[caseid] = [0]
        for rule in label0rules:
            result = all(elem in colindexing[caseid] for elem in rule)
            if result:
                satisfyingrule[caseid][0] +=1/len(label0rules)
    
    for case in list(satisfyingrule.keys()):
        if satisfyingrule[case][0]>=0.7:
            y_true[case].append(0)
        else:
            y_true[case].append(1)

    true_y = list(pd.DataFrame(y_true).T[0])
    predict_y = list(pd.DataFrame(y_true).T[1])

    result = classification_report(true_y,predict_y,target_names=['Label 0','Label 1'],output_dict=True)
    return result

def fourthmethod(testset,rules):
    df = pd.read_csv(testset)
    label1 = 'Label_1'
    label0 = 'Label_0'
    label1rules = rules[label1]
    label0rules = rules[label0]
    try:
        df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
    except:
        pass
    caseidlist = list(df['Case ID'])
    label1list = list(df['Label_1'])
    label0list = list(df['Label_0'])

    y_true = {}
    for pos,case in enumerate(caseidlist):
        if label1list[pos] ==1:
            y_true[case] = [1]
        else:
            y_true[case] = [0]

    for pos,k in enumerate(label1rules):
        label1rules[pos] = k.split('/')

    for pos,k in enumerate(label0rules):
        label0rules[pos] = k.split('/')

    df = df.drop(columns=['Case ID'],axis=1)
    cols = df.columns.values
    colindexing={}
    for c in cols:
        for pos,indexing in enumerate(list(df.loc[:,c])):
            if indexing ==1:
                if caseidlist[pos] not in colindexing.keys():
                    colindexing[caseidlist[pos]] = [c]
                else:
                    colindexing[caseidlist[pos]].append(c)
    
    satisfyingrule={} #key = caseid, item = list [0] = # of satisfying label0 rules [1] = # of satisfying label0 rules
    for caseid in colindexing.keys():
        satisfyingrule[caseid] = [0]
        for rule in label1rules:
            result = all(elem in colindexing[caseid] for elem in rule)
            if result:
                satisfyingrule[caseid][0] +=1/len(label1rules)
    
    for case in list(satisfyingrule.keys()):
        if satisfyingrule[case][0]>=0.7:
            y_true[case].append(1)
        else:
            y_true[case].append(0)

    true_y = list(pd.DataFrame(y_true).T[0])
    predict_y = list(pd.DataFrame(y_true).T[1])

    result = classification_report(true_y,predict_y,target_names=['Label 0','Label 1'],output_dict=True)
    return result

def fifthmethod(testset,rules): #Use loadrule2 function
    df = pd.read_csv(testset)
    label1 = 'Label_1'
    label0 = 'Label_0'
    label1rules = rules[label1]
    label0rules = rules[label0]

    if len(label1rules) ==0 and len(label0rules)==0:
        result = {'Label 1':{'precision':0,'recall':0,'f1-score':0,'support':0},'Label 0':{'precision':0,'recall':0,'f1-score':0,'support':0}}
        return result
    try:
        df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
    except:
        pass
    caseidlist = list(df['Case ID'])
    label1list = list(df['Label_1'])
    label0list = list(df['Label_0'])

    y_true = {}
    for pos,case in enumerate(caseidlist):
        if label1list[pos] ==1:
            y_true[case] = [1]
        else:
            y_true[case] = [0]

    for subrule in label1rules.values():
        for pos,smallrule in enumerate(subrule):
            subrule[pos] = smallrule.split('/')
    
    for subrule in label0rules.values():
        for pos,smallrule in enumerate(subrule):
            subrule[pos] = smallrule.split('/')
    
    label0ruleweighted = 0
    label1ruleweighted = 0
    for supplevel in label0rules.keys():
        subrule = label0rules[supplevel]
        label0ruleweighted += float(supplevel)*len(subrule)    
    for supplevel in label1rules.keys():
        subrule = label1rules[supplevel]
        label1ruleweighted += float(supplevel)*len(subrule)

    df = df.drop(columns=['Case ID'],axis=1)
    cols = df.columns.values
    colindexing={}
    
    for c in cols:
        for pos,indexing in enumerate(list(df.loc[:,c])):
            
            if indexing >0:
                if caseidlist[pos] not in colindexing.keys():
                    colindexing[caseidlist[pos]] = [c]
                else:
                    colindexing[caseidlist[pos]].append(c)
    satisfyingrule={} #key = caseid, item = list [0] = # of satisfying label0 rules [1] = # of satisfying label0 rules
    for caseid in colindexing.keys():
        satisfyingrule[caseid] = [0,0]
        for supplevel in label0rules.keys():
            subrule = label0rules[supplevel]
            for smallrule in subrule:
                result = all(elem in colindexing[caseid] for elem in smallrule)
                if result:
                    satisfyingrule[caseid][0] +=float(supplevel)/label0ruleweighted

        for supplevel in label1rules.keys():
            subrule = label1rules[supplevel]
            for smallrule in subrule:
                result = all(elem in colindexing[caseid] for elem in smallrule)
                if result:
                    satisfyingrule[caseid][1] +=float(supplevel)/label1ruleweighted
        
        if satisfyingrule[caseid][0] > satisfyingrule[caseid][1]:
            y_true[caseid].append(0)
        elif satisfyingrule[caseid][0] < satisfyingrule[caseid][1]:
            y_true[caseid].append(1)
        else:
            del(y_true[caseid])

    true_y = list(pd.DataFrame(y_true).T[0])
    predict_y = list(pd.DataFrame(y_true).T[1])

    result = classification_report(true_y,predict_y,target_names=['Label 0','Label 1'],output_dict=True)
    return result

def fifthmethod_fuzzy(testset,rules): #Use loadrule2 function
    df = pd.read_csv(testset)
    label1 = 'Label_1'
    label0 = 'Label_0'
    label1rules = rules[label1]
    label0rules = rules[label0]

    if len(label1rules) ==0 and len(label0rules)==0:
        result = {'Label 1':{'precision':0,'recall':0,'f1-score':0,'support':0},'Label 0':{'precision':0,'recall':0,'f1-score':0,'support':0}}
        return result
    try:
        df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
    except:
        pass
    caseidlist = list(df['Case ID'])
    label1list = list(df['Label_1'])
    label0list = list(df['Label_0'])

    y_true = {}
    for pos,case in enumerate(caseidlist):
        if label1list[pos] ==1:
            y_true[case] = [1]
        else:
            y_true[case] = [0]

    for subrule in label1rules.values():
        for pos,smallrule in enumerate(subrule):
            subrule[pos] = smallrule.split('/')
    
    for subrule in label0rules.values():
        for pos,smallrule in enumerate(subrule):
            subrule[pos] = smallrule.split('/')
    
    label0ruleweighted = 0
    label1ruleweighted = 0
    for supplevel in label0rules.keys():
        subrule = label0rules[supplevel]
        label0ruleweighted += float(supplevel)*len(subrule)    
    for supplevel in label1rules.keys():
        subrule = label1rules[supplevel]
        label1ruleweighted += float(supplevel)*len(subrule)

    
    cols = df.columns.values
    colindexing={}

    for t in range(len(df)):
        df_todict = df.loc[t,:].to_dict()
        df_todict = {c : df_todict[c] for c in df_todict.keys() if float(df_todict[c]) > 0.0}
        # print(df_todict)
        caseid = int(df_todict['Case ID'])
        del df_todict['Case ID']
        colindexing[caseid] = df_todict

    print(colindexing[12539803])
    satisfyingrule={} #key = caseid, item = list [0] = # of satisfying label0 rules [1] = # of satisfying label0 rules
    for caseid in colindexing.keys():
        satisfyingrule[caseid] = [0,0]
        for supplevel in label0rules.keys():
            subrule = label0rules[supplevel]
            rulediff_score = {}
            for smallrule in subrule:
                result = all(elem in list(colindexing[caseid].keys()) for elem in smallrule)
                if result and caseid == 12539803:
                    print(count, [colindexing[caseid][t] for t in smallrule])
                    satisfyingrule[caseid][0] +=float(supplevel)/label0ruleweighted
                    
                    for t in smallrule:
                        if colindexing[caseid][t] < 1.0:
                            rulediff_score[t] = colindexing[caseid][t]
            # print(rulediff_score)
        # print('----------')

        for supplevel in label1rules.keys():
            subrule = label1rules[supplevel]
            for smallrule in subrule:
                result = all(elem in list(colindexing[caseid].keys()) for elem in smallrule)
                if result:
                    satisfyingrule[caseid][1] +=float(supplevel)/label1ruleweighted
        
        if satisfyingrule[caseid][0] > satisfyingrule[caseid][1]:
            y_true[caseid].append(0)
        elif satisfyingrule[caseid][0] < satisfyingrule[caseid][1]:
            y_true[caseid].append(1)
        else:
            del(y_true[caseid])

    true_y = list(pd.DataFrame(y_true).T[0])
    predict_y = list(pd.DataFrame(y_true).T[1])

    result = classification_report(true_y,predict_y,target_names=['Label 0','Label 1'],output_dict=True)
    return result

if __name__ == "__main__":
    
    for prefix in range(5,6):
        print("Prefix :%s"%(prefix))
        resultdict={}
        resultdict['Label 0'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}
        resultdict['Label 1'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}
        for rndst in [0]:
            testset = './bpic2015/rule1/prefix'+str(prefix)+'/test_rndst'+str(rndst)+'.csv'
            rules=loadrule2(prefix,rndst,)
            result = fifthmethod_fuzzy(testset,rules)
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
        resultdir = './bpic2015/rule1/ruleresult/ARM/fifthmethod/'
        try:
            os.makedirs(resultdir)
        except:
            pass
        jsonname = resultdir+'/Summarized_prefix'+str(prefix)+'result.json'
        print(resultdict)
        # with open(jsonname ,'w') as f:
        #     json.dump(resultdict,f)
    

