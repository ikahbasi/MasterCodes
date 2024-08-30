from eqcorrscan.core.match_filter import read_detections
from obspy import read, Stream
import glob
import os

detections_path = './detections/6s'
detection_files = glob.glob(os.path.join(detections_path, '*'))
st_path = '24h/'

for detection_file in detection_files:
    detections = read_detections(detection_file)
    print("Detection file(s) read: ", len(detections))
    for i, detection in enumerate(detections):
        #Cutting
        pad=0.2
        length=10.0

        #Filtering
        freqmin=3.0
        freqmax=12.0

        #Taper
        max_percentage = 0.01

        #streams = []
        cut_stream = Stream()

        #cut_stream = Stream()
        year = detection.detect_time.year
        doy = detection.detect_time.strftime('%j')
        st = read(st_path+str(doy)+"/"+"*")

        #Deal with strange sampling_rate in mseeds
        print("Setting sampling rates of the traces")
        for tr in st:
            if not tr.stats.station == "TRI":
                if tr.stats.sampling_rate != 200.0:
                    tr.stats.sampling_rate=200.0
            else:
                if tr.stats.sampling_rate != 100.0:
                    tr.stats.sampling_rate = 100.0

        #Merge stream
        print("Merging traces")
        st.merge(method=1, fill_value=0)
        st_cuted = st.copy()
        #st_cuted = st_cuted.trim(starttime=detection.detect_time- pad,
        #        endtime=detection.detect_time- pad + length).taper(max_percentage=max_percentage, type="hann")
        st_cuted = st_cuted.trim(starttime=detection.detect_time- pad,endtime=detection.detect_time- pad + length)
        #st_cuted = st_cuted.interpolate(sampling_rate=st_cuted[0].stats.sampling_rate, starttime=detection.detect_time, npts=length*st_cuted[0].stats.sampling_rate)

        print(st_cuted)
        print("Saving as mseed...", i+1, "of ", len(detections))

        st_cuted.write("events/"+str(detection.detect_time)+".mseed", format="MSEED")
    else:
        pass
