#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:31:20 2019

@author: imon
"""
import shutil
import os
import glob
from obspy.io.xseed import Parser
################### 1_parser and copy BI resp in folder
BI_resp = glob.glob('./*.dataless')[0]
path = '../BI_resp/'
if not os.path.isdir(path): os.makedirs(path)
sp = Parser(BI_resp)
sp.write_resp(folder=path, zipped=False)
################### 2_copy dlsv resp
path = '../IR_resp/'
if not os.path.isdir(path): os.makedirs(path)
IR_resp = glob.glob('./*.dlsv')[0]
shutil.copy(IR_resp, path)
################### 3_parser and copy dlsv resp
sp = Parser(IR_resp)
sp.write_resp(folder=path, zipped=False)
################### 4_collection waveform with exist resp
path = '../IR_waveform_collecton/'
if not os.path.isdir(path): os.makedirs(path)

list_resp = glob.glob('../IR_RESP/RESP*')
list_trace = glob.glob('./IR_wavout*/*')
target = []
for dir_resp in list_resp:
    n = dir_resp.split('.')
    target.append(n[4])
    
for dir_tr in list_trace:
    l = dir_tr.split('.')[2]
    print l
    if l in target:
        shutil.copy(dir_tr, path)
################### 5_copy BI waveform
path = '../BI_waveform/'
BI_waveform = glob.glob('./*BIN*')[0]
if not os.path.isdir(path): os.makedirs(path)
shutil.copy(BI_waveform, path)
