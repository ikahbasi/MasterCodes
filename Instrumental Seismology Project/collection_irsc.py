#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 19:39:20 2019

@author: imon
"""
from shutil import copy
import glob
import os
path = './collection/'
if not os.path.isdir(path): os.makedirs(path)

list_resp = glob.glob('./IR_RESP/*')
list_trace = glob.glob('./IR_wavout(2698)/*')
target = []
for dir_resp in list_resp:
    n = dir_resp.split('.')
    target.append(n[3])
    
for dir_tr in list_trace:
    l = dir_tr.split('.')[2]
    print l
    if l in target:
        copy(dir_tr, path)