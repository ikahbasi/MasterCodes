#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:24:47 2019

@author: imon
"""
show = False
save = True
import obspy
import matplotlib.pyplot as plt
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
        code="IR",
        # A list of stations. We'll add one later.
        stations=[],
        description="iman.kahbasi make this inv",
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

name_station = []
lat_station = []
lon_station = []

#from for_iiees_inv_plot import make_iiees_location_station
#stations = make_iiees_location_station()
#for station in stations:
#    name_station.append(station[0])
#    lat_station.append(station[1])
#    lon_station.append(station[2])



name_stations = ['AKL','AMIS','ANJ','AZR','GLO','KGS1','KLNJ','LMD1',
                'MAHB','MEH','MRD','NGCH','QABG','SBZV','SRVN','TBJM']




lat_stations = [36.6 , 31.7 , 35.5 , 37.7 , 36.5 , 34.5 , 31.0 , 27.3 ,
               36.8 , 31.4 , 38.7 , 25.4 ,  35.7 , 36.4 , 27.4 , 35.3 ]



lon_stations = [58.8 , 49.3 , 53.9 , 46.0 , 53.8 , 45.6 , 51.6 , 53.2 ,
               45.7 , 54.6 , 45.7 , 61.1 , 49.6 , 57.6 , 62.4 , 60.3 ]
##### for triger
name_station = name_stations
lat_station = lat_stations
lon_station = lon_stations


inv = iiees_make_inventory(name_station,lat_station,lon_station)

if show:
    inv.plot(color = '1' , projection = 'local')
if save:
    import os
    from pylab import rcParams
    rcParams['figure.figsize'] = 15, 10
    fig = inv.plot(color = '1' , projection = 'local',show=False)
#    fig.set_size_inches(15,10)
    path = './output/plot_inv/'
    if not os.path.isdir(path): os.makedirs(path)
    fig.savefig(path+'irsc_station.png',dpi = 100) #save#
