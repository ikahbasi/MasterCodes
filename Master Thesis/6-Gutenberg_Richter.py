from obspy import read_events
from eqcorrscan.utils.mag_calc import calc_max_curv
from os.path import join
from myfunc.parameters import parameters
from myfunc.helper_eq import read_party
from myfunc.correction import correction_phases, select_proper_events, good_detections_in_party
from myfunc.plot import freq_mag
import os

params = parameters.Gutenberg_Richter()
Input = params.Input
output = params.output
run_name = os.path.basename(Input)


# children
if os.path.isfile(join(Input, 'mag-parties', 'catalog-with-mag.xml')):
    cat = read_events(join(Input, 'mag-parties', 'catalog-with-mag.xml'))
else:
    path = join(output, 'mag-parties', '*party*')
    party = read_party(path)
    good_detections_in_party(party)
    #
    cat = party.get_catalog()
    cat.write(
        join(Input, 'mag-parties', 'catalog-with-mag.xml'), format="QUAKEML"
        )
# mag children
ch_magnitudes = [
    ev.magnitudes[0].mag for ev in cat if ev.magnitudes != []
    ]
'''
from myfunc.read_locations import catalog
xyzm = catalog()
xyzm.read_xyzm(file_name='/home/ehsan/Documents/kahbasi/main/run_clean_data/location/cat-with-mag/merge-mag/xyzm.dat')
ch_magnitudes = xyzm.MAG
'''
ch_completeness = calc_max_curv(ch_magnitudes)

# templates
from eqcorrscan.core.match_filter.tribe import Tribe
import glob
'''
tribe_files = glob.glob(join(Input, 'tribes', 'tribe*'))
tribe = Tribe()
for tribe_f in tribe_files:
    tribe.read(tribe_f)
tm_catalog = []
for t in tribe:
    tm_catalog.append(t.event)
'''
tm_catalog = read_events(join(params.path_refrence_catalog, '*'))
correction_phases(tm_catalog)
tm_catalog = select_proper_events(tm_catalog,
                                  min_num_stations=params.min_num_stations,
                                  min_azimuthal_gap=params.min_azimuthal_gap)
#tm_catalog =  tm_catalog.filter('time > 2014-11-20', 'time < 2014-11-21')
# mag templates
tm_magnitudes = [
    ev.magnitudes[0].mag for ev in tm_catalog if ev.magnitudes != []
    ]
tm_completeness = calc_max_curv(tm_magnitudes)

binsize = 0.25
# GR children
print(f'children -> max: {max(ch_magnitudes)} Mc = {ch_completeness}')
freq_mag(ch_magnitudes=ch_magnitudes,
         ch_completeness=ch_completeness,
         ch_max_mag=max(ch_magnitudes),
         binsize=binsize, show=False, save=True,
         savefile=join(output, f'GR-children({run_name}).png'))

print(f'templates -> max: {max(tm_magnitudes)} Mc = {tm_completeness}')
# GR templates
freq_mag(tm_magnitudes=tm_magnitudes,
         tm_completeness=tm_completeness,
         tm_max_mag=max(tm_magnitudes),
         binsize=binsize, show=False, save=True,
         savefile=join(output, f'GR-template({run_name}).png'))

# GR children VS templates
freq_mag(ch_magnitudes=ch_magnitudes,
         ch_completeness=ch_completeness,
         ch_max_mag=max(ch_magnitudes),
         #
         tm_magnitudes=tm_magnitudes,
         tm_completeness=tm_completeness,
         tm_max_mag=max(tm_magnitudes),
         #
         binsize=binsize, show=False, save=True,
         savefile=join(output, f'GR-templates VS children({run_name}).png'))
