import collections
from collections import Counter
import numpy as np
from os.path import join
import os

def _logging_exceptions(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
    except Exception as error:
        print(f"{f}: {error}")
        raise


def _write_data(path, name, header, bins_hist, **kwargs):
    '''
    write output of functions in a ascii file
    
    dictionary of key and array
    path of output
    file name to save
    '''
    os.makedirs(path, exist_ok=True)
    outpath = join(path, f'{name}.hist')
    rows = list(zip(*bins_hist))
    newline = '\n'
    header = ''.join(['{:<15}'.format(x) for x in header])
    #
    with open(outpath, 'w', newline=newline) as outfile:
        print(name, file=outfile)
        print(header, file=outfile)
        for row in rows:
            row = ''.join(['{:<15}'.format(round(x, 2)) for x in row])
            print(row, file=outfile)
    print(f'data save to {outpath}')


def _write_json(dictinary, path, mode='w', **kwargs):
    import json
    basepath = os.path.dirname(path)
    os.makedirs(basepath, exist_ok=True)
    json.dump(dictinary,
              open(path, mode)
              )
    print(f'data save to {path}')


def hist_scc(party, **kwargs):
    '''
    draw histogram of sum of cc phase picking of each event
    '''
    from myfunc.correction import dic_max_cc
    scc            = []
    scc_norm_phase = []
    scc_norm_temp  = []
    for family in party:
        for detection in family.detections:
            if len(detection.event.picks) == 0:
                print('detection with zero picks found')
                continue
            # get cc of phase-picking
            phases_cc  = dic_max_cc(detection)
            cc         = sum(list(phases_cc.values()))
            
            scc.append(cc)
            scc_norm_temp.append(round(cc/detection.no_chans, 5))
            scc_norm_phase.append(round(cc/len(detection.event.picks), 5))
    # normalized scc
    step = 0.05
    bins_norm = np.arange(0, 1+step, step)
    hist_scc_norm_phase = np.histogram(scc_norm_phase, bins=bins_norm)
    hist_scc_norm_temp  = np.histogram(scc_norm_temp, bins=bins_norm)
    # write to a file
    name = kwargs['name']
    path = kwargs['path']
    kwargs.update(path      = join(path, 'n-scc'),
                  name      = f'n-scc_{name}',
                  header    = ['scc', 'rate-phase', 'rate-temp'],
                  bins_hist = [hist_scc_norm_phase[1],
                               hist_scc_norm_phase[0],
                               hist_scc_norm_temp[0]])
    _write_data(**kwargs)
    # scc
    step = 1
    bins = np.arange(0, int(max(scc))+step, step)
    hist_scc = np.histogram(scc, bins=bins)
    kwargs.update(path      = join(path, 'scc'),
                  name      = f'scc_{name}',
                  header    = ['scc', 'rate'],
                  bins_hist = [hist_scc[1], hist_scc[0]])
    _write_data(**kwargs)


def hist_cc(party, absolute=True, **kwargs):
    '''
    draw hsitogram of detect_vals of party
    '''
    name = kwargs['name']
    path = kwargs['path']
    #
    cc_detect = []
    cc_detect_norm = []
    for family in party:
        for detection in family.detections:
            ###
            cc = detection.detect_val
            if absolute:
                cc = abs(cc)
            cc_detect.append(cc)
            ###
            cc_norm = round(detection.detect_val/detection.no_chans, 5)
            if absolute:
                cc_norm = abs(cc_norm)
            cc_detect_norm.append(cc_norm)
    # normlized
    step = 0.1
    cc_detect_norm.sort()
    bins_norm = np.arange(int(min(cc_detect_norm))-2*step,
                          max(cc_detect_norm)+step, step)
    print(bins_norm)
    hist_norm = np.histogram(cc_detect_norm, bins=bins_norm)
    # write
    kwargs.update(path = join(path, 'n-cc'),
                  name      = f'n-cc_{name}',
                  header    = ['cc', 'rate'],
                  bins_hist = [hist_norm[1], hist_norm[0]])
    _write_data(**kwargs)
    ###############
    # not normalized
    step = 1
    bins = np.arange(int(min(cc_detect))-step, int(max(cc_detect))+step, step)
    hist = np.histogram(cc_detect, bins=bins)
    # write to a file
    kwargs.update(path = join(path, 'cc'),
                  name      = f'cc_{name}',
                  header    = ['cc', 'rate'],
                  bins_hist = [hist[1], hist[0]])
    _write_data(**kwargs)




def phases_pre_event(catalog, **kwargs):
    '''
    each event of the catalog has how many phases.
    show avrege phases pre event of the catalog.
    show avrege p-phases and s-phases pre event of the catalog.
    all result show in a plot.
    '''
    picks = []
    for event in catalog:
        for pick in event.picks:
            if pick.phase_hint is not None:
                picks.append(pick.phase_hint)
    js = {}
    num_events = catalog.count()
    js['num_events'] = num_events
    
    num_all_phases = len(picks)
    js['num_all_phases'] = num_all_phases
    
    phases_counter = Counter(picks)
    js['phases_counter'] = phases_counter
    
    phases_in_each_event = [len(ev.picks) for ev in catalog]
    phases_in_each_event = Counter(phases_in_each_event)
    js['phases_in_each_event'] = phases_in_each_event
    
    path = kwargs.get('path')
    name = kwargs.get('name')
    kwargs.update(path=join(path, f'phases-pre-event_{name}.json'))
    _write_json(js, **kwargs)
    #num_phases, num_events = phases_in_each_event.items()


def phase_counter(catalog, **kwargs):
    '''
    how many p-phases and s-phases are in catalog.
    return: matplotlib.plot
    '''
    picks = []
    for event in catalog:
        for pick in event.picks:
            picks.append(pick.phase_hint)
    counter = Counter(picks)
    counter = collections.OrderedDict(sorted(counter.items()))
    path = kwargs.get('path')
    name = kwargs.get('name')
    kwargs.update(path=join(path, f'phases-counter_{name}.json'))
    _write_json(counter, mode='w', **kwargs)
    

def self_detection(party, num_reference_events=None, **kwargs):
    '''
    how many self detections (full detection)
    and
    how many new detections

    self detections select if

    number of channel of detection
    EQUAL TO
    detection value of sum of cross-correlation detection.
    '''
    self_detection = []
    new_detection = []
    num_reference_events = num_reference_events or len(party)
    for family in party:
        for detection in family.detections:
            if detection.no_chans == round(detection.detect_val, 3):
                self_detection.append(detection.detect_val)
            else:
                new_detection.append(detection.detect_val)
    dictionary = dict(self_detection=len(self_detection),
                      new_detection=len(new_detection),
                      reference_detections=num_reference_events)
    path = kwargs.get('path')
    name = kwargs.get('name')
    kwargs.update(path=join(path, f'self-detection_{name}.json'))
    _write_json(dictionary, **kwargs)
    
def get_rms_phases_cat(catalog, step=0.5, **kwargs):
    '''
    get_rms_phases_cat(cat, name='test-rms', path=join('.', 'filter_test', 'QC'))
    '''
    rms = []
    for event in catalog:
        origin = event.origins[0]
        for arrival in origin.arrivals:
                rms.append(arrival.time_residual)
    rms = [_rms or 0 for _rms in rms]
    bins = np.arange(int(min(rms))-2*step,
                     max(rms)+2*step, step)
    hist_rms = np.histogram(rms, bins=bins)
    # write
    name = kwargs['name']
    kwargs.update(name      = f'rms_{name}',
                  header    = ['rms', 'rate'],
                  bins_hist = [hist_rms[1], hist_rms[0]])
    _write_data(**kwargs)
    
'''
if __name__=='__main__':
    import sys
    if '--path' in sys.argv:
        path = sys.argv[sys.argv.index('--path') + 1]
        run(path)
    else:
        pass
'''
