from myfunc.qcontrol import hist_cc_detect
import glob
from myfunc.helper_eq import read_party
from os.path import join
import os
import matplotlib.pyplot as plt

_dirs = glob.glob('filter_test/run*')



datas = {}
for _dir in _dirs:
    print(_dir)
    run_name = os.path.basename(_dir)
    party = read_party(join(_dir, 'repicked-parties', '*'))
    catalog = party.get_catalog()
    print(catalog)
    bins, values = hist_cc_detect(party=party, return_data=True, show=False)
    print(bins, values)
    datas[run_name] = dict(zip(bins, values))

ref_name = run_name
reference = datas[ref_name]

output = 'diff/cc_detection'
os.makedirs(output, exist_ok = True)
for run_name, a in datas.items():
    diff = {}
    for key, val in a.items():
        diff[key] = val - reference.get(key, 0)
    for key in reference.keys():
        if key not in a.keys():
            diff[key] = -1 * reference[key]
    (bins, values) = zip(*diff.items())
    fig = plt.figure(figsize=(8, 6))
    plt.barh(bins, values)
    max_x = 5
    plt.xlim([-max_x, max_x])
    plt.ylim([-5, 12])
    plt.yticks(bins)
    plt.xticks(values)
    #
    name = f'{run_name} - {ref_name}'
    plt.title(name)
    fig.savefig(f'{output}/{name}.png')

