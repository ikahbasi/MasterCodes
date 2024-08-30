"""
Created on Sun Sep 29 18:28:05 2019

@author: imon
"""

from obspy.signal.cross_correlation import *
import numpy as np
import matplotlib.pyplot as plt
from math import sin
from math import sqrt
#define signal
'''
signal1 = [0, 10, 5, 10, 0]
signal2 = [10, 0, 5, 0, 10]
'''
theta = np.linspace(0, 2*np.pi, 61)
signal1 = np.sin(theta) * 2
signal2 = np.sin(theta) * 0.5

shift = (len(signal1)+len(signal2))//2
cc = correlate(signal1, signal2, shift, normalize=True)# , demean=False, method='direct')
cc_not = correlate(signal1, signal2, shift, normalize=False)
cc1= correlate(signal1, signal1, shift, normalize=False)
cc2 = correlate(signal2, signal2, shift, normalize=False)

#cc = correlate_template(signal1, signal2, demean=False, method='direct')
#cc = xcorr(signal1, signal2, len(signal1)//2)
#cc = correlate(a, b, len(a)+len(b)-1)
'''
print('normalize cc: ', max(cc))
print('cc_not: ', max(cc_not))
print('cc1: ', max(cc1))
print('cc2: ', max(cc2))
print('sqrt cc1*cc2: ', sqrt(max(cc1)*max(cc2)))
print('my cc: ', max(cc_not)/sqrt(max(cc1)*max(cc2)))
'''
fig = plt.figure(figsize=(10, 8))
labelsize=15
ax1 = plt.subplot(311)
ax1.xaxis.set_tick_params(labelsize=labelsize)
ax1.yaxis.set_tick_params(labelsize=labelsize)
ax1.plot(signal1, linewidth=2)
ax1.set_xlabel('Time', fontsize=10)
ax1.set_ylabel('Amplitude', fontsize=10)
ax1.set_title('Signal 1', fontsize=15, weight='bold')
ax1.set_ylim([-2.2, 2.2])
plt.grid()

ax2 = plt.subplot(312)
ax2.xaxis.set_tick_params(labelsize=labelsize)
ax2.yaxis.set_tick_params(labelsize=labelsize)
ax2.plot(signal2, linewidth=2)
ax2.set_xlabel('Time', fontsize=10)
ax2.set_ylabel('Amplitude', fontsize=10)
ax2.set_title('Signal 2', fontsize=15, weight='bold')
ax2.set_ylim([-2.2, 2.2])
plt.grid()

ax3 = plt.subplot(313)
ax3.xaxis.set_tick_params(labelsize=labelsize)
ax3.yaxis.set_tick_params(labelsize=labelsize)
x = np.arange(-(len(cc)-1)/2,(len(cc)-1)/2+1)
ax3.plot(x, cc, 'g', linewidth=2)
ax3.set_ylabel('Correlation Coefficient', fontsize=10)
ax3.set_xlabel('Shift', fontsize=10)
ax3.set_title('Cross-Correlation', fontsize=15, weight='bold')
ax3.set_ylim([-1.2, 1.2])
plt.grid()
plt.tight_layout()
for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(2)
    ax2.spines[axis].set_linewidth(2)
    ax3.spines[axis].set_linewidth(2)


plt.savefig('./test1.png',dpi=120)
#plt.show()
