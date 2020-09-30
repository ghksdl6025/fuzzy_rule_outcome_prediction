import pandas as pd
for prefix in range(2,11):
    continuous = pd.read_csv('../new paper/bpic2015/ltl1/bpic2015_1/indexbase/prefix'+str(prefix)+'/simple_timediscretize/ARMinput_preprocessed.csv')
    fuzzified = pd.read_csv('./bpic2015/rule1/prefix'+str(prefix)+'/bpic2015_fuzzified.csv')
    
    neglect =['(case) SUMleges','Time']
    takecolumn = []
    deletecolumn = []
    for t in list(continuous.columns.values):
        for n in neglect:
            if n not in t:
                takecolumn.append(t)
            else:
                deletecolumn.append(t)
    takecolumn.remove('Case ID')      
      
    # continuous = continuous.loc[:,takecolumn]    
    
    dft = pd.merge(fuzzified,continuous,on='Case ID')
    filename = './bpic2015_concatanated_fuzzy_tx.csv'
    dirname = './bpic2015/rule1/prefix'+str(prefix)
    dft = dft.drop(columns=deletecolumn,axis=1)
    dft.to_csv(dirname+filename,index=False)
    
    