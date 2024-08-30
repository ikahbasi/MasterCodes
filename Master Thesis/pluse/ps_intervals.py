from obspy import read_events
from myfunc.correction import *
from myfunc.qcontrol_plot import *
cat = read_events('/home/ehsan/Documents/kahbasi/catalog/Ilam_s1.out')
catalog = select_proper_events(cat, 3, 180)
catalog.count()
ps_delta(catalog, path='.')

