import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

def uniform_plotting_membership(interval_number):
    interval_value =1/(2 * interval_number -1)
    total_interval = []
    interval =0
    for x in range(2*interval_number):
        total_interval.append(interval)
        interval +=interval_value
    total_interval[-1] = 1
    membership_f_front = [1,1,0]
    membership_f_mid = [0,1,1,0]
    membership_f_end = [0,1,1]

    fig,ax = plt.subplots()
    membership_loc={}

    for x in range(interval_number):
        interval_name = 'Interval_'+str(x+1)
        if x ==0:
            ax.plot(total_interval[x:x+3], membership_f_front,color='black')
            membership_loc[interval_name] = [total_interval[x:x+3], membership_f_front]
        elif x == interval_number-1:       
            ax.plot(total_interval[interval_number*2-3:interval_number*2], membership_f_end,color='black')
            membership_loc[interval_name] = [total_interval[interval_number*2-3:interval_number*2], membership_f_end]
        else:
            ax.add_patch(patches.Polygon(xy=list(zip(total_interval[2*x-1:2*x-1+4],membership_f_mid)),fill=False))
            membership_loc[interval_name] = [total_interval[2*x-1:2*x-1+4], membership_f_mid]
            
    ax.spines['top'].set_visible(False)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    plt.tight_layout()
    # plt.savefig('./uniform_membership_function.png')
    return membership_loc


def membership_f(membership_loc):
    interval_list = list(membership_loc.keys())

    membership_function ={}
    for name in interval_list:
        membership_area = membership_loc[name]
        membership_function[name] = {'Split_interval':[],'Value':[]}
        for k in range(len(membership_area[1])-1):
            if membership_area[1][k] == membership_area[1][k+1]:
                membership_function[name]['Split_interval'].append((membership_area[0][k], membership_area[0][k+1]))
                membership_function[name]['Value'].append((0,1))
            else:
                slope = (membership_area[1][k+1] -membership_area[1][k]) / (membership_area[0][k+1] -membership_area[0][k])
                beta = membership_area[1][k] - (slope * membership_area[0][k])                
                formula = (slope, beta)

                membership_function[name]['Split_interval'].append((membership_area[0][k], membership_area[0][k+1]))
                membership_function[name]['Value'].append(formula)

    return membership_function

if __name__=='__main__':
    membership_loc = uniform_plotting_membership(5)
    t = membership_f(membership_loc)
    print(t)





