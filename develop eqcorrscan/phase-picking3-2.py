"""
Created on Sun Nov 24 15:13:41 2019

@author: imon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks#, argrelextrema
import os
import glob
shift = 1
output_path = './img'

files = sorted(glob.glob('*.npy'))
os.makedirs(output_path, exist_ok=True)
# parameter
min_cc = 0.6
flow_cc = 0.6666
multi = 2
width = 10

def RMS(array):
    rms = np.sqrt(np.mean(np.square(array)))
    return rms

for path in files:
#    path = './QualityOfPhasePicking-array/20140915t21041830_20140924_220100350000/20140915t21041830_20140924_220100350000-1.npz.npy'
    output_name = os.path.basename(path).split('.')[0]
    print(output_name)
    arrs = np.load(path)
#    fig, axs = plt.subplots(ncols=2, nrows=len(arrs)//2+1, figsize=(6, len(arrs)))
    plt.figure(figsize=(8, 8))
    for ii, arr in enumerate(arrs):
        
        ax = plt.subplot(len(arrs)//3+1, 3, ii+1)
        cc_max = arr.max()
        rms = RMS(arr)
        rms_thr = rms * 2
        ax.plot(arr)
        ax.hlines(rms_thr, 0, len(arr), 'c', ls=':')
        ax.hlines(min_cc, 0, len(arr), 'r', ls=':')
        ax.hlines(flow_cc*cc_max, 0, len(arr), 'g')
        if cc_max > min_cc:
            _skip_phase = False
            ax.plot(arr.argmax(), cc_max, 'or')
        elif cc_max < min_cc and 1 >= 0.5:
            num_of_peaks = len(
                find_peaks(arr, height=flow_cc*cc_max)[0])
            if  num_of_peaks == 1 and cc_max > 0.2:
                _skip_phase = False
                ax.plot(arr.argmax(), cc_max, 'og')
            else:
                _skip_phase = True
        else:
            _skip_phase = True
        
        if _skip_phase:
            continue
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
    plt.savefig(os.path.join(output_path, path+'.png'))
    plt.close('all')
#    plt.show()
