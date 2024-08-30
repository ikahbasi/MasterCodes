import matplotlib.pyplot as plt
import numpy as np
from os.path import join, splitext
import os
import collections
import random
import glob
import json


def _finalise_figure(fig, **kwargs):  # pragma: no cover
    """
    Internal function to wrap up a figure.
    {plotting_kwargs}
    """
    show = kwargs.get("show", True)
    save = kwargs.get("save", False)
    savefile = kwargs.get("savefile", "EQcorrscan_figure.png")
    if save:
        path = os.path.dirname(savefile)
        os.makedirs(path, exist_ok=True)
    return_fig = kwargs.get("return_figure", False)
    size = kwargs.get("size", (10.5,10))#(10.5, 7.5))
    fig.set_size_inches(size)
    if save:
        fig.savefig(savefile, bbox_inches="tight", dpi=130)
        print("Saved figure to {0}".format(savefile))
    if show:
        plt.show(block=True)
    if return_fig:
        return fig
    fig.clf()
    plt.close(fig)
    return None

##############################################################################
def phase_pre_event(path, outpath='.', **kwargs):
    '''
    each event of the catalog has how many phases.
    show avrege phases pre event of the catalog.
    show avrege p-phases and s-phases pre event of the catalog.
    all result show in a plot.
    '''
    list_fpath = glob.glob(path)
    dictionary = {}
    for fpath in list_fpath:
        name = os.path.basename(fpath)
        dictionary[name] = json.load(open(fpath))
    ymin, ymax, xmax = 100, 0, 0
    for key, val in dictionary.items():
        ph_pre_ev = list(val['phases_in_each_event'].keys())
        ph_pre_ev = [int(_) for _ in ph_pre_ev]
        ph_pre_ev_min = min(ph_pre_ev)
        ph_pre_ev_max = max(ph_pre_ev)
        ymin = min(ymin, ph_pre_ev_min-1)
        ymax = max(ymax, ph_pre_ev_max+1)
        xmax = max(xmax, max(val['phases_in_each_event'].values())+2)
    xlim = [0, xmax]
    ylim = [ymin, ymax]
    for name, val in dictionary.items():
        kwargs.update(savefile=join(outpath, f'{name}.png'))
        num_events = val['num_events']
        phases_counter = val['phases_counter']
        num_all_phases = val['num_all_phases']
        phases_in_each_event = val['phases_in_each_event']
        #######
        phases_in_each_event = collections.OrderedDict(sorted(phases_in_each_event.items(), key=lambda x: int(x[0])))
        bins = list(phases_in_each_event.keys())
        bins = [int(_) for _ in bins]
        values = list(phases_in_each_event.values())
        fig = plt.figure(figsize=(8, 6))
        #plt.grid()
        plt.barh(bins, values, edgecolor='black', linewidth=1.2)
        phase_pre_event = num_all_phases / num_events
        plt.hlines(phase_pre_event, 0, xlim[1],
                   colors='g',
                   label='%d/%d = %.2f (ph/ev)'
                   % (num_all_phases, num_events, phase_pre_event))
        for key, val in phases_counter.items():
            if 'A' in key:
                continue
            phase_pre_event = round(val/num_events, 2)
            if phase_pre_event == 0:
                continue
            if 'P' in key:
                c = 'r'
            elif 'S' in key:
                c = 'b'
            else:
                c = [(random.random(), random.random(), random.random())]
            plt.hlines(phase_pre_event, 0, xlim[1], colors=c,
                       label='%d/%d = %f (%s-ph/ev)'
                       % (val, num_events, phase_pre_event, key))
        plt.ylabel('number of phases in event', fontsize=17)
        plt.xlabel('number of events', fontsize=17)
        plt.legend(loc=4, prop={'size': 20})
        plt.yticks(range(ylim[0], ylim[1]))
        plt.xticks(range(xlim[0], xlim[1]))
        plt.xlim(xlim)
        plt.ylim(ylim)
        title = name.split('run')[-1]
        title = splitext(title)[0]
        qcname = '' #'rate of phases pre event\n'
        plt.title(qcname + title + ' HZ', fontsize=25)#, weight='bold')
        ax = plt.gca()
        ax.xaxis.set_tick_params(labelsize=15)
        ax.yaxis.set_tick_params(labelsize=15)
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
        fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover


##############################################################################
def phase_counter(path, outpath='.', **kwargs):
    '''
    how many p-phases and s-phases are in catalog.
    return: matplotlib.plot
    '''
    list_fpath = glob.glob(path)
    dictionary = {}
    for fpath in list_fpath:
        name = os.path.basename(fpath)
        dictionary[name] = json.load(open(fpath))
    ymin, ymax, = 0, 0
    for key, val in dictionary.items():
        num_phases = list(val.values())
        min_phases = min(num_phases)
        max_phases = max(num_phases)
        ymin = min(ymin, min_phases-1)
        ymax = max(ymax, max_phases + 1)
    ylim = [ymin, ymax]
    for name, counter in dictionary.items():
        kwargs.update(savefile=join(outpath, f'{name}.png'))
        counter = collections.OrderedDict(sorted(counter.items()))
        bins = list(counter.keys())
        values = list(counter.values())
        fig = plt.figure(figsize=(8, 6))
        plt.bar(bins, values)
        for ii in range(len(bins)):
            plt.text(x=ii, y=values[ii], s=values[ii], size=16,
                     horizontalalignment='center', verticalalignment='bottom')
        plt.xlabel('phase name')
        plt.ylabel('count of phase in catalog')
        plt.yticks(values)
        plt.ylim(ylim)
        title = name.split('run')[-1]
        title = splitext(title)[0]
        qcname = '' #'P vs S\n'
        plt.title(qcname + title)
        fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover


##############################################################################
def hist_correlation(path, column=1, outpath='.', **kwargs):
    '''
    draw hsitogram of detect_vals of party
    '''
    list_fpath = glob.glob(path)
    dictionary = {}
    for fpath in list_fpath:
        name = os.path.basename(fpath)
        array = np.genfromtxt(fname=fpath, delimiter=None, skip_header=2)
        cc = array[:, 0]
        rate = array[:, column]
        dictionary[name] = dict(cc=cc, rate=rate)
    ymin, ymax, xmax = 100, 0, 0
    for key, val in dictionary.items():
        cc = val['cc']
        delta = np.diff(cc)[0]
        rate = val['rate']
        notzero = [i for i, e in enumerate(rate) if e != 0]
        ccmin = cc[notzero[0]]
        ccmax = cc[-1]
        ymin = min(ymin, ccmin)
        ymax = max(ymax, ccmax+delta)
        xmax = max(xmax, max(rate)+1)
    xlim = [0, xmax]
    ylim = [ymin, ymax]
    for name, val in dictionary.items():
        cc = val['cc']
        rate = val['rate']
        kwargs.update(savefile=join(outpath, f'{name}.png'))
        fig = plt.figure(figsize=(8, 6))
        delta = np.diff(cc)[0]
        plt.barh(cc, rate, align='edge', height=delta, edgecolor='black', linewidth=1.2)
        plt.xticks(np.arange(xlim[0], xlim[1], 2))
        plt.yticks(np.arange(ylim[0], ylim[1]+delta, delta))
        plt.xlim(xlim)
        plt.ylim(ylim)
        #plt.grid()
        plt.xlabel('Number of detections', fontsize=17)
        plt.ylabel('Correlation Coefficient', fontsize=17)
        title = name.split('run')[-1]
        title = splitext(title)[0]
        qcname = '' #'CC of detections\n'
        plt.title(qcname + title+' HZ', fontsize=25)#, weight='bold')
        ax = plt.gca()
        ax.xaxis.set_tick_params(labelsize=15)
        ax.yaxis.set_tick_params(labelsize=15)
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
        fig = _finalise_figure(fig=fig, **kwargs)


##############################################################################
def self_detection(path, outpath='.', **kwargs):
    '''
    how many self detections (full detection)
    and
    how many new detections

    self detections select if

    number of channel of detection
    EQUAL TO
    detection value of sum of cross-correlation detection.
    '''
    list_fpath = glob.glob(path)
    dictionary = {}
    for fpath in list_fpath:
        name = os.path.basename(fpath)
        dictionary[name] = json.load(open(fpath))
    ymin, ymax, = 0, 0
    for key, val in dictionary.items():
        num_phases = list(val.values())
        min_phases = min(num_phases)
        max_phases = max(num_phases)
        if ymin > min_phases:
            ymin = min_phases - 1
        if ymax < max_phases:
            ymax = max_phases + 1
    ylim = [ymin, ymax]
    for name, val in dictionary.items():
        kwargs.update(savefile=join(outpath, f'{name}.png'))
        self_detection = val['self_detection']
        num_refrence_events = val['reference_detections']
        new_detection = val['new_detection']
        fig = plt.figure(figsize=(8, 6))
        plt.bar(['Self-Detection', 'New-Detection'],
                [self_detection, new_detection],
                label='new catalog', edgecolor='black', linewidth=1.2)
        plt.bar(['Self-Detection'],
                [num_refrence_events],
                color='g', width=0.4,# hatch='|',
                label='Reference catalog', edgecolor='black', linewidth=1.2)

        plt.yticks([self_detection,
                    new_detection,
                    num_refrence_events])
        plt.ylim(ylim)
        plt.ylabel('Number of detections', fontsize=17)
        title = name.split('run')[-1]
        title = splitext(title)[0]
        qcname = '' #'Self-detection VS New-detection\n'
        plt.title(qcname + title + ' HZ', fontsize=25)#, weight='bold')
        plt.legend(loc=2)
        ax = plt.gca()
        ax.xaxis.set_tick_params(labelsize=15)
        ax.yaxis.set_tick_params(labelsize=15)
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
        fig = _finalise_figure(fig=fig, **kwargs)


##############################################################################
def ps_delta(catalog, method='network', **kwargs):
    '''
    interval between p and s phases of events in same stations.
    for select length of template phases.
    '''
    list_ps_delta = []
    stations_ps_delta = {}
    for ev in catalog:
        stations_phases = {}
        for pick in ev.picks:
            if (pick.phase_hint is None) or ('A' in pick.phase_hint) or (pick.phase_hint == ''):
                continue
            station_name = pick.waveform_id.station_code
            phase = pick.phase_hint
            if station_name not in stations_phases.keys():
                stations_phases[station_name] = {}
            stations_phases[station_name][phase[0]] = pick.time
        for station, phases in stations_phases.items():
            if len(phases) == 2:
                ps_delta = phases['S'] - phases['P']
                list_ps_delta.append(ps_delta)
                if station not in stations_ps_delta.keys():
                    stations_ps_delta[station] = []
                stations_ps_delta[station].append(ps_delta)
    if method == 'network' or method == 'both':
        print('max:', max(list_ps_delta))
        print('min:', min(list_ps_delta))
        counts, bins = np.histogram(list_ps_delta, bins=40)
        fig = plt.figure(figsize=(8, 6))
        ax = plt.gca()
        ax.yaxis.set_tick_params(labelsize=15)
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
        plt.hist(bins[:-1], bins, weights=counts, edgecolor='black', linewidth=1.2)
        plt.xticks(list(range(round(max(bins))+1)), fontsize=15)
        plt.xlabel('Interval of P-S pairs [S]', fontsize=17)
        plt.ylabel('Abundance [Count]', fontsize=17)
        plt.title('Ilam reference catalog', fontsize=25)#, weight='bold')
        kwargs.update(savefile=join(kwargs['path'], 'network.png'))
        fig = _finalise_figure(fig=fig, **kwargs)
    if method == 'stations' or method == 'both':
        for station, deltas in stations_ps_delta.items():
            print(station)
            print('max:', max(deltas))
            print('min:', min(deltas))
            counts, bins = np.histogram(deltas, bins=40)
            fig = plt.figure(figsize=(8, 6))
            plt.hist(bins[:-1], bins, weights=counts)
            plt.xlabel('Interval of P-S pairs [S]')
            plt.ylabel('Abundance')
            plt.title(station)
            kwargs.update(savefile=join(kwargs['path'], f'{station}.png'))
            fig = _finalise_figure(fig=fig, **kwargs)


def interval_events(party=None, catalog=None, times=None, max_time=None, bins=100,
                    **kwargs):
    times = times or []
    if catalog:
        for event in catalog:
            try:
                time = event.origins[0].time
                times.append(time)
            except Exception as error:
                print(error)
    if party:
        for family in party:
            for detect in family:
                times.append(detect.detect_time)
    times.sort()
    max_time = max_time or max(np.diff(times))
    xticks = np.arange(0, max_time+bins, 4*max_time/bins)
    dt = [times[ii+1]-times[ii] for ii in range(len(times)-1)]
    dt.sort()
    dt = np.array(dt)
    if max_time:
        idx = (np.abs(dt - max_time)).argmin()
        dt = dt[:idx]
    fig = plt.figure(figsize=(8, 6))
    counts, bins = np.histogram(dt, bins=bins)
    plt.hist(bins[:-1], bins, weights=counts)
    plt.xticks(xticks)
    plt.ylabel('number of events')
    plt.xlabel('interval of events')
    kwargs.update(
        title='delta of origin time' + kwargs.get('title', '')
        )
    fig = _finalise_figure(fig=fig, **kwargs)


def detection_pre_template(party, return_data=False, **kwargs):
    detections = {}
    for family in party:
        detections[family.template.name] = len(family)
    detections = collections.OrderedDict(sorted(detections.items(), key=lambda e: int(e[0])))
    bins = list(detections.keys())
    values = list(detections.values())
    fig = plt.figure(figsize=(8, 6))
    plt.barh(bins, values, label=f'{len(party.get_catalog())} detections\n{len(party.families)} templates')
    for ii in range(len(bins)):
        plt.text(x=values[ii], y=ii, s=values[ii], size=16,
                 horizontalalignment='left', verticalalignment='center')
    plt.xlabel('Number of detections')
    plt.ylabel('template name')
    plt.legend()
    kwargs.update(title='number of detection with each template' +
                  kwargs.get('title', ''))
    plt.xlim([0, 20])
    fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover
    if return_data:
        return bins, values
    return fig


##############################################################################
def hist_rms(path, outpath='.', log=True, min_rate=2, **kwargs):
    '''
    draw hsitogram of detect_vals of party
    '''
    list_fpath = glob.glob(path)
    dictionary = {}
    for fpath in list_fpath:
        name = os.path.basename(fpath)
        array = np.genfromtxt(fname=fpath, delimiter=None, skip_header=2)
        rms = array[:, 0]
        rate = array[:, 1]
        dictionary[name] = dict(rms=rms, rate=rate)
    ymaxs, xmins, xmaxs = [], [], []
    for key, val in dictionary.items():
        rms = val['rms']
        delta = np.diff(rms)[0]
        rate = val['rate']
        if log:
            rate[rate <= min_rate] = 0
        notzero = [i for i, e in enumerate(rate) if e >= min_rate]
        minrms = rms[notzero[0]]
        maxrms = rms[notzero[-1]]
        xmins.append(minrms-delta)
        xmaxs.append(maxrms+delta)
        ymaxs.append(max(rate+1))
    xlim = [min(xmins), max(xmaxs)]
    ylim = [1, max(ymaxs)]
    for name, val in dictionary.items():
        rms = val['rms']
        rate = val['rate']
        fig = plt.figure(figsize=(8, 6))
        delta = np.diff(rms)[0]
        plt.bar(rms, rate, align='edge', width=delta, log=log, edgecolor='black', linewidth=1.2)
        plt.xticks(np.arange(xlim[0], xlim[1]+delta, delta))
        if not log:
            step = ylim[1]//10
            plt.yticks(np.arange(ylim[0], ylim[1]+1, step))
        plt.ylim(ylim)
        plt.xlim([-2, 10])#xlim)
        plt.xlabel('RMS', fontsize=17)
        plt.ylabel('Number of phases', fontsize=17)
        title = name.split('run')[-1]
        title = splitext(title)[0]
        qcname = '' #'RMS phases\n'
        plt.title(qcname + title[:-4]+' HZ' , fontsize=25)#, weight='bold')
        #plt.grid()
        ax = plt.gca()
        ax.yaxis.set_tick_params(labelsize=15)
        ax.xaxis.set_tick_params(labelsize=15)
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(2)
        kwargs.update(savefile=join(outpath, f'{name}.png'))
        fig = _finalise_figure(fig=fig, **kwargs)


##############################################################################
def logging_exceptions(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
    except Exception as error:
        print(f"{f}: {error}")
       # raise

'''
if __name__=='__main__':
    import sys
    if '--path' in sys.argv:
        path = sys.argv[sys.argv.index('--path') + 1]
        run(path)
    else:
        pass
'''
