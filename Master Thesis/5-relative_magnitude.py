############################
#     by IMAN KAHBASI      #
# master students in IIEES #
############################
from eqcorrscan.utils.mag_calc import relative_magnitude
from eqcorrscan.core.match_filter.party import Party
from obspy import read
import glob
from eqcorrscan.utils.pre_processing import dayproc
from obspy import UTCDateTime as utc
from os.path import join
import os
from pathlib import Path
from myfunc.correction import mag2event, dic_max_cc
from myfunc.process import processing_stream
from myfunc.parameters import parameters
def get_detect_near_template_from_party(party):
    for family in party:
        for ii, detect in enumerate(family):
            no_chans = detect.no_chans
            no_phase = len(detect.event.picks)
            if no_phase < (2/3*no_chans):
                family.detections[ii] = None
        family.detections = [d for d in family if d is not None]
# set parameter
params = parameters.relative_magnitude()
print(params)
output = params.output
Input_stream = params.Input_stream
Input = params.Input
input_path = join(Input, 'repicked-parties', '*party*')
input_files = sorted(glob.glob(input_path))
print(f'There are {len(input_files)} parties')
# output write here
####
mag_parties = join(output, 'mag-parties')
os.makedirs(mag_parties, exist_ok=True)
# list of date of total continuse data
counter = 0
last_template_date = None
# run for each party
for inp_num, inp_file in enumerate(input_files):
    real_time = utc()
    real_time.precision = 0
    real_time = real_time.datetime
    print(f'\n* Calc relative magnitude on party({inp_num}of{len(input_files)}): ', inp_file,
          f'\nrun time: ({real_time})')
    party = Party().read(inp_file)
    print('*', party)
    print(f'* with {party.get_catalog().count()} detections')
    # get_detect_near_template_from_party
    #get_detect_near_template_from_party(party)
    print('*', party, '(after collection)')
    print(f'* with {party.get_catalog().count()} detections (after collection)')
    # read data in day of this party
    party_date = str(party.get_catalog()[0].origins[0].time.date)
    print('* Reading data of the party in: ', party_date)
    if not params.use_s_picks:
        st_party = read(join(Input_stream, party_date, '*SZ*.msd'))
    else:
        st_party = read(join(Input_stream, party_date, '*.msd'))
    st_party = processing_stream(st_party)
    print('* Processing data')
    # get parameters of pre_processing from one template from first family.
    # because all of the parameter of  all template is same,
    # then of of them is enough to get.
    temp = party[0].template
    # only get the parameter to print
    temp_params_str = str(temp)
    print(temp_params_str.replace(
        temp_params_str[: temp_params_str.find(':')], 'With parameters'))
    # pre processing data with the parameters
    try:
        st_party = dayproc(st_party,
                           lowcut=params.lowcut or temp.lowcut,
                           highcut=params.highcut or temp.highcut,
                           filt_order=params.filt_order or temp.filt_order,
                           samp_rate=temp.samp_rate,
                           starttime=utc(party_date),
                           parallel=params.parallel,
                           num_cores=params.cores,
                           ignore_length=False,
                           fill_gaps=True,
                           ignore_bad_data=False,
                           fft_threads=1)
    except Exception as error:
        print(error)
        print('core:', params.cores)
        print('Error occur in dayproc of day party stream')
        continue
    # run for each family in this party
    party.sort()
    for num_family, family in enumerate(party):
        print('\n', '\t\t', '*'*80, '\n', '\t\t', '*'*80, '\n')
        print(num_family+1, '--->', family)
        # if catalog of template event doesn't have magnitude,
        # then go to next family
        if family.template.event.magnitudes == []:
            print('Failed\n',
                  "event of this template doesn't have magnitude\n",
                  'skip of calculate relative magnitude')
            print('party: ', party)
            print('family: ', family)
            continue
        # get date time of template of the family to read continues data of it
        template_date = str(family.template.event.origins[0].time.date)
        print('** Reading template data: ', template_date)
        # if date of the template of this family is same to date of last family
        # then don't need to read countinues data and process.
        # but if template is in another date must read new data from new date.
        if template_date == last_template_date:
            print('same to date of last template, Using last data')
        else:
            # read continues data of the template of the family
            if not params.use_s_picks:
                st_template = read(join(Input_stream, template_date, '*SZ*.msd'))
            else:
                st_template = read(join(Input_stream, template_date, '*.msd'))
            st_template = processing_stream(st_template)
            print('** Processing data')
            # get parameters of pre_processing template of this family.
            try:
                st_template = dayproc(st_template,
                                      lowcut=params.lowcut or temp.lowcut,
                                      highcut=params.highcut or temp.highcut,
                                      filt_order=params.filt_order or temp.filt_order,
                                      samp_rate=temp.samp_rate,
                                      starttime=utc(template_date),
                                      parallel=params.parallel,
                                      num_cores=params.cores,
                                      ignore_length=False,
                                      fill_gaps=True,
                                      ignore_bad_data=False,
                                      fft_threads=1)
            except Exception as error:
                print(error)
                print('core:', params.cores)
                print('Error occur in dayproc of template stream')
                continue
            # save name for next step
            last_template_date = template_date
        # pring number of family in this party
        print('** Family number: ', num_family+1, 'of: ', inp_file)
        origin_family = str(family.template.event.origins[0].time)
        print('** ', family)
        print('** Origin time of the template of this family:', origin_family)
        # run for each detection in this family
        for num_detect, detect in enumerate(family.detections):
            if params.use_cc_of_lag:
                try:
                    correlations = dic_max_cc(detect)
                except Exception as error:
                    print('Failed: ', error)
                    correlations = None
            else:
                correlations = None
            print(f'\n*** detection number: {num_detect+1} of {len(family)}')
            print(f'Detection id: {detect.id}')
            try:
                mags, corrs = relative_magnitude(st1=st_template,
                                                 st2=st_party,
                                                 event1=family.template.event,
                                                 event2=detect.event,
                                                 noise_window=params.noise_window,
                                                 signal_window=params.signal_window,
                                                 min_snr=params.min_snr,
                                                 min_cc=params.min_cc,
                                                 use_s_picks=params.use_s_picks,
                                                 correlations=correlations,
                                                 shift=params.shift,
                                                 return_correlations=params.return_correlations,
                                                 weight_by_correlation=params.weight_by_correlation)
                print(corrs)
            except Exception as error:
                print('Failed in relative magnitude function')
                print(error)
                continue
            if list(mags.values()) == []:
                print("Failed. doesn't have any relative magnitude.(maybe for cc threshold)")
                continue
            mean_delta_mag = sum(mags.values()) / len(mags)
            temp_mag = family.template.event.magnitudes[0].mag
            detect_mag = temp_mag + mean_delta_mag
            print(f'template magnitude is: {temp_mag}')
            print(f'child magnitude is: {detect_mag}')
            # add magnitude to catalog of obspy
            mag2event(detect.event,
                      mag=detect_mag,
                      magType='relative_magnitude')
    cats = party.get_catalog()
    num_mags = len(
        [ev.magnitudes[0].mag for ev in cats if ev.magnitudes != []]
        )
    num_cats = party.get_catalog().count()
    name = Path(inp_file).stem.replace('repicked', 'mag')
    name = name.split('(')[:-1]
    name.append(f'({num_mags}of{num_cats})')
    name = '_'.join(name)
    party.write(filename=join(mag_parties, name),
                format='tar',
                write_detection_catalog=True,
                catalog_format='QUAKEML')
