from eqcorrscan.core import match_filter, lag_calc
from eqcorrscan.utils import pre_processing
from eqcorrscan.utils.plotting import detection_multiplot
from obspy import read, Catalog
import glob
import os

# Read in the templates
template_path = './templates'
template_files = glob.glob(os.path.join(template_path, '*'))

templates = []

for template_file in template_files:
    templates.append(read(template_file))
for template in templates:
    template.merge()
    for tr in template:
        # Change channel names to two letters because EQcorrscan uses Seisan
        # style channel names, which are not standard, and should be changed!
        # Note that I might change EQcorrscan to use proper three letter
        # chanel names in a future release, but I will ensure it works with
        # two letter channel names too.
        tr.stats.channel = tr.stats.channel[0] + tr.stats.channel[-1]
        #pre_processing.shortproc(st=tr, lowcut=3.0, highcut=6.0, filt_order=3, samp_rate=20)

days =os.listdir('./24h/')
    
      
for day in sorted(days):
  # Create detections and detections/6s folder that are used for detection files
  if not os.path.isdir("detections/") == True:
    os.system("mkdir detections")
    os.system("mkdir detections/6s")
    
  print("Days with data: ", sorted(days))
  print("Number of days with data: ", len(days))
  print("Match filter started for day: ", day)

  # Read in and process the daylong data
  # There is something wrong with the way, Antelope is setting sampling rate to the miniseeds...
  # This is why you need to manualy set to 200Hz - miniseeds are at 199.99Hz.
  st = read('24h/'+day+'/*')
  print("Setting sampling rates of the traces")
  for tr in st:
    tr.stats.channel = tr.stats.channel[0] + tr.stats.channel[-1]
    if not tr.stats.station == "VINO": 
      if tr.stats.sampling_rate != 200.0:
        tr.stats.sampling_rate=200.0
    else:
      if tr.stats.sampling_rate != 100.0:
        tr.stats.sampling_rate = 100.0
  print("Merging traces")
  st.merge(method=1, fill_value=0)
  print("Detrending traces")
  st.detrend('constant')
  # Remove traces that are shorter then 17280000 samples (otherwise this will not work). What can be done?
  print("Removing traces shorter then 17270000 samples")
     
  for tr in st:
    if not tr.stats.station == "VINO":
      if len(tr) < 17270000:
        st.remove(tr)
        print("trace with less then 17280000 and not PRED:", tr.stats.station)
    else:
      if len(tr) < 8640000:
        st.remove(tr)
        print("trace with less then 8640000 samples removed:", tr.stats.station)
  # Some streams will be empty after st.remove, so we cant do anything with them...
  if len(st) == 0:
    pass
  else:


    # Use the same filtering and sampling parameters as your template!
    print("Preprocessing stream")
    #st = pre_processing.shortproc(st, lowcut=3.0, highcut=6.0, filt_order=3,
    #                    samp_rate=20,
    #                    starttime=st[0].stats.starttime)
    # Forced Daylong
    st = pre_processing.dayproc(st, lowcut=3.0, highcut=6.0, filt_order=3,
                        samp_rate=20,
                        starttime=st[0].stats.starttime)



    print(st.__str__(extended=True))            
       
    ####
    print("Starting with match filter")
    detections = match_filter.match_filter(template_names=template_files,
                                           template_list=templates, st=st,
                                           threshold=9, threshold_type='MAD',
                                           trig_int=3, plotvar=False, plotdir=('./plots'),
                                           cores=6)
    ####
    for detection in detections:
         detection.write("detections/"+day+'_detections', append=True)


    ####
    unique_detections = []
    
    for master in detections:
        if float(master.threshold) != 0 and (abs(float(master.detect_val))/float(master.threshold) > (1.05)):
            keep = True
            for slave in detections:
                if not master == slave and\
                    abs(master.detect_time - slave.detect_time) <= 6.0:
                    # If the events are within 6s of each other then test which
                    # was the 'best' match, strongest det
                    if not master.detect_val > slave.detect_val:
                        keep = False
                        break
            if keep:
                unique_detections.append(master)
    
    for detw in unique_detections:
         detw.write("detections/6s/"+day+'_detections_unique', append=True)
         print(detw.template_name)


    ####
    cat_cc = lag_calc.lag_calc(detections=unique_detections, detect_data=st, template_names=template_files, templates=templates, shift_len=0.2, min_cc=0.4, cores=6, interpolate=False, plot=False, parallel=True, debug=0)
    cat_cc.write("corrected.xml", format="QUAKEML")
    #cat_cc.write("corrected.nll", format="NLLOC_OBS")


    if not os.path.isdir("events_cc/") == True:
        os.system("mkdir events_cc")

    
    for event in cat_cc:
        #print(event.origins[0].time)
        event.write("events_cc/"+str(event.picks[0].time)+".hyp", format="NLLOC_OBS")
        event.write("events_cc/"+str(event.picks[0].time)+".xml", format="QUAKEML")
    
