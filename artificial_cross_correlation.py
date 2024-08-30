"""
Created on Thu Mar 21 22:11:16 2019

@author: imon
"""
from obspy.signal.cross_correlation import correlate
import numpy as np
import matplotlib.pyplot as plt
from math import sin
#define signal
noise = np.random.normal(0,1,10000)
noise=noise/(2*max(noise)) # normal max to 1
template = noise[700:800]  # shift a by 20 samples
#domain
domain = np.linspace(0,4,10000)*2*3.14
# sinusodal signal
signal1 = list(map(sin,domain))
# cross correlation coefficient

cc = correlate(noise+signal1, template, (len(noise)+len(template))//2)
#plot 
"""
fig = plt.figure(figsize=(10,10))
plt.subplots_adjust(hspace=0.6)
fig.add_subplot(511).plot(signal1)
plt.title('signal1')

fig.add_subplot(512).plot(noise)
plt.title('noise')

fig.add_subplot(513).plot(noise+signal1)
plt.title('noise+signal1')

fig.add_subplot(514).plot(template)
plt.title('template')

fig.add_subplot(515).plot(cc)
plt.title('cc')
#plt.show()
#############################################################
template_1_1 = signal1[400:1000]
cc = correlate(noise+signal1, template_1_1, (len(noise)+len(template_1_1))//2)
#plot 
fig = plt.figure(figsize=(10,10))
plt.subplots_adjust(hspace=0.6)
fig.add_subplot(511).plot(signal1)
plt.title('signal1')

fig.add_subplot(512).plot(noise)
plt.title('noise')

fig.add_subplot(513).plot(noise+signal1)
plt.title('noise+signal1')

fig.add_subplot(514).plot(template_1_1)
plt.title('template')

fig.add_subplot(515).plot(cc)
plt.title('cc')
#plt.show()
plt.close('all')
"""

#############################################################
domain2 = np.linspace(0,1,200)*2*3.14
template2 = list(map(sin,domain2))
# reduce template amplitude for burailing in to noise
my_new_list = [i * 0.1 for i in template2]
#my_new_list = [i for i in template2]

signal2 = (list(np.zeros(5000)) + my_new_list + list(np.zeros(4800)))#*0.1
cc2 = correlate(noise+signal2, template2, (len(noise)+len(template2))//2)
#cc2 = correlate(signal2[4500:5500], template2, (len(noise)+len(template2[4500:5500]))//2)

#cc = correlate(a, b, len(a)+len(b)-1)
fig = plt.figure(figsize=(12,8))
fig.subplots_adjust(hspace=2)
ax1 = plt.subplot2grid((3, 10), (0, 1), colspan=9)
ax2 = plt.subplot2grid((3, 10), (1, 0))
ax3 = plt.subplot2grid((3, 10), (1, 1), colspan=9)#, rowspan=1)
ax4 = plt.subplot2grid((3, 10), (2, 1), colspan=9)#, rowspan=2)


#ax1 = plt.subplot(322)
ax1.plot(signal2)
ax1.set_title('signal')
ax1.set_xlabel('time')
ax1.set_ylabel('amplitude')



#ax2 = plt.subplot(321)
ax2.plot(template2)
ax2.set_title('template')
ax2.set_xlabel('time')
ax2.set_ylabel('amplitude')


#ax3 = plt.subplot(312)
ax3.plot(noise+signal2)
ax3.set_title('noise+signal')
ax3.set_xlabel('time')
ax3.set_ylabel('amplitude')



#ax4 = plt.subplot(313)
#x = np.arange(-len(cc2)/2,len(cc2)/2)
ax4.plot(cc2)
ax4.set_title('cross correlation')
ax4.set_xlabel('shift')
ax4.set_ylabel('correlation value')


plt.tight_layout()
#plt.savefig('./test.png',dpi=120)
plt.show()
'''
plt.close('all')
fig = plt.figure(figsize=(8,5))
plt.subplots_adjust(hspace=0.6)
fig.add_subplot(311).plot(signal2[4500:5500])
plt.title('signal')
fig.add_subplot(412).plot(noise+signal2)
plt.title('noise+signal2')
fig.add_subplot(211).plot(signal2[4500:5500])
fig.add_subplot(211).plot(template2,'r')
plt.title('template2')
fig.add_subplot(212).plot(cc2)
plt.title('cc')
plt.show()
'''
