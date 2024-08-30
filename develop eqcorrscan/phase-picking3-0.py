"""
Created on Sun Nov 24 15:13:41 2019

@author: imon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks#, argrelextrema
import os
import glob
from obspy.core.trace import Trace
shift = 1
output_path = './output-{}shift'.format(shift)
files = sorted(glob.glob('./QualityOfPhasePicking-array/*/*{}.npz.npy'.format(shift)))
os.makedirs(output_path, exist_ok=True)
# parameter
EQ_threshold = 0.4
Strict_threshold = 0.6
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
    for ii, arr in enumerate(arrs):
#        ii = 6
#        arr = arrs[ii]
        print(ii)
        tr = Trace(arr)
        tr.taper(0.005)
        arr = tr.data
        # array
        plt.plot(arr)
        rms = RMS(arr)
        # find max peaks and plot them
        Max = arr.max()
        Max_index = np.where(arr == Max)[0][0]
        '''
        max_peaks_index, max_peaks_val = find_peaks(arr, height=rms_threshold)
        max_peaks_val = max_peaks_val['peak_heights']
        if len(max_peaks_val)>=1:
            Max = max_peaks_val.max()
            Max_index = max_peaks_index[np.where(max_peaks_val==Max)]
        else:
            Max = None
            Max_index = None
        '''
        # find min peaks and plot them
        Min = arr.min()
        Min_index = np.where(arr == Min)[0][0]
        '''
        min_peaks_index, min_peaks_val = find_peaks(arr*(-1), height=rms_threshold)
        min_peaks_val = min_peaks_val['peak_heights'] * (-1)
        if len(min_peaks_val)>=1:
            Min = min_peaks_val.min()
            Min_index = min_peaks_index[np.where(min_peaks_val==Min)]
        else:
            Min = None
            Min_index = None
        '''
        # plot 2*rms zone and related maximumes and minimumes
        plt.plot([Max_index, Min_index], [Max, Min],
                 'xg', label='all max & min excited 2*rms')
        plt.axhspan(-2*rms, 2*rms, facecolor='#2ca02c', alpha=0.5, label='2*rms zone')
        # plot eqcorrscan treshold
        plt.hlines(EQ_threshold, 0, len(arr), 'r', label='EQ threshold')
        if Max >= EQ_threshold:
            plt.plot(Max_index, Max, 'or', label='EQ phase picking')
        # plot strict threshold
        plt.hlines(
            [Strict_threshold, -Strict_threshold], 0, len(arr),
            'b', linestyles='dashdot', label='Strict threshold')
        # find my maximume peaks
        if Max > Strict_threshold:
            detection_max = [Max_index, Max]
        else:
            plt.hlines(Max-rms, 0, len(arr), 'g', label='is it a unique pick?')
            num_of_peaks = len(find_peaks(arr, height=Max-rms)[0])
            if  num_of_peaks == 1:
                detection_max = [Max_index, Max]
            elif num_of_peaks > 1:
                detection_max = [None, None]
        # find my minimume peaks
        if Min < -Strict_threshold:
            detection_min = [Min_index, Min]
        else:
            plt.hlines(Min+rms, 0, len(arr), 'g', label='is it a unique pick?')
            num_of_peaks = len(find_peaks(-arr, height=-(Min+rms))[0])
            if num_of_peaks==1:
                detection_min = [Min_index, Min]
            else:
                detection_min = [None, None]
        # Select pick between max and min of selected picks
        if (None not in detection_min) and (None in detection_max):
            phase = detection_min
        elif (None in detection_min) and (None not in detection_max):
            phase = detection_max
        elif (None in detection_max) and (None in detection_min):
            phase = [None, None]
        elif (None not in detection_max) and (None not in detection_min):
            if abs(detection_min[1]) > abs(detection_max[1]):
                phase = detection_min
            else:
                phase = detection_max
        else:
            print('some unknown situation happened')
        plt.scatter(phase[0], phase[1], linewidth=20, label='my phase picking')
        text = 'rms is: %.2f\nmax is: %.2f\nmin is: %.2f' % (rms, Max, Min)
        plt.text(len(arr)+10, 0, text, ha='left', style='italic')
        
        plt.tight_layout()
        plt.legend(loc='lower left', bbox_to_anchor= (0.0, 1.05), ncol=2,
                   borderaxespad=0, frameon=True)
        plt.savefig('{}/{}-{}.png'.format(output_path, output_name, ii))
#        plt.show()
        plt.close()
        
#        break
#    break
