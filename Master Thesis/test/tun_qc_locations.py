from myfunc.qcontrol import run
import glob

_dirs = glob.glob('filter_test/locations/catalog*')

for _dir in _dirs:
    print(_dir)
    run(_dir)
