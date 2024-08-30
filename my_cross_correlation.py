"""
Created on Wed Apr  3 21:04:43 2019

@author: imon
"""
from math import sqrt
import matplotlib.pyplot as plt
def cross_correlation(signal1,signal2):
    c = sum([signal1[n]*signal2[n] for n in range(len(signal1))])
    return c

def cc(signal1,signal2):
    num = cross_correlation(signal1,signal2)
    dem = sqrt(cross_correlation(signal1,signal1)*cross_correlation(signal2,signal2))
#    dem = 1
    cc = num/dem
    return cc

def correlation(signal1,signal2):
    if len(signal1)<len(signal2):
        template = signal1
        signal = signal2
    else:
        template = signal2
        signal = signal1
    L = len(template)
    
    for n in range(0,len(signal)-len(template)):
        yield round(cc(template,signal[n:n+L]),4)
#        
#s1 = [1,2,3,4]
#s2 = [5,6,7,8]*10
#
#print(cross_correlation(s1,s2))
#print(cc(s1,s1))
#plt.plot(list(correlation(s1,s2)))
#
#from obspy.signal.cross_correlation import correlate
#
#plt.plot(correlate(s1,s2,len(s1+s2)))
        
from obspy import read
st_1 = read('/home/imon/Desktop/project/1.miniseed')
signal = st_1[0]
signal = signal.detrend()
signal = signal.data.tolist()
tem = signal[400:700]

plt.plot(list(correlation(signal,tem)))
