#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 18:29:09 2019

@author: imon
"""
'''
ILBA
SHGR
SNGE
MAKU
RMKL
ASAO
KHMZ
traget = ['ILBA','SHGR','SNGE','MAKU','RMKL','ASAO','KHMZ']
'''
from obspy.io.xseed import Parser
from obspy.imaging.maps import plot_map
import matplotlib.pyplot as plt
def make_iiees_location_station():
	p = Parser('./BI_2019-01-07.dataless')
	blk = p.blockettes

	List = []
	lat = []
	lon = []
	stations = []

	for ii in blk[50]:
		if ii.station_call_letters in List:
		    continue
		List.append(ii.station_call_letters)
		lat.append(ii.latitude)
		lon.append(ii.longitude)
		stations.append([ii.station_call_letters,ii.latitude,ii.longitude])
	return stations
