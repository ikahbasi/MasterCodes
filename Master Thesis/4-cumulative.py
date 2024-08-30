############################
#     by IMAN KAHBASI      #
# master students in IIEES #
############################
from myfunc.helper_eq import read_party
from os.path import join
from myfunc.parameters import parameters
import os
params = parameters.cumulative()
print(params)
Input = params.Input
output = params.output
# party files
run_name = os.path.basename(Input)

path = join(Input, 'repicked-parties', '*party*')
party = read_party(path)
#party.min_chans(min_chans=params.min_chans)
min_dets = 0

party.plot(plot_grouped=True,
           dates=None,
           min_dets=min_dets,
           rate=False,
           show=False,
           save=True,
           savefile=join(output, f'cumulative-group({run_name}).png'))

party.plot(plot_grouped=False,
           dates=None,
           min_dets=min_dets,
           rate=False,
           show=False,
           save=True,
           savefile=join(output, f'cumulative-all({run_name}).png'))

binsize = 1.5 * 24 * 60 * 60
party.plot(plot_grouped=True,
           dates=None,
           min_dets=min_dets,
           rate=True,
           show=False,
           save=True,
           binsize=binsize,
           savefile=join(output, f'detections-rate({run_name}).png'))
