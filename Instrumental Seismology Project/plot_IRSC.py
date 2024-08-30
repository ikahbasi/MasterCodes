#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 21:15:33 2019

@author: imon
"""
import glob
from obspy import read
List = glob.glob('./collection/*')
for name in List:
    st = read(name)
    st.plot()