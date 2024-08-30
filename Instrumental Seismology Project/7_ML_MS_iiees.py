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
    ftext = open(path+'ML_&_MS(iiees).txt','w')
######### epicenter
lat_event = 34.877
lon_event = 45.841
######### for get name_lat_lon from response file
#stations = make_iiees_location_station()
######### for run faster make list name_lat_lon
name_station = [u'AHRM', u'ASAO', u'BJRD', u'BNDS', u'BSRN', u'CHBR',
                u'CHTH', u'DAMV', u'GHIR', u'GHVR', u'GIDE', u'GRMI',
                u'GTMR', u'ILBA', u'KHMZ', u'KRBR', u'MAKU', u'MRVT',
                u'NASN', u'RMKL', u'SHGR', u'SHRO', u'SHRT', u'SNGE',
                u'SRSL', u'TABS', u'THKV', u'YZKH', u'ZHSF', u'ZNJK']

lat_station = [28.8654, 34.5479, 37.7, 27.3994, 31.9651, 25.5955, 35.9078,
               35.6304, 28.2856, 34.48, 36.923, 38.8081, 32.4705, 33.624,
               33.7396, 29.9824, 39.3549, 37.6593, 32.7992, 30.982, 32.1084,
               36.0085, 33.6462, 35.0925, 36.2122, 33.649, 35.9157, 32.3901,
               29.611, 36.6709]

lon_station = [51.2973, 50.0255, 57.4107, 56.1714, 59.1259, 60.4821, 51.1259,
               51.9715, 52.9867, 51.2453, 49.9101, 47.8938, 49.1123, 46.207,
               49.9642, 56.7604, 44.6835, 56.0892, 52.8083, 49.809, 48.8014,
               56.0129, 60.291, 47.347, 45.4339, 57.119, 50.8788, 54.5916,
               60.7753, 48.685]
######### station that calculat magnitude on them
#  'ILBA','SNGE',,'ASAO','KHMZ'
target = ['ZNJK','SNGE','ASAO','KHMZ']
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
    tr.stats.network = 'BI'
    
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
################ MS
def MS(ampl,distance):
    T =20
    MS = log10((ampl*10**6)/T) + 1.66*log10(distance) + 3.3
    print 'in ', tr_E.id[0:-5],' Ms: ',MS
    if save:
        ftext.write('MS in '+ tr_E.id[0:-5]+' station is: '+str(round(MS,2))+'\n')
        
################## code
st = read("./BI_waveform/*")
for name in target:
    print '\n',name,'\n'
    st2 = st.select(station=name)
    
    print st2
    print '\n'

    tr_Z = st2.select(component='Z')
    tr_Z = tr_Z[0]
    tr_Z = correct_detail(tr_Z)
    
    tr_N = st2.select(component='N')
    tr_N = tr_N[0]
    tr_N = correct_detail(tr_N)
    
    tr_E = st2.select(component='E')
    tr_E = tr_E[0]
    tr_E = correct_detail(tr_E)
    
    resp_Z = Parser('./BI_RESP/RESP.'+str(tr_Z.id))
    resp_N = Parser('./BI_RESP/RESP.'+str(tr_N.id))
    resp_E = Parser('./BI_RESP/RESP.'+str(tr_E.id))
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
    
    
ftext.close()
