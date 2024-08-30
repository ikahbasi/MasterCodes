#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 18:49:15 2019

@author: imon
"""
lat_event = 34.877
lon_event = 45.841
save = False
show = True

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os



def plot_cat(catalog):
    fig, ax = plt.subplots(figsize=(7,7))
    #for size of map
    rad = 0.7E5
    #make basemap
    m = Basemap(projection='lcc', resolution=None,
                width= rad, height=rad, 
                lat_0=lat_event, lon_0=lon_event)
    '''
#    n=0.4
#    rad = n
#    m = Basemap(projection='merc', resolution=None,
#                llcrnrlat=lat_event-n,
#                llcrnrlon=lon_event-n,
#                urcrnrlat=lat_event+n,
#                urcrnrlon=lon_event+n)
#    rad = m(rad,rad)
    
#    m.bluemarble()
#    m.drawmapboundary(color='k', linewidth=1.0, fill_color=None, zorder=None, ax=None)
#    m.etopo(scale=2)
    '''
    #make background
    m.drawlsmask(land_color='0.9', ocean_color='b')

    #draw parallels between latitude
    parallels = np.arange(lat_event-1,lat_event+1,.2)
    m.drawparallels(parallels,labels=[True,False,True,False])
    #draw meridians between longitude
    meridians = np.arange(lon_event-1,lon_event+1,0.2)
    m.drawmeridians(meridians,labels=[True,False,True,False])
    #make array of number for circular label
    an = np.linspace(0, 2 * np.pi, len(catalog)+3)
    count = 0
    for name in catalog.keys():
        #make point of lat&lon epicenter
        x, y = m(catalog[name][1], catalog[name][0])
        plt.plot(x, y, 'x',color='red' ,markersize=7)
        
        #make position of label
        xtext = rad/2.5 * np.cos(an[count]) + rad/2
        ytext = rad/2.5 * np.sin(an[count]) + rad/2
        
        #lat & lon for write in label
        xt = str(round(catalog[name][1],2))
        yt = str(round(catalog[name][0],2))
        ax.annotate(name+'\n'+xt+'_'+yt,
                    xy=(x, y), xycoords="data",
                    va="center", ha="center",xytext=(xtext, ytext),
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        count +=1
    #save output file
    if show:
        fig.show()
    if save:
        path = './output/'
        if not os.path.isdir(path): os.makedirs(path)
        fig.savefig(path+'catalog_map'+'.png', dpi=100) #save#
        
from catalog import get_catalog
cat = get_catalog()
plot_cat(cat)
'''
https://matplotlib.org/gallery/userdemo/annotate_simple_coord03.html#sphx-glr-gallery-userdemo-annotate-simple-coord03-py
'''
'''
def plot_cat(catalog):
    fig, ax = plt.subplots(figsize=(10, 8))
    m = Basemap(projection='lcc', resolution=None,
                width=0.5E5, height=0.5E5, 
                lat_0=34.877, lon_0=45.841)
    m.bluemarble()
    
    count = 0
    for name in catalog.keys():
        xt = str(catalog[name][1])
        yt = str(catalog[name][0])
        x, y = m(catalog[name][1], catalog[name][0])
        plt.plot(x, y, 'x',color='red' ,markersize=10)
        if count ==0:
            an1 = ax.annotate(name+'_'+xt+'_'+yt,
                              xy=(x, y), xycoords="data",
                              va="center", ha="center",xytext=(9000, 10000),
                              bbox=dict(boxstyle="round", fc="w"),
                              arrowprops=dict(arrowstyle="->"))
            count +=1
        else:
            offset_from = OffsetFrom(an1, (0.3, 0.7))
            an1 = ax.annotate(name+'_'+xt+'_'+yt,
                              xy=(x, y), xycoords="data",
                              xytext=(-20, 0), textcoords=offset_from,
                              # xytext is offset points from "xy=(0.5, 0), xycoords=an1"
                              va="top", ha="center",
                              bbox=dict(boxstyle="round", fc="w"),
                              arrowprops=dict(arrowstyle="->"))
plot_cat(cat)
'''