############################
#     by IMAN KAHBASI      #
# master students in IIEES #
############################
from eqcorrscan.core.match_filter import Tribe
import glob
from obspy import read_events, read
from os.path import join
import os
from myfunc.correction import correction_phases, select_proper_events
from myfunc.process import processing_stream
from myfunc.parameters import parameters
from datetime import timedelta
import logging
################################################
params = parameters.tribes()
print(params)
log_level = params.log_level
Input_stream = params.Input_stream
Input_catalog = params.Input_catalog
output = params.output
################################################
os.makedirs(join(output, 'log'), exist_ok=True)
logging.basicConfig(
    level=eval(f'logging.{log_level}'),
    format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
    filename=join(output, 'log', '1-tribes.log'),
    filemode='w')
################################################
os.makedirs(join(output, 'tribes'), exist_ok=True)
################################################
# ### QuakeMLs: path of catalog that we use to make template
catalog = read_events(join(Input_catalog, '*'))
correction_phases(catalog)
catalog = select_proper_events(catalog,
                               min_num_stations=params.min_num_stations,
                               min_azimuthal_gap=params.min_azimuthal_gap)
################################################
# list of date to process
list_date = sorted(list({ev.origins[0].time.date for ev in catalog}))
num_ev = catalog.count()
num_ev_pass = 0
print(f'**** Number of all event in catalog: {len(catalog)} \n ****')
# dictionary of ignore events
ig_evs = {}
one_day_datetime = timedelta(days=1)
for date in list_date:
    print(f'*** making tribe will start in: {date}')
    daily_cat = catalog.filter(f'time > {date}',
                               f'time < {date+one_day_datetime}')
    date = str(date)
    DailyCount = daily_cat.count()
    # read signals in
    if glob.glob(join(Input_stream, date, '*.msd')) == []:
        ig_evs[date] = DailyCount
        num_ev_pass += DailyCount
        print(f"*** {date} ---> There is no data. ({DailyCount} events lost)")
        continue
    st = read(join(Input_stream, date, '*.msd'))
    st = processing_stream(st)
    # Some streams will be empty, so we cant do anything with them...
    if len(st) == 0:
        print(f"*** {date} ---> No data remain. ({DailyCount} events lost)")
        ig_evs[date] = DailyCount
        num_ev_pass += DailyCount
        continue    
    # Start make tribe of templates
    print(f'*** There are {DailyCount} events in this day')
    print('*** Using these data:\n', st.__str__(extended=True))
    try:
        print('*** Start construct')
        tribe = Tribe().construct(st=st,
                                  method="from_meta_file",
                                  meta_file=daily_cat,
                                  lowcut=params.lowcut,
                                  highcut=params.highcut,
                                  samp_rate=params.samp_rate,
                                  filt_order=params.filt_order,
                                  length=params.length,
                                  prepick=params.prepick,
                                  swin=params.swin,
                                  all_horiz=params.all_horiz,
                                  delayed=params.delayed,
                                  plot=params.plot,
                                  plotdir=join(output, 'templates_plot'),
                                  debug=params.debug,
                                  min_snr=params.min_snr,
                                  parallel=params.parallel,
                                  num_cores=params.num_cores,
                                  save_progress=False,
                                  skip_short_chans=params.skip_short_chans)
        lenTribe = len(tribe)
        print(f"*** {date} ---> DONE ({lenTribe} of {DailyCount})")
    except Exception as error:
        print(f"*** {date} ---> FAILED ({DailyCount} lost)")
        print(error)
        continue
    '''
    min_snr (float) – where signal-to-noise ratio is calculated as the
    ratio of the maximum amplitude in the template window to the rms amplitude
    in the whole window given.

    Number of cores to try and use, if False and parallel=True,
    will use either all your cores, or as many traces as in the data
    (whichever is smaller).
    '''
    # convert name of templates from starttime to sequence in tribe
    print('*** Converting name of templates in tribe')
    for template in tribe:
        num_ev_pass += 1
        template.name = str(num_ev_pass)
    print(f'*** Writing tribe of: {date}')
    if lenTribe == DailyCount:
        name = f'tribe_{date}({lenTribe}full)'
    else:
        name = f'tribe_{date}({lenTribe}of{DailyCount})'
    tribe.write(join(output, 'tribes', name))
    # Print perecent of work that done
    precent = round(num_ev_pass*100/num_ev, 2)
    print('\n*** {} of {} events in catalog passed ({}%)\n'
          .format(num_ev_pass, num_ev, precent))

# print events that don't make template for them
events_ignored = num_ev - num_ev_pass
print(f"*** {events_ignored} events didn't have any signal in phase's time")
for key, val in ig_evs.items():
    print(f"In {key} didn't have or remain any stream and {val} events ignored")
