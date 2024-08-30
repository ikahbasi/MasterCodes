from myfunc.qcontrol_plot import interval_events
from myfunc.helper_eq import read_party

path = '/home/ehsan/Documents/kahbasi/main_19mordad/run2-8/repicked-parties/*'
party = read_party(path=path, read_detection_catalog=False, estimate_origin=True)

interval_events(party=party, catalog=None, times=None, max_time=100, bins=10)
