na_stations = {'6266': 'TONL', '6180': 'SKAR', '6289': 'EINS',
               '6269': 'ANJR', '6254': 'ABTF', '6252': 'MAHO',
               '6219': 'MIME', '6260': 'DLRN', 'CMG6': 'MAHO',
               '6226': 'TIAK', '6259': 'JHAD', '6215': 'HONG',
               '6267': 'GLGL', '6249': 'BARE',
               '5645': 'TONL'}
stations = na_stations.values()
phases = {}
for sta in stations:
    phases[sta] = []
#with open(r'C:\Users\ashka\Dropbox\0_payan-name\code\ilam\results\on-thesis\locations\hypoell3575\nordic.out') as inp:
with open(r'C:\Users\ashka\Dropbox\0_payan-name\code\ilam\results\refrence\templates_838.out') as inp:
    for line in inp:
        line = line.split()
        if line == []:
            continue
        if line[0] in stations:
            phases[line[0]].append(int(line[3]))

cnt = {}
for key, val in phases.items():
    cnt[key] = {'0': val.count(0), '4': val.count(4)}
    
stations = []
w0 = []
w4 = []
for key, val in cnt.items():
    stations.append(key)
    w0.append(val['0'])
    w4.append(val['4'])    

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
x = np.arange(len(stations))
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, w0, width, label='good phase', edgecolor='black', linewidth=1)
rects2 = ax.bar(x + width/2, w4, width, label='Outlier', edgecolor='black', linewidth=1)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2)
ax.set_xticks(x)
ax.set_xticklabels(stations, weight='bold')
ax.set_yticks([])
ax.yaxis.set_tick_params(labelsize=10)
ax.xaxis.set_tick_params(labelsize=10)
ax.legend()
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)


autolabel(rects1)
autolabel(rects2)
plt.title('Reference catalog of Ilam', fontsize=18, weight='bold')
plt.ylim(top=6100)
fig.tight_layout()
plt.show()

