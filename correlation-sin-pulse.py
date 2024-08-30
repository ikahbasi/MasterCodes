from obspy.signal.cross_correlation import correlate
import numpy as np
import matplotlib.pyplot as plt
from math import sin
#define signal
noise = np.random.normal(0, 1, 10000)
noise = noise/(max(noise)/1.5) # normal max to 1


time = np.linspace(0, 1, 200) * 2 * 3.14
template = np.array(list(map(sin, time)))

signal = np.concatenate((np.zeros(5000), template * 0.2, np.zeros(4800)))#*0.1
cc2 = correlate(noise+signal, template, (len(noise)+len(template))//2)
#cc2 = correlate(signal2[4500:5500], template2, (len(noise)+len(template2[4500:5500]))//2)

#cc = correlate(a, b, len(a)+len(b)-1)
fig = plt.figure(figsize=(12,8))
fig.subplots_adjust(hspace=2)
ax1 = plt.subplot2grid((3, 10), (0, 1), colspan=8)   # sin pulse
ax2 = plt.subplot2grid((3, 10), (1, 0), colspan=1)   # template
ax3 = plt.subplot2grid((3, 10), (1, 1), colspan=8)   # signal and noise
ax4 = plt.subplot2grid((3, 10), (2, 1), colspan=8)   # cross correlation


#ax1 = plt.subplot(322)
t = np.arange(len(np.zeros(5000)))
ax1.plot(t, np.zeros(5000), 'C0')
t = np.arange(len(template)) + (t[-1]+1)
ax1.plot(t, template * 0.2, 'r')
t = np.arange(len(np.zeros(4800))) + (t[-1]+1)
ax1.plot(t, np.zeros(4800), 'C0')
#ax1.plot(signal)
ax1.set_title('Sinusoidal pulse', fontsize=15, loc='right')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude [count]')



#ax2 = plt.subplot(321)
ax2.plot(template, 'r')
ax2.set_title('Template', fontsize=15)
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Amplitude [count]')


#ax3 = plt.subplot(312)
ax3.plot(noise+signal)
ax3.set_title('Noise and buried sinusoidal pulse', fontsize=15, loc='right')
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Amplitude [count]')



#ax4 = plt.subplot(313)
#x = np.arange(-len(cc2)/2,len(cc2)/2)
ax4.plot(cc2, 'g')
ax4.set_title('cross correlation', fontsize=15, loc='right')
ax4.set_xlabel('Shift [count]')
ax4.set_ylabel('Correlation coefficient')

for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(2)
    ax2.spines[axis].set_linewidth(2)
    ax3.spines[axis].set_linewidth(2)
    ax4.spines[axis].set_linewidth(2)
plt.tight_layout()
#plt.savefig('./test.png',dpi=120)
plt.show()
