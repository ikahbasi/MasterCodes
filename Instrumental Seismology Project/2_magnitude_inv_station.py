#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:24:47 2019

@author: imon
"""
show = False
save = True
import obspy
from matplotlib.pyplot import figure
from obspy.core.inventory import Inventory, Network, Station, Site


def iiees_make_inventory(name_station,lat_station,lon_station):
    # We'll first create all the various objects. These strongly follow the
    # hierarchy of StationXML files.
    inv = Inventory(
        # We'll add networks later.
        networks=[],
        # The source should be the id whoever create the file.
        source="imon")
    
    net = Network(
        # This is the network code according to the SEED standard.
        code="BI",
        # A list of stations. We'll add one later.
        stations=[],
        description="A test stations.",
        # Start-and end dates are optional.
        start_date=obspy.UTCDateTime(2016, 1, 2))
    
    # This is the station code according to the SEED standard.
    for ii in range(len(name_station)):
        sta = Station(code = name_station[ii],
                      latitude = lat_station[ii],
                      longitude = lon_station[ii],
                      elevation = 345.0,
                      creation_date = obspy.UTCDateTime(2016, 1, 2),
                      site=Site(name = "iran"))
        
    
        net.stations.append(sta)
    inv.networks.append(net)
    
    return inv
#############################################################################
name_station = []
lat_station = []
lon_station = []
name_stations = [u'AHRM', u'ASAO', u'BJRD', u'BNDS', u'BSRN', u'CHBR',
                u'CHTH', u'DAMV', u'GHIR', u'GHVR', u'GIDE', u'GRMI',
                u'GTMR', u'ILBA', u'KHMZ', u'KRBR', u'MAKU', u'MRVT',
                u'NASN', u'RMKL', u'SHGR', u'SHRO', u'SHRT', u'SNGE',
                u'SRSL', u'TABS', u'THKV', u'YZKH', u'ZHSF', u'ZNJK']

lat_stations = [28.8654, 34.5479, 37.7, 27.3994, 31.9651, 25.5955, 35.9078,
               35.6304, 28.2856, 34.48, 36.923, 38.8081, 32.4705, 33.624,
               33.7396, 29.9824, 39.3549, 37.6593, 32.7992, 30.982, 32.1084,
               36.0085, 33.6462, 35.0925, 36.2122, 33.649, 35.9157, 32.3901,
               29.611, 36.6709]

lon_stations = [51.2973, 50.0255, 57.4107, 56.1714, 59.1259, 60.4821, 51.1259,
               51.9715, 52.9867, 51.2453, 49.9101, 47.8938, 49.1123, 46.207,
               49.9642, 56.7604, 44.6835, 56.0892, 52.8083, 49.809, 48.8014,
               56.0129, 60.291, 47.347, 45.4339, 57.119, 50.8788, 54.5916,
               60.7753, 48.685]  

lat_station = []
lon_station = []
######## for magnitude
target = ['ZNJK','SNGE','ASAO','KHMZ']
name_station = target
for name in target:
    lat_station.append(lat_stations[name_stations.index(name)])
    lon_station.append(lon_stations[name_stations.index(name)])
    
inv_iiees = iiees_make_inventory(name_station,lat_station,lon_station)
#########################################################################
def irsc_make_inventory(name_station,lat_station,lon_station):
    # We'll first create all the various objects. These strongly follow the
    # hierarchy of StationXML files.
    inv = Inventory(
        # We'll add networks later.
        networks=[],
        # The source should be the id whoever create the file.
        source="imon")
    
    net = Network(
        # This is the network code according to the SEED standard.
        code="IR",
        # A list of stations. We'll add one later.
        stations=[],
        description="A test stations.",
        # Start-and end dates are optional.
        start_date=obspy.UTCDateTime(2016, 1, 2))
    
    # This is the station code according to the SEED standard.
    for ii in range(len(name_station)):
        sta = Station(code = name_station[ii],
                      latitude = lat_station[ii],
                      longitude = lon_station[ii],
                      elevation = 345.0,
                      creation_date = obspy.UTCDateTime(2016, 1, 2),
                      site=Site(name = "iran"))
        
    
        net.stations.append(sta)
    inv.networks.append(net)
    
    return inv



name_stations = ['AKL','AMIS','ANJ','AZR','GLO','KGS1','KLNJ','LMD1',
                'MAHB','MEH','MRD','NGCH','QABG','SBZV','SRVN','TBJM']
lat_stations = [36.6 , 31.7 , 35.5 , 37.7 , 36.5 , 34.5 , 31.0 , 27.3 ,
               36.8 , 31.4 , 38.7 , 25.4 ,  35.7 , 36.4 , 27.4 , 35.3 ]
lon_stations = [58.8 , 49.3 , 53.9 , 46.0 , 53.8 , 45.6 , 51.6 , 53.2 ,
               45.7 , 54.6 , 45.7 , 61.1 , 49.6 , 57.6 , 62.4 , 60.3 ]

######## for magnitude
lat_station = []
lon_station = []
target = ['MAHB','QABG','KLNJ']
name_station = target
for name in target:
    lat_station.append(lat_stations[name_stations.index(name)])
    lon_station.append(lon_stations[name_stations.index(name)])
    
inv_irsc = irsc_make_inventory(name_station,lat_station,lon_station)

from obspy.clients.fdsn import Client
from obspy import UTCDateTime
time_event = '2017-11-12 18:18:17.8'
t = UTCDateTime(time_event)
try:
    client = Client('IRIS')
    catalog = client.get_events(starttime = t - 360,
                                    endtime = t + 360,
                                    minmagnitude = 7)
    print '>>> >>> >>>'
except:
    print key,'>>> The current client does not have an event service.'
    
if show:
    #from pylab import rcParams
    #rcParams['figure.figsize'] = 15, 10
    fig = inv_irsc.plot(color = '1' , projection = 'local',show=False)
    fig = inv_iiees.plot(color = '1' , projection = 'local',fig=fig,show=False)
    catalog.plot(method="basemap",projection='local',fig=fig)
if save:
    import os
#    from pylab import rcParams
#    rcParams['figure.figsize'] = 15, 10
    fig = inv_irsc.plot(method="basemap",color = '1' , projection = 'local',show=False)
    fig = inv_iiees.plot(method="basemap",color = '0.5' , projection = 'local',show=False,fig=fig)
    fig = catalog.plot(method="basemap",projection='local',fig=fig,show=False)
#    fig.set_size_inches(15,10)
    path = './output/plot_inv/'
    if not os.path.isdir(path): os.makedirs(path)
    fig.savefig(path+'magnitude_inv_station.png',dpi = 100) #save#
