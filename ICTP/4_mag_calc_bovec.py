# coding: utf-8

import os
import glob

from eqcorrscan.core.match_filter import read_detections

from obspy import read, read_inventory
from obspy.io.xseed import Parser
from obspy.geodetics.base import gps2dist_azimuth

from math import log10, log
import numpy as np

outfile = open("event_magnitudes_ml", "w")
#######################################################
### Set parameters
######################################################

fmin = 1.25
fmax = 20.0
cont_folder = ('24h/')
event_lat = 45.7693
event_lon = 14.1971

######################################################
### resp files
######################################################
pre_filt = (0.005, 0.006, 30.0, 35.0)

######################################################

detections = read_detections("6s_detections_ok")
print "Detection file(s) read..."



for i, detection in enumerate(detections):
    
    print "Calculating ", i+1, "of", len(detections)
    try:
       ml = []
       ml_all = []

       year = detection.detect_time.year
       month = detection.detect_time.month
       day = detection.detect_time.day
       doy = detection.detect_time.strftime('%j')
       st = read(cont_folder+doy+'/'+'*')

       # Prepare the waveform data
       print "Setting sampling rates of the traces"
       for tr in st:
           if tr.stats.station == "VINO": 
               if tr.stats.sampling_rate != 100.0:
                   tr.stats.sampling_rate=100.0
           elif tr.stats.sampling_rate == "TRI":
               if tr.stats.sampling_rate != 100.0:
                   tr.stats.sampling_rate=100.0
           else:
               if tr.stats.sampling_rate != 200.0:
                   tr.stats.sampling_rate = 200.0
       print "Merging traces"
       st.merge(method=1, fill_value=0)
       print "Detrending traces"
       st.detrend('constant')

       # Get the detection times and cut the data around the detection time
       for tr in st:
           if tr.stats.station == "CEY":
               tstart = detection.detect_time
               tend = tstart + 20.0
           elif tr.stats.station == "SKDS":
               tstart = detection.detect_time
               tend = tstart + 20.0
           elif tr.stats.station == "KNDS":
               tstart = detection.detect_time
               tend = tstart + 20.0
           elif tr.stats.station == "JAVS":
               tstart = detection.detect_time
               tend = tstart + 20.0

       st1a = st.slice(starttime=tstart, endtime=tend)
       st1a = st1a.taper(max_percentage=0.05, type="hann")
       #st1a.write("detections_mseeds/"+str(detection.detect_time)+".mseed", format="MSEED")
       #print "Done cutting", detection.detect_time

       st1a.filter("bandpass", freqmin=fmin, freqmax=fmax)
       #st1a.plot()
       stations = []
       for tr in st1a:
           sta = tr.stats.station
           stations.append(sta)

       stations = list(set(stations))

       for sta in stations:

           amp_e = None
           amp_n = None
           amp_z = None
           
           #Disp is in meters!
           st_sta = st1a.select(station=sta)
           st_sta.remove_response(inventory=read_inventory("../../../stationxml/"+str(st_sta[0].stats.station).lower()+".xml"), output='DISP', pre_filt=pre_filt)
           hhe = st_sta.select(channel="HHE")
           for he in hhe:
               ampl_e = max(abs(he.data))
               ampl_e = ampl_e/1000
               amp_e = ampl_e
           hhn = st_sta.select(channel="HHN")
           for ne in hhe:
               ampl_n = max(abs(ne.data))
               ampl_n = ampl_n/1000
               amp_n = ampl_n
           hhz = st_sta.select(channel="HHZ")
           for ze in hhz:
               ampl_z = max(abs(ze.data))
               ampl_z = ampl_z/1000
               amp_z = ampl_z

           ampl = max(amp_e, amp_n)
           ampl_all = max(amp_e, amp_n, amp_z)
           
           print ampl
           
           staxml = read_inventory("../../../stationxml/"+str(st_sta[0].stats.station).lower()+".xml")
           
           epi_dist, az, baz = gps2dist_azimuth(float(event_lat), float(event_lon), float(staxml[0][0].latitude), float(staxml[0][0].longitude))
           epi_dist = epi_dist/1000.0
           
           print "Epicentral distance of ", sta, "is ", epi_dist

           if 0.0 <= epi_dist <= 5.0:
               corr = 1.4
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante)
               print "Claculating with correction ", corr
           elif 5.0 < epi_dist <= 10.0:
               corr = 1.4
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante)
               print "Claculating with correction ", corr
           elif 10.0 < epi_dist <= 15.0:
               corr = 1.5
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante)
               print "Claculating with correction ", corr
           elif 15.0 < epi_dist <= 20.0:
               corr = 1.6
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante)
               print "Claculating with correction ", corr
           elif 20.0 < epi_dist <= 25.0:
               corr = 1.7
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante) 
               print "Claculating with correction ", corr
           elif 25.0 < epi_dist <= 30.0:
               corr = 1.9
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante)
               print "Claculating with correction ", corr
           elif 30.0 < epi_dist <= 35.0:
               corr = 2.1
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante)
               print "Claculating with correction ", corr
           elif 35.0 < epi_dist <= 40.0:
               corr = 2.3
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante) 
               print "Claculating with correction ", corr
           elif 40.0 < epi_dist <= 45.0:
               corr = 2.4
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante)
               print "Claculating with correction ", corr
           elif 50.0 < epi_dist <= 55.0:
               corr = 2.5
               ml_ante = log(float(ampl),10) + corr
               ml.append(ml_ante) 
               print "Claculating with correction ", corr                                                                                              

       net_mag = round(np.median(ml),2)

       print detection.detect_time, net_mag
       print >>outfile, detection.detect_time, net_mag

    except IndexError:
       print >>outfile, detection.detect_time, "error in wfs (prop some station / chann is not working, check"
    except TypeError:
       print >>outfile, detection.detect_time, "TypeError error in wfs (prop some station / chann is not working, check"
