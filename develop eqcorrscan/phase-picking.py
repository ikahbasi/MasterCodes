"""
Created on Sun Nov 24 15:13:41 2019

@author: imon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import os
from obspy.core.trace import Trace
os.makedirs('./output', exist_ok=True)
path = './QualityOfPhasePicking-array/20140915t21041830_20140924_220100350000/20140915t21041830_20140924_220100350000-2.npz.npy'
arrs = np.load(path)
shift = 2
ii = 0
threshold = 0.4
multi = 2

def rms(x):
    rms = np.sqrt(np.mean(np.square(x)))
    return rms


def index(n):
    return (n-(100*shift))/(100*shift)

for name, arr in enumerate(arrs):
    tr = Trace(arr)
    tr.taper(0.02)
    arr = tr.data
    peaks_index, peaks_val = find_peaks(arr, height=rms(arr)*multi)
    peaks_val = peaks_val['peak_heights']
    
    width = 10
    iteration = 0
    for x,y in zip(peaks_index, peaks_val):
        l_threshold, r_threshold = None, None
        if x - width > 0:
            left = arr[0: x-width]
            l_rms = rms(left)
            l_threshold = l_rms * multi
            print('left threshold is', l_threshold)
        if x + width < len(arr):
            right = arr[x+width: len(arr)]
            r_rms = rms(right)
            r_threshold = r_rms * multi
            print('right threshold is', r_threshold)
        
        plt.axvspan(x-width, x+width, facecolor='#2ca02c', alpha=0.5)
        if r_threshold and l_threshold is not None:
            if (y > r_threshold) and (y > l_threshold):
                plt.plot(x, y, 'or')
#        noise = np.concatenate((left, right))
#        rms_noise = rms(noise)
#        snr_threshold = 2 * rms_noise
#        print('rms noise is: ', snr_threshold)
#        if y > snr_threshold:
#            plt.plot(x, y, 'oy')
        print('amplitude of peak is: ', y)
        plt.plot(arr)
        plt.xlim(0, len(arr))
        plt.hlines([threshold, -1*threshold], 0, len(arr), 'r')
        plt.plot(peaks_index, arr[peaks_index], 'xg')
        
        plt.savefig('./output/{}-{}.png'.format(name, iteration))
#        plt.show()
        plt.close()
        iteration += 1
#        break
#    break