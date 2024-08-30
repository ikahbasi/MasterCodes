from myfunc.plot import twoD_seismplot, threeD_seismplot
from myfunc.correction import correction_phases, select_proper_events
from obspy import read_events

cat_children = read_events('../../main_19mordad/located-nordics/*.out')
cat_template0 = read_events('../../catalog/*.out')
correction_phases(cat_template0)
cat_template = select_proper_events(cat=cat_template0, min_num_stations=3,
                                    min_azimuthal_gap=180)
#twoD_seismplot(catalog=cat_children, show=True)
#threeD_seismplot(catalog_children=cat_children, catalog_template=cat_template)
threeD_seismplot(catalog_children=cat_children)
