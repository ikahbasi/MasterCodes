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
        description="iman.kahbasi make this inv.",
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
##### for triger remove some station that we dont have trace
rm = [u'GTMR', u'RMKL', u'SHGR', u'SRSL', u'BJRD', u'BSRN', u'GRMI',u'NASN', u'TABS', u'ZNJK']
for ii in rm:
    ind = name_stations.index(ii)
    name_stations.pop(ind)
    lat_stations.pop(ind)
    lon_stations.pop(ind)
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
    
#    fig.set_size_inches(15,10, forward=True)
    path = './output/plot_inv/'
    if not os.path.isdir(path): os.makedirs(path)
    fig.savefig(path+'iiees_station.png',dpi = 100) #save#
