"""
Created on Fri Jul 31 10:32:57 2020

@author: imon
"""

from obspy import read
import scipy.fftpack
import numpy as np
import matplotlib.pyplot as plt

def fft_plot(tr):
    tr.filter('highpass', freq=0.2)
    sps = tr.stats.sampling_rate
    T = 1/sps
    N = tr.data.size
    segment = scipy.fftpack.helper.next_fast_len(tr.data.size)
    yf = scipy.fftpack.fft(tr.data, segment)
    yf = np.abs(yf[:N//2])
    xf = np.fft.fftfreq(segment, d=T)[:N//2]
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.plot(xf, yf)
    plt.xlabel('frequency', fontweight='black')
    plt.ylabel('amplitude', fontweight='black')

###################### 200sps --> 180sps

#st = read('./white-noise/white-noise.msd')
#tr0 = st[0]
#tr0.detrend('constant')
#tr0.taper(0.01)
#
#
## method 1
#print('decimate to 100sps. interpolate to 180sps.')
#tr = tr0.copy()
#tr.decimate(2, no_filter=False)
#tr.interpolate(180)
#fft_plot(tr)
#
## method 2
#print('interpolate to 360sps. decimate to 180sps.')
#tr = tr0.copy()
#tr.interpolate(360)
#tr.decimate(2, no_filter=False)
#fft_plot(tr)


###################### 200sps --> 50sps
## part 1
#st = read('./white-noise/white-noise.msd')
#tr0 = st[0]
#
#print('decimate with pre-filter')
#tr = tr0.copy()
#tr.decimate(4, no_filter=False)
#fft_plot(tr)
#
## part 2
#print('decimate without pre-filter')
#tr = tr0.copy()
#tr.decimate(4, no_filter=True)
#fft_plot(tr)
#
## part 3
#print('tr.stats.sampling_rate=50')
#tr = tr0.copy()
#tr.stats.sampling_rate = 50
#fft_plot(tr)
#print(tr)
#
## part 4
#print('filter data and decimate without pre-filter')
#tr = tr0.copy()
#tr.filter('lowpass', freq=25)
#tr.decimate(4, no_filter=True)
#fft_plot(tr)

################  correlation detector
'''
from math import sin
domain = np.linspace(0,4,10000)*2*3.14
sinusoid = np.array(list(map(sin, domain)))

st = read('white-noise.msd')
tr0 = st[0]
tr0.detrend('constant')
tr = tr0
data = tr.data

n = 400000
data[n: n+len(sinusoid)] += sinusoid * 1.5
tr.data = data

n = 300000
data[n: n+len(sinusoid)] += sinusoid * 0.75
tr.data = data

n = 200000
data[n: n+len(sinusoid)] += sinusoid * 2
tr.data = data

n = 100000
data[n: n+len(sinusoid)] += sinusoid
tr.data = data

tr.write('correlation.msd', format='MSEED')
'''

#temp = read('./sinusoid-pulse/template.msd')
#temp.detrend('constant')
#
#st = read('./sinusoid-pulse/signal_and_noise.msd')
#st.detrend('constant')
#
## method 1
#from obspy.signal.cross_correlation import correlate
#shift = (len(st[0].data)+len(temp[0].data)) // 2
#cc = correlate(st[0].data, temp[0].data, shift)
#tr_cc = st[0].copy()
#tr_cc.data = cc[len(temp[0].data)-1:]
#tr_cc.plot(method='full')
#
## method 2
#from obspy.signal.cross_correlation import correlation_detector
#height = 0.3  # similarity threshold
#distance = 10  # distance between detections in seconds
#detections, sims = correlation_detector(st, temp, height, distance,
#                                        template_names=[1], plot=st)


############### time
#from obspy.signal.cross_correlation import xcorr_max
#from obspy.signal.cross_correlation import correlate
## part 1
#st41 = read('./time/event1-code1.msd')
#st42 = read('./time/event1-code2.msd')
#cc = correlate(st41[0].data, st42[0].data, 100000)
#shift, value = xcorr_max(cc)
#print('samples:', shift, 'time:', shift/st41[0].stats.sampling_rate)
#
## part 2
#st51 = read('./time/event2-code1.msd')
#st52 = read('./time/event2-code2.msd')
#tr51 = st51[0]
#tr52 = st52[0]
#tr51.trim(tr52.stats.starttime, tr51.stats.endtime)
#cc = correlate(st51[0].data, st52[0].data, 100000)
#shift, value = xcorr_max(cc)
#print('samples:', shift, 'time:', shift/st51[0].stats.sampling_rate)


################### filter
#from obspy import Trace
#filt = np.genfromtxt('FIR')
#noise = np.random.normal(0, 10, 10000)
#
#tr200 = Trace(noise)
#tr200.stats.sampling_rate = 200
#fft_plot(tr200)
##
#tr200.data = np.convolve(tr200.data, filt)
#fft_plot(tr200)
#
#tr150 = Trace(noise)
#tr150.stats.sampling_rate = 150
#fft_plot(tr150)
##
#tr150.data = np.convolve(tr150.data, filt)
#fft_plot(tr150)
#
#tr50 = Trace(noise)
#tr50.stats.sampling_rate = 50
#fft_plot(tr50)
##
#tr50.data = np.convolve(tr50.data, filt)
#fft_plot(tr50)