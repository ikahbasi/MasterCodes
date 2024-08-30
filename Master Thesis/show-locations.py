from myfunc.plot import twoD_seismplot, threeD_seismplot
from myfunc.correction import correction_phases, select_proper_events
from obspy import read_events
from myfunc.read_locations import *

#all_evs = read_events('/home/imon/Dropbox/0_payan-name/code/ilam/results/refrence/Ilam_s1.out')
cat_children = read_events('/media/imon/imon32/31mordad/main/located-nordics/nordic-run_clean_data.out')
cat = catalog()
#hypoDD
cat.read_xyzm('/home/imon/Dropbox/0_payan-name/code/ilam/results/3/run_3/xyzm.dat')

#hypoellipse
#cat.read_xyzm('/home/imon/Dropbox/0_payan-name/code/ilam/results/2/hypoellipse/xyzm.dat')

#cond = [(cat.RMS<0.1) & (cat.SEH<1) & (cat.SEZ<2)]
cond = [cat.RMS < 100]
location_children = zip(cat.LAT[cond], cat.LON[cond], -cat.DEPTH[cond])

cat = catalog()
#cat.read_xyzm('/home/imon/Dropbox/0_payan-name/code/ilam/results/refrence/xyzm_838.dat')
#location_templates = zip(cat.LAT, cat.LON, -cat.DEPTH)
#cat_children = read_events('../../main_19mordad/located-nordics/*.out')
#cat_template0 = read_events('../../catalog/*.out')
#correction_phases(cat_template0)
#cat_template = select_proper_events(cat=cat_template0, min_num_stations=3,
#                                    min_azimuthal_gap=180)
twoD_seismplot(catalog=cat_children, method='time', show=True)
#threeD_seismplot(catalog_children=cat_children, catalog_template=cat_template)
threeD_seismplot(location_children=location_children)#,
                 #location_templates=location_templates)
