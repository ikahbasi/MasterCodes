#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 23:16:44 2019

@author: imon
"""
#origin time of earthquake
lat_event = 34.877
lon_event = 45.841
depth_event = 18
################### import library ###################
import matplotlib.pyplot as plt
import os
from obspy import read
from obspy.io.xseed import Parser
#from matplotlib.pyplot import figure
save = True
show = False
size = 30
############ get lat & lon of each station
def get_lat_long(resp):
    blk = resp.blockettes
    List = []
    stations = {}
    for ii in blk[50]:
        if ii.station_call_letters in List:
            continue
        List.append(ii.station_call_letters)
        stations[ii.station_call_letters] = [ii.latitude,ii.longitude]
    return stations
########### correct detail of trace
def correct_detail(tr):
    tr.stats.network = 'IR'
    if tr.stats.channel == 'B Z':
        tr.stats.channel = 'SHZ'
    elif tr.stats.channel == 'B N':
        tr.stats.channel = 'SHZ'
    else:
        tr.stats.channel = 'SHE'
    return tr
############# def #############
def iiees_plot_rm_resp(tr,resp):
    time_window = tr.times().tolist()
    name =  str(tr.id)
    ##### preper for remove resp
    tr.detrend()
    tr.filter('bandpass', freqmin=0.005, freqmax=24)
#    tr.filter("highpass", freq=0.1)
    ##### dispelacement
    tr_copy = tr.copy()
    tr_copy.simulate(seedresp={'filename': resp, 'units': "DIS"})
    tr_copy.filter('bandpass', freqmin=0.005, freqmax=24)
    tr_rm_resp_disp = tr_copy.data.tolist()
    
    ##### velocity
    tr_copy = tr.copy()
    tr_copy.simulate(seedresp={'filename': resp, 'units': "VEL"})
    tr_rm_resp_vel = tr_copy.data.tolist()
    #### acceleration
    tr_copy = tr.copy()
    tr_copy.simulate(seedresp={'filename': resp, 'units': "ACC"})
    tr_rm_resp_acc = tr_copy.data.tolist()
    
    ############## subplot of origin_DISP_VEL_ACC
    #### make subplot
    f = plt.figure(figsize=(25,20))#,dpi=100)
    plt.subplots_adjust(hspace=0.6)
    f.suptitle(name,fontsize=40,fontweight='black')
    #### ORIGIN
    f.add_subplot(411).plot(time_window, st[0].data.tolist(), color='black',lw=1.3)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('count',fontsize=size,fontweight='black')
    plt.title('origin trace', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    #### DISP
    f.add_subplot(412).plot(time_window, tr_rm_resp_disp, color='green',lw=1.3)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('displacement',fontsize=size,fontweight='black')
    plt.title('displacement', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    #### VEL
    f.add_subplot(413).plot(time_window, tr_rm_resp_vel, color='blue',lw=1.3)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('velocity',fontsize=size,fontweight='black')
    plt.title('velocity', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    #### ACC
    f.add_subplot(414).plot(time_window, tr_rm_resp_acc, color='red',lw=0.9)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('acceleration',fontsize=size,fontweight='black')
    plt.title('acceleration', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    
    ###
    if show:
        f.show()
    if save:
        path = './output/rmresp/'
        if not os.path.isdir(path): os.makedirs(path)
        f.savefig(path+str(tr.id)+'_subplot_'+'.png') # save image(optional)
    
    ############# plot all trace in one
    plt.figure(figsize=(30,10))#,dpi=100)
    plt.plot(time_window,tr_rm_resp_acc,'r',lw=0.6,label= 'ACC')
    plt.plot(time_window,tr_rm_resp_vel,'b',lw=1, label ='VELOCITY')
    plt.plot(time_window,tr_rm_resp_disp,'g',lw=1.2,label='DISP')
    plt.xlabel('time',fontsize=size+15,fontweight='black')
    plt.ylabel('amplitude',fontsize=size+15,fontweight='black')
    plt.suptitle(name,fontsize=40,fontweight='black')
    plt.tick_params(labelsize=size)
    plt.legend(fontsize=30)
    ###
    if show:
        plt.show()
    if save:
        plt.savefig(path+str(tr.id)+'_all.in.one_'+'.png') # save image(optional)
    


############# set some parameter #############
st = read('./IR_waveform_collecton/IR.SBZV..SHE.20171112.181000.mseed')
tr = st[0]
if show:
    tr.plot()
########### correction
tr = correct_detail(tr)
print tr.id
############ read dataless
#resp = Parser('./IR_RESP/RESP.'+str(tr.id))
resp = Parser('./IR_resp/IR_2018-05-20.dlsv')
##################
iiees_plot_rm_resp(tr,resp)
'''
########### deterend and filter befor correct response
#tr.filter("highpass", freq=1.0)
tr.detrend(type='linear')

########### correct response
iiees_plot_rm_resp(tr)
#tr.plot()
########### get max for magnitude
ampl = max(abs(tr.data))

########### get location of station for magnitude
location = stations[tr.stats.station]
distance = locations2degrees(lat_event , lon_event , 
                             location[0] , location[1])

########### calculate magnitude
mw = calculate_mwp_mag(ampl,distance)

from math import log10
if distance<6:
    a = 0.018
    b = 2.17
    ml = log10(ampl * 1000) + a * distance*111 + b
    print(ml)
'''
