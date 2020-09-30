import json
import pandas as pd
import os
import math
import ast

for rnd in range(5):
    for prefix in range(2,11):
        dirname = './bpic2015/rule1/ruleresult/ARM'
        inputpath = './bpic2015/rule1/prefix'+str(prefix)+'/rules/'
        label1df = pd.read_csv(inputpath+'/association_rule_df_label1_rnd'+str(rnd)+'.csv')
        label0df = pd.read_csv(inputpath+'/association_rule_df_label0_rnd'+str(rnd)+'.csv')
        

        ruledict={'Label_1':{},'Label_0':{}}

        try:
            os.makedirs(dirname)
        except:
            pass

        label1_antecedent = list(label1df['Antecedents'])
        label1_support = list(label1df['Support'])
        for pos,x in enumerate(label1_support):
            support_level = str(x)[:3]
            antecedent = '/'.join(sorted(ast.literal_eval(label1_antecedent[pos])))
            if support_level not in list(ruledict['Label_1'].keys()):
                ruledict['Label_1'][support_level] = [antecedent]
            else:
                ruledict['Label_1'][support_level].append(antecedent)

        label0_antecedent = list(label0df['Antecedents'])
        label0_support = list(label0df['Support'])
        for pos,x in enumerate(label0_support):
            support_level = str(x)[:3]
            antecedent = '/'.join(sorted(ast.literal_eval(label0_antecedent[pos])))
            if support_level not in list(ruledict['Label_0'].keys()):
                ruledict['Label_0'][support_level] = [antecedent]
            else:
                ruledict['Label_0'][support_level].append(antecedent)

        savefilename = dirname+'/Rule_prefix'+str(prefix)+'_rnd'+str(rnd)+'.json'
        with open(savefilename,'w') as f:
            json.dump(ruledict,f)
        f.close()


