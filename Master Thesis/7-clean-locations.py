from obspy import read_events
from myfunc.correction import remove_low_weight_phases, select_proper_events
import glob
import os
from os.path import join
from myfunc.parameters import parameters
params = parameters.QC()
basepath = params.Input


list_nordics = glob.glob(join(basepath, 'located-nordics', '*.out'))
outpath = join(basepath, 'clean-located-nordics')
os.makedirs(outpath, exist_ok=True)

for fpath in list_nordics:
    print(fpath)
    name = os.path.basename(fpath)
    catalog = read_events(fpath)
    remove_low_weight_phases(catalog=catalog, min_p=3, min_weight=4)
    catalog = select_proper_events(cat=catalog, min_num_stations=3, min_azimuthal_gap=180)
    catalog.write(join(outpath, name), format='NORDIC')
