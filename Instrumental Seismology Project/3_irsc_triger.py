#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 19:22:39 2019

@author: imon
"""
show = False
save = True
import glob
from obspy import read
from obspy.signal.trigger import classic_sta_lta
#from obspy.signal.trigger import trigger_onset
from obspy.io.xseed import Parser
if save:
    from change_obspy import my_plot_trigger
if show:
    from obspy.signal.trigger import plot_trigger

count = 0
#list of target trace
List = glob.glob('./IR_waveform_collecton/*Z*')
for dir in List:
    st = read(dir)
    tr = st[0]
    ################### triger STA/LTA
    triger_on = 30
    triger_off = 0.5
    df = tr.stats.sampling_rate
    try:
        cft = classic_sta_lta(tr , int(10 * df) , int(400 * df))
    #### save or show triger###
        if show:
            plot_trigger(tr , cft , triger_on , triger_off)
        if save:
            my_plot_trigger(tr , cft , triger_on , triger_off,count) #save#
    #    ###
    #    onset_triger = trigger_onset(cft , triger_on , triger_off)[0][0]
    #    t_arrival_p[station_name] = [lat_station , long_station ,onset_triger]
        count +=1
#        if count == 10:
#            break
    except:
        print '\n>>> >>>',tr.id, 'fail \n'
#    break
