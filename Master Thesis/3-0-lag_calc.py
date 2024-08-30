# by IMAN KAHBASI
# IIEES
#################
from myfunc.process import processing_stream
from myfunc.parameters import parameters
from eqcorrscan.core.match_filter.party import Party
from obspy import read
from obspy import UTCDateTime as utc
import glob
import os
from os.path import join, basename
import logging
# #**##**
params = parameters.lag_calc()
print(params)
log_level = params.log_level
Input = params.Input
Input_stream = params.Input_stream
output = params.output
################################################
os.makedirs(join(output, 'log'), exist_ok=True)
logging.basicConfig(
    level=eval(f'logging.{log_level}'),
    format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
    filename=join(output, 'log', '3-lag-calc.log'),
    filemode='w')
##########
# party files
party_files = glob.glob(join(Input, 'parties', 'party*'))
len_parties = len(party_files)

output_rp_parties = join(output, 'repicked-parties')
os.makedirs(output_rp_parties, exist_ok=True)
for i, f in enumerate(sorted(party_files)):
    real_time = utc()
    real_time.precision = 0
    real_time = real_time.datetime
    print('\n**** Start phase picking on {} ({}% passed) -- <{}>****'
          .format(f, i*100//len_parties, real_time))
    # if read_detection_catalog set to False then origin time estimate
    party = Party().read(f, read_detection_catalog=False, estimate_origin=True)
    party.decluster(trig_int=params.trig_int,
                    timing=params.timing,
                    metric=params.metric)
    print('***', party, 'include ', len(party.get_catalog()), 'events')
    if len(party.get_catalog()) == 0:
        print('no detection, go to the next party')
        continue
    date = basename(f).split('_')[1]
    st = read(join(Input_stream, date, '*.msd'))
    st = processing_stream(st, good_data_run=False)
    # Some streams will be empty after remove short traces
    if len(st) == 0:
        print('*** Failed ---> {} (No data remaind)'.format(date))
        continue
    print('*** Using these:\n', st.__str__(extended=True))
    # check if families didn't have any detections
    party = party.filter(dates=[utc(date), utc(date)+24*3600])
    # Find true phase picks
    if params.relative_magnitudes:
        kwargs = {'noise_window': (-20, -1),
                  # 'signal_window': (-0.5, 20),
                  'min_snr': 1.0}
    else:
        kwargs = {}
    try:
        print("*** Starting lag_calc for detections")
        cat_cc = party.lag_calc(stream=st,
                                pre_processed=params.pre_processed,
                                shift_len=params.shift_len,
                                min_cc=params.min_cc,
                                horizontal_chans=['E', 'N', '1', '2'],
                                vertical_chans=['Z'],
                                cores=params.cores,
                                interpolate=params.interpolate,
                                plot=params.plot,
                                plotdir=join(output, 'lag-plot'),
                                parallel=params.parallel,
                                process_cores=params.cores,
                                ignore_length=params.ignore_length,
                                ignore_bad_data=params.ignore_bad_data,
                                relative_magnitudes=params.relative_magnitudes,
                                **kwargs)
        print("*** {} ---> DONE".format(date))
        min_chans = params.min_chans
        party.min_chans(min_chans=min_chans)
        num_repicked = party.get_catalog().count()
        print(f"*** Writing re-picked party with {num_repicked} events")
        print(f"*** {cat_cc.count() - num_repicked} event have less than {min_chans} phases")
        party.write(
            filename=join(output_rp_parties, f'repicked_party_{date}({num_repicked})'),
            format='tar',
            write_detection_catalog=True,
            catalog_format='QUAKEML')
    except Exception as error:
        print("*** {} ---> FAILED".format(date))
        print(error)
        continue
print('\n*** 100% FINISH\n')
