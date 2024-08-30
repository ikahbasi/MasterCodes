import glob
import os

from eqcorrscan.core.match_filter import read_detections
from obspy import read, UTCDateTime 

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np

fminb=3
fmaxb=6

if not os.path.isdir("spectrograms/") == True:
    os.system("mkdir spectrograms")

#detection_files =os.listdir('./detections/6s/')
detection_path = './detections/6s/'
detection_files = glob.glob(os.path.join(detection_path, '*'))

for detection_file in sorted(detection_files):
  detections = read_detections(detection_file)
  print("Starting for: ", detection_file)

  for i, detection in enumerate(detections):
    if float(detection.threshold) != 0 and (abs(float(detection.detect_val))/float(detection.threshold) > (1.05)):
        print("Ploting ", i+1, "of ", len(detections)) 

        doy = detection.detect_time.strftime('%j')       

        stations = []
        for chan in detection.chans:
            sta_tup = chan[0]
            stations.append(str(sta_tup))
        stations = list(set(stations))

        npanels=len(stations)

        fig = plt.figure(figsize=(12,20))
        for i,sta in enumerate(stations):

            # you have to start with common reference times
            st = read("finished/"+doy+"/"+sta.upper()+".HHE.*")

            for tr in st:
                if tr.stats.station == "VINO":
                    if tr.stats.sampling_rate != 100.0:
                        tr.stats.sampling_rate = 100.0
                else:
                    if tr.stats.sampling_rate != 200.0:
                        tr.stats.sampling_rate = 200.0

            st.merge(method=1, fill_value=0)
            
            if st[0].stats.station == "JAVS":
                ax1 = plt.subplot(411)

                tstart = UTCDateTime(detection.detect_time - 5.0)
                #ts = date2num(UTCDateTime(detection.detect_time)) - 7.5
                tend = UTCDateTime(detection.detect_time + 20.0)
                #te = date2num(UTCDateTime(detection.detect_time)) + 20.0
        
                st1 = st.copy()
                st1 = st1.slice(starttime=tstart, endtime=tend)

                sp1spectrr = st1.copy()
                sp1spectr = sp1spectrr[0]
            
                sp1spectr.spectrogram(log=False, show=False, axes=ax1, wlen=0.5, cmap ='jet', dbscale=True)
                ax1.set_ylim(0, 70)

                st1det = st1.detrend(type='constant')
                st1det = st1det.taper(max_percentage=0.05, type="hann")

                st1filta = st1det.filter('bandpass', freqmin=fminb, freqmax=fmaxb, zerophase=True)
                
                ax1a=ax1.twinx()
                ax1a.plot(st1filta[0].times(), st1filta[0], 'k')
                ax1a.axvline((detection.detect_time - st1[0].stats.starttime), color='k', linestyle='--')    

            if st[0].stats.station == "CEY":
                ax2 = plt.subplot(412)
                
                tstart = UTCDateTime(detection.detect_time - 5.0)
                #ts = date2num(UTCDateTime(detection.detect_time)) - 7.5
                tend = UTCDateTime(detection.detect_time + 20.0)
                #te = date2num(UTCDateTime(detection.detect_time)) + 20.0
        
                st1 = st.copy()
                st1 = st1.slice(starttime=tstart, endtime=tend)

                sp1spectrr = st1.copy()
                sp1spectr = sp1spectrr[0]
            
                sp1spectr.spectrogram(log=False, show=False, axes=ax2, wlen=0.5, cmap ='jet', dbscale=True)
                ax2.set_ylim(0, 70)

                st1det = st1.detrend(type='constant')
                st1det = st1det.taper(max_percentage=0.05, type="hann")

                st1filta = st1det.filter('bandpass', freqmin=fminb, freqmax=fmaxb, zerophase=True)
                
                ax2a=ax2.twinx()
                ax2a.plot(st1filta[0].times(), st1filta[0], 'k')
                ax2a.axvline((detection.detect_time - st1[0].stats.starttime), color='k', linestyle='--')  

            if st[0].stats.station == "KNDS":
                ax3 = plt.subplot(413)

                tstart = UTCDateTime(detection.detect_time - 5.0)
                #ts = date2num(UTCDateTime(detection.detect_time)) - 7.5
                tend = UTCDateTime(detection.detect_time + 20.0)
                #te = date2num(UTCDateTime(detection.detect_time)) + 20.0
        
                st1 = st.copy()
                st1 = st1.slice(starttime=tstart, endtime=tend)

                sp1spectrr = st1.copy()
                sp1spectr = sp1spectrr[0]
            
                sp1spectr.spectrogram(log=False, show=False, axes=ax3, wlen=0.5, cmap ='jet', dbscale=True)
                ax3.set_ylim(0, 70)

                st1det = st1.detrend(type='constant')
                st1det = st1det.taper(max_percentage=0.05, type="hann")

                st1filta = st1det.filter('bandpass', freqmin=fminb, freqmax=fmaxb, zerophase=True)
                
                ax3a=ax3.twinx()
                ax3a.plot(st1filta[0].times(), st1filta[0], 'k')
                ax3a.axvline((detection.detect_time - st1[0].stats.starttime), color='k', linestyle='--')  

            if st[0].stats.station == "SKDS":
                ax4 = plt.subplot(414)

                tstart = UTCDateTime(detection.detect_time - 5.0)
                #ts = date2num(UTCDateTime(detection.detect_time)) - 7.5
                tend = UTCDateTime(detection.detect_time + 20.0)
                #te = date2num(UTCDateTime(detection.detect_time)) + 20.0
        
                st1 = st.copy()
                st1 = st1.slice(starttime=tstart, endtime=tend)

                sp1spectrr = st1.copy()
                sp1spectr = sp1spectrr[0]
            
                sp1spectr.spectrogram(log=False, show=False, axes=ax4, wlen=0.5, cmap ='jet', dbscale=True)
                ax4.set_ylim(0, 70)

                st1det = st1.detrend(type='constant')
                st1det = st1det.taper(max_percentage=0.05, type="hann")

                st1filta = st1det.filter('bandpass', freqmin=fminb, freqmax=fmaxb, zerophase=True)
                
                ax4a=ax4.twinx()
                ax4a.plot(st1filta[0].times(), st1filta[0], 'k')
                ax4a.axvline((detection.detect_time - st1[0].stats.starttime), color='k', linestyle='--')  
        plt.savefig("spectrograms/"+str(detection.detect_time)+'spectrogram'+".png")
        plt.close()
