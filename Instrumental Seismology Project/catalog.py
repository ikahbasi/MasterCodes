# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 10:24:27 2019

@author: Kahbasi
"""
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
def get_catalog():
    time_event = '2017-11-12 18:18:17.8'
    t = UTCDateTime(time_event)
    cat = {}
    
    from obspy.clients.fdsn.header import URL_MAPPINGS
    for key in sorted(URL_MAPPINGS.keys()):
        
        try:
            client = Client(key)
            catalog = client.get_events(starttime = t - 360,
                                    endtime = t + 360,
                                    minmagnitude = 7)
            print('>>> >>> >>> in',key, ':')
    #        cat.plot()
            cat[key]=[catalog[0].origins[0].latitude,catalog[0].origins[0].longitude]
            print(cat[key],'\n')
        except:
            print(key,'>>> The current client does not have an event service.\n')
	#print(cat)
    return cat