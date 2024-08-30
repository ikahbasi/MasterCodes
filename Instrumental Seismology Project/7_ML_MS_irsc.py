# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 15:56:22 2019

@author: Kahbasi
"""
save = True

from obspy.geodetics.base import locations2degrees
from obspy.io.xseed import Parser
#from for_iiees_inv_plot import make_iiees_location_station
from obspy.geodetics import gps2dist_azimuth
from math import log10
from obspy import read
######### make directory for output
if save:
    import os
    path = './output/text/'
    if not os.path.isdir(path): os.makedirs(path)
    ftext = open(path+'ML_&_MS(irsc).txt','w')
######### epicenter
lat_event = 34.877
lon_event = 45.841
######### for run faster make list name_lat_lon
name_station = ['AKL','AMIS','ANJ','AZR','GLO','KGS1','KLNJ','LMD1',
                'MAHB','MEH','MRD','NGCH','QABG','SBZV','SRVN','TBJM']

lat_station = [36.6 , 31.7 , 35.5 , 37.7 , 36.5 , 34.5 , 31.0 , 27.3 ,
               36.8 , 31.4 , 38.7 , 25.4 ,  35.7 , 36.4 , 27.4 , 35.3 ]

lon_station = [58.8 , 49.3 , 53.9 , 46.0 , 53.8 , 45.6 , 51.6 , 53.2 ,
               45.7 , 54.6 , 45.7 , 61.1 , 49.6 , 57.6 , 62.4 , 60.3 ]

######### station that calculat magnitude on them
target = ['MAHB','QABG','KLNJ']
lat = []
lon = []
for name in target:
    lat.append(lat_station[name_station.index(name)])
    lon.append(lon_station[name_station.index(name)])
######### woodanderson response for ML
paz_wa = {'sensitivity': 2800, 'zeros': [0j], 'gain': 1,
          'poles': [-6.2832 - 4.7124j, -6.2832 + 4.7124j]}
########### correct detail of trace
def correct_detail(tr):
    tr.stats.network = 'IR'
    
    if tr.stats.channel == 'B Z':
        tr.stats.channel = 'SHZ'
        
    if tr.stats.channel == 'B N':
        tr.stats.channel = 'SHN'
        
    if tr.stats.channel == 'B E':
        tr.stats.channel = 'SHE'
    return tr
##################
def get_ampl_ml(tr,resp):
    tr.detrend()
    tr.filter('bandpass', freqmin=0.01, freqmax=24.0)
    try:
        tr.simulate(seedresp={'filename': resp, 'units': "DISP"})
        tr.filter('bandpass', freqmin=0.01, freqmax=24.0)
#        tr.plot()
    except:
        print 'imon: cant get DIS with response in ',tr.id
    
    tr.simulate(paz_simulate=paz_wa, water_level=10)
    ampl = max(abs(tr.data))
    return ampl
##################
def get_ampl_ml2(tr,resp):
    tr.detrend()
    tr.filter('bandpass', freqmin=0.01, freqmax=24.0)
    try:
        tr.simulate(seedresp={'filename': resp, 'units': "DISP"})
        tr.filter('bandpass', freqmin=0.01, freqmax=24.0)
#        tr.plot()
    except:
        print 'imon: cant get DIS with response in ',tr.id
    ampl = max(abs(tr.data))
    return ampl
##################
def get_ampl_mw(tr,resp):
    tr.detrend()
    tr.filter('bandpass', freqmin=0.01, freqmax=24.0)
    try:
        tr.simulate(seedresp={'filename': resp, 'units': "DISP"})
        tr.filter('bandpass', freqmin=0.01, freqmax=24.0)
    except:
        print 'imon: cant get DIS with response in ',tr.id
    ampl = max(abs(tr.data))
    return ampl
################ ML
def ML(ampE,ampN,distance):
    ampl = max(amplN,amplE)
    if distance < 60:
        a = 0.018
        b = 2.17
    else:
        a = 0.0038
        b = 3.02
    ml = log10(ampl * 1000) + a * distance + b
    
    print 'in ', tr_E.id[0:-5],' Ml: ',ml
    if save:
        ftext.write('ML in '+ tr_E.id[0:-5]+' station is: '+str(round(ml,2))+'\n\n')
############## MS   
def MS(ampl,distance):
    T =20
    MS = log10((ampl*10**6)/T) + 1.66*log10(distance) + 3.3
    print 'in ', tr_E.id[0:-5],' Ms: ',MS
    if save:
        ftext.write('MS in '+ tr_E.id[0:-5]+' station is: '+str(round(MS,2))+'\n')
        
################## code    
for name in target:
    tr_Z = read("./IR_waveform_collecton/IR."+name+'..SHZ*')
    tr_Z = tr_Z[0]
    tr_Z = correct_detail(tr_Z)
    
    tr_N = read("./IR_waveform_collecton/IR."+name+'..SHN*')
    tr_N = tr_N[0]
    tr_N = correct_detail(tr_N)
    
    tr_E = read("./IR_waveform_collecton/IR."+name+'..SHE*')
    tr_E = tr_E[0]
    tr_E = correct_detail(tr_E)
    
    resp_Z = Parser('./IR_RESP/RESP.'+str(tr_Z.id))
    resp_N = Parser('./IR_RESP/RESP.'+str(tr_N.id))
    resp_E = Parser('./IR_RESP/RESP.'+str(tr_E.id))
    ##### preper for remove resp
    amplN = get_ampl_ml(tr_N,resp_N)
    amplE = get_ampl_ml(tr_E,resp_E)
    amplZ = get_ampl_mw(tr_Z,resp_Z)
    ##### get lat & lon target from list
    lat0 = lat[target.index(tr_E.stats.station)]
    lon0 = lon[target.index(tr_E.stats.station)]
    ####### calculat MS
    distance = locations2degrees(lat_event, lon_event, lat0 , lon0)
    MS(amplZ,distance)
    ####### calculat ML
    distance, az, baz = gps2dist_azimuth(lat_event, lon_event, lat0 , lon0)
    distance = distance / 1000
    ML(amplE,amplN,distance)
    
#    amplN = get_ampl_ml2(tr_N,resp_N)
#    amplE = get_ampl_ml2(tr_E,resp_E)
#    ml2 = log10(max(amplE,amplN) * 10**3) + 3*log10(distance) - 3.38
#    print 'in ', tr_E.id[0:-5],' Ml2: ',ml2
#    ftext.write('ML2 in '+ tr_E.id[0:-5]+' station is: '+str(round(ml2,2))+'\n')
ftext.close()
