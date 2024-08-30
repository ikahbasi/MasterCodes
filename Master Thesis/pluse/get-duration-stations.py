import glob
from os.path import join, basename
import numpy as np

def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict


days = sorted(glob.glob('2014*'))

details = {}

for day in days:
    #contents = glob.glob(join(day, '*.msd')) + glob.glob(join(day, 'outlier', '*.msd'))
    contents = glob.glob(join(day, '*.msd')) + glob.glob(join(day, 'outlier', '*HONG*.msd'))
    for content in contents:
        station = basename(content)[:4]
        print(station)
        if station == 'unkn':
            print(station)
            station = 'BARE'
        if station not in details.keys():
            details[station] = []
            
        details[station].append(day)
        



#res = sorted(details, key = lambda key: len(details[key]), reverse=True)
#details = {k: v for k, v in sorted(details.items(), key=lambda item: item[1])}

stations = []
ii = 1
import matplotlib.pyplot as plt
for key, val in details.items():
#    for v in val:
    stations.append(key)
    if key == 'HONG':
        val = []
    plt.plot(val, ii*np.ones(len(val)), 'o')
    ii += 1
plt.yticks(range(1, len(stations)+1), stations, weight='bold')
plt.xticks(['2014-08-20', '2014-09-01', '2014-10-01', '2014-11-01', '2014-11-25'], weight='bold')
ax = plt.gca()
ax.xaxis.set_tick_params(labelsize=10)
ax.yaxis.set_tick_params(labelsize=10)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2)
plt.grid()
plt.title('Cleaned data of Ilam-network', fontsize=20, weight='bold')
plt.show()
