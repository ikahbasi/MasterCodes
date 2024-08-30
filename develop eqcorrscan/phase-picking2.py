"""
Created on Sun Nov 24 15:13:41 2019

@author: imon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, argrelextrema
import os
#from obspy.core.trace import Trace
import glob

files = sorted(glob.glob('./QualityOfPhasePicking-array/*/*1.npz.npy'))
os.makedirs('./output/', exist_ok=True)
# parameter
shift = 2
ii = 0
EQ_threshold = 0.4
Strict_threshold = 0.6
multi = 2
width = 10

def rms(x):
    rms = np.sqrt(np.mean(np.square(x)))
    return rms

def index(n):
    return (n-(100*shift))/(100*shift)


for path in files:
    output_name = os.path.basename(path).split('.')[0]
    print(output_name)
    arrs = np.load(path)
    for name, arr in enumerate(arrs):
        # array
        plt.plot(arr)
        # find peaks and plot them
        rms_threshold = rms(arr) * multi
        peaks_index, peaks_val = find_peaks(arr, height=rms_threshold)
        peaks_val = peaks_val['peak_heights']
        plt.plot(peaks_index, arr[peaks_index], 'xg')
        # plot eqcorrscan treshold
        plt.hlines([EQ_threshold, EQ_threshold*(-1)], 0, len(arr), 'r')
        # find my pick
        
#        maximums_index = argrelextrema(arr, np.greater)[0]
#        minimums_index = argrelextrema(arr, np.less)[0]
#        maximums = arr[maximums_index]
#        minimums = arr[minimums_index]
#        max_peaks = muximums[muximums > threshold]
        try:
            Max = np.max(peaks_val)
            if (Max < Strict_threshold) and (len(find_peaks(arr, height=Max-(Max/4))[0])==1):
                plt.plot(peaks_index[np.where(peaks_val==Max)], Max, 'or')
                plt.hlines([Max-(Max/4)], 0, len(arr), 'g')
            elif (Max < Strict_threshold) and (len(find_peaks(arr, height=Max-(Max/4))[0])>1):
                #plt.plot(peaks_index, peaks_val, 'or')
                plt.hlines([Max-(Max/4)], 0, len(arr), 'g')
            elif Max > Strict_threshold:
                plt.plot(peaks_index[np.where(peaks_val==Max)], Max, 'or')
        except Exception as error:
            print(error)
            plt.xlabel('error')
        
        plt.savefig('./output/{}-{}.png'.format(output_name, name))
#        plt.show()
        plt.close()
        print(name)
        break
    break
