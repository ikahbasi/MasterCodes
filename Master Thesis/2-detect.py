############################
#     by IMAN KAHBASI      #
# master students in IIEES #
############################
from myfunc.process import processing_stream
from myfunc.parameters import parameters
from eqcorrscan.core.match_filter.tribe import Tribe
from os.path import join
from obspy import read
from obspy import UTCDateTime as utc
import logging
import glob
import os
from collections import Counter
# #**##**
params = parameters.detect()
print(params)
Input = params.Input
Input_stream = params.Input_stream
output = params.output
log_level = params.log_level
################################################
os.makedirs(join(output, 'log'), exist_ok=True)
logging.basicConfig(
    level=eval(f'logging.{log_level}'),
    format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
    filename=join(output, 'log', '2-detect.log'),
    filemode='w')
##########
os.makedirs(join(output, 'parties'), exist_ok=True)
# Read in the tribes of templates
tribe_files = glob.glob(join(Input, 'tribes', 'tribe*'))
tribe = Tribe()
for tribe_f in tribe_files:
    tribe.read(tribe_f)
number_of_template_in_each_day = dict(Counter(
    [str(tem.event.origins[0].time.date) for tem in tribe.templates]
        ))
# ### Make list of days that we want to detect on them
dates = sorted(os.listdir(Input_stream))
len_dates = len(dates)
print("*** Number of days with data: ", len_dates)
print("*** Days with data: ", dates)
print('*** Number of total templates:', len(tribe.templates),
      'with group_size:', params.group_size)

total_detections = 0
for i, date in enumerate(dates):
    precent = i*100//len_dates
    real_time = utc()
    real_time.precision = 0
    real_time = real_time.datetime
    print(f'\n**** Detecting on: {date} ({precent}% passed) -- <{real_time}>****')
    # place of some ram test
    st = read(join(Input_stream, date, '*.msd'))
    st = processing_stream(st)
    # Some streams will be empty after remove short traces
    if len(st) == 0:
        print(f'*** {date} ---> No data remaind')
        continue
    print('*** Using these:\n', st.__str__(extended=True))
    # matched filter
    num_last_detections = number_of_template_in_each_day.get(date, 0)
    print(f"*** previous catalog has {num_last_detections} detections")
    try:
        print("*** Starting match filter")
        party = tribe.detect(stream=st,
                             threshold=params.threshold,
                             threshold_type=params.threshold_type,
                             trig_int=params.trig_int,
                             plot=params.plot,
                             plotdir=join(output, 'plots_scc', date),
                             daylong=params.daylong,
                             parallel_process=params.parallel_process,
                             xcorr_func=None,
                             concurrency=None,
                             cores=params.cores,
                             ignore_length=params.ignore_length,
                             ignore_bad_data=params.ignore_bad_data,
                             group_size=params.group_size,
                             overlap=params.overlap,
                             full_peaks=params.full_peaks,
                             save_progress=params.save_progress,
                             process_cores=params.process_cores)  # **kwargs
        # xcorr_func:  None, 'time_domain', 'numpy', 'fftw'
        # concurrency: None, 'multithread', 'multiprocess', 'concurrent'
        # trig_int (float): Minimum gap between detections in seconds.
        party.decluster(trig_int=params.trig_int_decluster,
                        timing=params.timing,
                        metric=params.metric)
        num_detections = len(party.get_catalog())
        print(f"*** {date} ---> DONE ({num_detections} detections)")
    except Exception as error:
        print(f"*** {date} ---> FAILED")
        print(error)
        continue
    # count number of detections
    total_detections += num_detections
    # write party
    print("*** Writing party")
    party.write(join(output, 'parties', f'party_{date}_({num_detections})'),
                format='tar',
                write_detection_catalog=True,
                catalog_format='QUAKEML')
print('\n*** 100% FINISH')
print(f'*** Total number of detections are \
      {total_detections} in {len_dates} days')
print(f'*** And saved in {output}')
