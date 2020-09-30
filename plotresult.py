import matplotlib.pyplot as plt
import json
import pandas as pd
df = pd.DataFrame()
armlabel0f1 = []
armlabel1f1 = []
rflabel0f1 = []
rflabel1f1 = []

for prefix in range(2,11):
    filename = './bpic2015/rule1/ruleresult/ARM/fifthmethod/prefix'+str(prefix)+'result.json'
    
    with open(filename,'r') as f:
        result = json.load(f)

    armlabel1f1.append(result['Label 1']['f1-score'][0])
    armlabel0f1.append(result['Label 0']['f1-score'][0])


    filename = './bpic2015/rule1/ruleresult/randomforest/prefix'+str(prefix)+'result.json'
    with open(filename,'r') as f:
        result = json.load(f)

    rflabel1f1.append(result['Label 1']['f1-score'][0])
    rflabel0f1.append(result['Label 0']['f1-score'][0])

xtick = [x for x in range(2,11)]
plt.plot(xtick,armlabel0f1,label='Fuzzy ARM label 0')
plt.plot(xtick,armlabel1f1,label='Fuzzy ARM label 1')
plt.plot(xtick,rflabel0f1,label='RF label 0')
plt.plot(xtick,rflabel1f1,label='RF label 0')
plt.ylim(0.2,1.1)
plt.legend()
# plt.show()
plt.title('BPIC 2015 F1-score')
plt.savefig('./img/fuzzyvsrf.png')

plt.cla()
plt.clf()
oldarmlabel1f1=[]
oldarmlabel0f1=[]
for prefix in range(2,11):
    filename ='../new paper/bpic2015/ltl1/ruleresult/way3/fifthmethod/bpic2015_1/prefix'+str(prefix)+'result.json'
    with open(filename,'r') as f:
        result = json.load(f)

    oldarmlabel1f1.append(result['Label 1']['f1-score'][0])
    oldarmlabel0f1.append(result['Label 0']['f1-score'][0])
    
xtick = [x for x in range(2,11)]
plt.plot(xtick,oldarmlabel0f1,label='Normal ARM label 0')
plt.plot(xtick,oldarmlabel1f1,label='Normal ARM label 1')
plt.plot(xtick,armlabel0f1,label='Fuzzy ARM label 0')
plt.plot(xtick,armlabel1f1,label='Fuzzy ARM label 0')
plt.ylim(0.2,1.1)
plt.legend()
# plt.show()
plt.title('BPIC 2015 F1-score')
plt.savefig('./img/fuzzyvsnormal.png')
