# by IMAN KAHBASI
# IIEES
#################
from eqcorrscan.core.match_filter.party import Party
from os.path import join, isdir
import glob
import os
output = 'output'
# party files
party = Party()
_list = glob.glob(join(output, 'parties', '*party*'))
for ii, f in enumerate(_list):
    print(f'{ii} of {len(_list)}')
    print(f)
    party += Party().read(f, read_detection_catalog=False, estimate_origin=True)
os.makedirs(join(output, 'tmp-cumulative'))
kwargs = {'show':False , 'save':True, 'savefile':join(output, 'tmp-cumulative', 'tmp-cumulative-G.png')}
party.plot(plot_grouped=True, dates=None, min_dets=1, rate=False, **kwargs)

kwargs = {'show':False , 'save':True, 'savefile': join(output, 'tmp-cumulative', 'tmp-cumulative.png')}
party.plot(plot_grouped=False, dates=None, min_dets=1, rate=False, **kwargs)

kwargs = {'show':False , 'save':True, 'savefile':join(output, 'tmp-cumulative', 'tmp-rate-detections.png'),
          'binsize':None}
party.plot(plot_grouped=True, dates=None, min_dets=1, rate=True, **kwargs)
