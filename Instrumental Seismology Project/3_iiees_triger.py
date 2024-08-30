#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 09:25:19 2019

@author: imon
"""
show = False
save = True
from obspy import read
from obspy.signal.trigger import trigger_onset
from obspy.signal.trigger import classic_sta_lta
from obspy import Stream
if save:
    from change_obspy import my_plot_trigger
if show:
    from obspy.signal.trigger import plot_trigger
##################
def correct_detail(tr):
    tr.stats.network = 'BI'
    if tr.stats.channel == 'B Z':
        tr.stats.channel = 'SHZ'
    elif tr.stats.channel == 'B N':
        tr.stats.channel = 'SHN'
    elif tr.stats.channel == 'B E':
        tr.stats.channel = 'SHE'
    return tr
####################
st =read('./BI_waveform/*')


t_arrival_p={}
list_station=[]
count = 0
for tr in st:
############# triger phase #############
    if str(tr.stats.channel) != 'B Z':
        continue
    st2 = Stream()
    tr = correct_detail(tr)
    ###### for extention trace
    trcopy = tr.copy()
    st2 += tr
    t = tr.stats.starttime
    trcopy.trim(t, t + 10)
    for ii in range(55):
        trcopy.stats.starttime = trcopy.stats.starttime - 5
        tr = trcopy+tr
        st2.append(tr)
    st2.merge(method=1)
    tr = st2[0]
    #######
    station_name = str(tr.stats.station)
    list_station.append(station_name)
    triger_on = 3
    triger_off = 0.5
    df = tr.stats.sampling_rate
    cft = classic_sta_lta(tr , int(30 * df) , int(300 * df))
    try:
        onset_triger = trigger_onset(cft , triger_on , triger_off)[0][0]
    except:
        print 'i skipped ',tr.id
        continue
    if show:
        plot_trigger(tr , cft , triger_on , triger_off)
    if save:
        my_plot_trigger(tr , cft , triger_on , triger_off,count)
    
#    t_arrival_p[station_name] = [lat_station , long_station ,onset_triger]
    count +=1
#    break
#    if count == 10:
#        break
