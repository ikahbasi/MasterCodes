#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 21:49:02 2019

@author: imon kahbasi
"""
#### plot show or save
show = False
save =  True

'''
http://www.iiees.ac.ir/fa/eventspec/?eqid=103758
sarpole zahab m=7.3
Lat_event = 34.877 Lon_event = 45.841
'''
#origin time of earthquake
time_event = '2017-11-12 18:18:17.8'
lat_event = 34.877
lon_event = 45.841
depth_event = 18
################### import library ###################
from obspy import UTCDateTime
from obspy.taup import TauPyModel
from obspy.geodetics.base import locations2degrees
from obspy.clients.fdsn import Client
import lineid_plot
import matplotlib.pyplot as plt
from obspy.realtime.signal import calculate_mwp_mag
from obspy.signal.trigger import trigger_onset
from obspy.signal.trigger import classic_sta_lta
from obspy.core.stream import Stream

if save:
    from change_obspy import my_plot_trigger
    import os
if show:
    from obspy.signal.trigger import plot_trigger
#import numpy as np
############# set some parameter #############
client = Client("IRIS")
origine_time = UTCDateTime(time_event)
end_time = origine_time + 3600*4
list_magnitude = []
stream = Stream()
t_arrival_p={}
List_station=[]
if save:
    path = './output/text/'
    if not os.path.isdir(path): os.makedirs(path)
    ftext = open(path+'global.txt','w')
############# define model of earth #############
model = TauPyModel(model='iasp91')
    
############# get inventory #############
inventory = client.get_stations(network = "IU", station = "*",
                                starttime = origine_time,
                                endtime = end_time,
                                latitude = lat_event,
                                longitude = lon_event,
                                maxradius = 50)
if show:
    inventory.plot(color = '65748' , projection = 'ortho')
if save:
#    fig2 = plt.figure(figsize = (20,15))
#    fig2, ax = plt.subplots(figsize=(7,7))
    from pylab import rcParams
    rcParams['figure.figsize'] = 15, 10
    fig = inventory.plot(color = '65748' , projection = 'local',show=False)
#    fig.set_size_inches(15,10)
    path = './output/plot_inv/'
    if not os.path.isdir(path): os.makedirs(path)
    fig.savefig(path+'global_station.png',dpi = 100) #save#

#########################
L = len(inventory[0])
if save:
    ftext.write('progress for ' + str(L) + ' station' + '\n')
    
print 'progress start for ',L,'station'
for jj in range(0,L):
    ############# station parameter #############
    station = inventory[0][jj]
    lat_station = station.latitude
    long_station = station.longitude
    station_name = station.code
    
    print str(jj+1)+'_station "'+station_name+'"'
    
    ############# epicenter distance in degree #############
    distance = locations2degrees(lat_event , lon_event , 
                                 lat_station , long_station)
    
    print 'epicenteral distance in degree is:', distance
    
    if save:
        ftext.write('\n'+str(jj+1)+'_station: "'+station_name+'"')
        ftext.write('\n'+'epicenteral distance(degree) is: '+ str(round(distance,3)))
    ############# phase arrival #############
    arrivals = model.get_travel_times(source_depth_in_km = depth_event, 
                                      distance_in_degree = distance)
#    print arrivals
    ############# select time & name of all phase arrivall #############
    time_arrivals = []
    name_arrivals = []
    for arrival in arrivals:
        if arrival.name in name_arrivals:
            continue
        name_arrivals.append(arrival.name)
        time_arrivals.append(arrival.time + 360)
        
    ############# get data from station #############
    end_of_waveform = origine_time + time_arrivals[-1] 
    try:
        st = client.get_waveforms("IU", station_name, "00", "LHZ", 
                                  origine_time-360,
                                  end_of_waveform,
                                  attach_response=True)
        if show:
            st.plot()
        List_station.append(station_name)
    except:
        print 'NOTE: waveform not exist'
        print '-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-','\n'
        if save:
            ftext.write('\n'+'NOTE: waveform not exist')
            ftext.write('\n'+'-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-'+'\n')
        continue
    ###################################################
    tr = st[0]
    stream += tr
    
    ############# trace to array for plot #############
    tr_d = tr.data.tolist()
    
    ############# time window for plot #############
    time_window = tr.times().tolist()
    
    ############# plot trace and phases #############
    fig = plt.figure(figsize=(22 , 8))
    T = int(time_arrivals[0]) - 50 #for better plot and incress resolotion
    lineid_plot.plot_line_ids(time_window[T:] , tr_d[T:] , time_arrivals , name_arrivals , box_axes_space=0.11 , fig=fig)
    plt.title(tr.id , loc='right', fontweight='black',fontsize = 20)
    plt.tick_params(labelsize=20)
    if show:
        lineid_plot.lineid_plot.plt.show()   
    ############# save each figure #############
    if save:
        path = './output/lineid/'
        if not os.path.isdir(path): os.makedirs(path)
        fig.savefig(path+str(jj+1)+'_'+str(tr.id)+'.png', dpi=100) #save#
    
    ############# triger phase #############
    triger_on = 30
    triger_off = 0.5
    df = tr.stats.sampling_rate
    cft = classic_sta_lta(tr , int(10 * df) , int(400 * df))
    
    #### save or show triger###
    if show:
        plot_trigger(tr , cft , triger_on , triger_off)
    if save:
        my_plot_trigger(tr , cft , triger_on , triger_off,jj) #save#
    ###
    onset_triger = trigger_onset(cft , triger_on , triger_off)[0][0]
    t_arrival_p[station_name] = [lat_station , long_station ,onset_triger]
    
    ############# remove response #############
    pre_filt = (0.005, 0.006, 30.0, 35.0)
    st.remove_response(output='DISP', pre_filt=pre_filt)
    
    ############# mgnitude #############
    ampl = max(abs(tr.data))
    mw = calculate_mwp_mag(ampl,distance)
    print 'magnitude in "'+station_name+'" station is:',mw
    print '-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-','\n'
    if save:
        ftext.write('\n'+'magnitude in "'+station_name+'" is:'+str(round(mw,3)))
        ftext.write('\n'+'-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-'+'\n')
    list_magnitude.append(mw)
    
############# print final magnitude #############
print '*** *** *** FINAL MAGNITUDE:',sum(list_magnitude)/len(list_magnitude),'*** *** ***'
if save:
    ftext.write('\n'+'*** *** FINAL MAGNITUDE:'+str(round(sum(list_magnitude)/len(list_magnitude),3))+' *** ***' )

ftext.close()
