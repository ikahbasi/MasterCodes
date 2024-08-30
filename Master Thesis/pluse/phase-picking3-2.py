"""
Created on Sun Nov 24 15:13:41 2019

@author: imon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks#, argrelextrema
import os
import glob
from scipy.stats import median_abs_deviation as MAD

shift = 1
min_cc = 0.6
float_cc = 0.6666
multi = 2
width = 10

def RMS(array):
    rms = np.sqrt(np.mean(np.square(array)))
    return rms

def phase_picking(path):
    files = sorted(glob.glob(os.path.join(path, 'lag-plot', '*.npy')))
    output_path = os.path.join(path, 'lag-plot', 'img')
    os.makedirs(output_path, exist_ok=True)
    for path_file in files:
        output_name = os.path.basename(path_file).split('.')[0]
        print(output_name)
        arrs = np.load(path_file)
    #    fig, axs = plt.subplots(ncols=2, nrows=len(arrs)//2+1, figsize=(6, len(arrs)))
        plt.figure(figsize=(8, 8))
        for ii, arr in enumerate(arrs):
            ax = plt.subplot(len(arrs)//3+1, 3, ii+1)
            cc_max = arr.max()
            #rms = RMS(arr)
            #rms_thr = rms * 2
            ax.plot(arr)
            # mad
            mad = MAD(arr, axis=None) * 2
            ax.hlines(mad, 0, len(arr), 'violet', ls='-.')
            # 0.5
            ax.hlines(0.5, 0, len(arr), 'k', alpha=0.5)
            # strict treshold
            ax.hlines(min_cc, 0, len(arr), 'r', ls=':')
            # Floating
            ax.hlines(float_cc*cc_max, 0, len(arr), 'g')
            ax.set_ylim(top=1.1)
            ax.set_yticks([0, 0.5, 1])
            if cc_max > min_cc:
                _skip_phase = False
                ax.plot(arr.argmax(), cc_max, 'or')
            elif cc_max < min_cc and 1 >= 0.5:
                num_of_peaks = len(
                    find_peaks(arr, height=float_cc*cc_max)[0])
                if  num_of_peaks == 1 and cc_max > 0.3:
                    _skip_phase = False
                    ax.plot(arr.argmax(), cc_max, 'og')
                else:
                    _skip_phase = True
            else:
                _skip_phase = True
            
            if _skip_phase:
                continue
            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
        plt.savefig(os.path.join(output_path, f'{output_name}.png'))
        plt.close('all')
#    plt.show()

inp_path = 'main_19mordad'
runs_path = glob.glob(os.path.join('..', '..', inp_path, 'run*'))
runs_path = sorted(runs_path)
for path in runs_path:
    print(path)
    phase_picking(path)
