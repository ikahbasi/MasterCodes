import glob
from os.path import join, basename
tests = glob.glob('filter_test(*')

d = {}
for test in tests:
    runs = glob.glob(join(test, 'run*'))
    for run in runs:
        print(run)
        run_name = basename(run)
        if run_name not in d.keys():
            d[run_name] = {}
        method = run.split('(')[1].split(')')[0].split('-')[-1]
        print(run)
        path = join(run, 'log', '3-lag-terminal.log')
        f = open(path)
        txt = f.read()
        d[run_name][method] = txt.count('skip')
        
for key, val in d.items():
    k = val.keys()
    v = val.values()
    
    print(f"{key:<10}   75: {val['75']}    60: {val['60']:>2}    50: {val['50']:>2}")