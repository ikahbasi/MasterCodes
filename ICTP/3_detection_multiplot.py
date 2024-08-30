from eqcorrscan.utils.plotting import detection_multiplot
from eqcorrscan.core.match_filter import read_detections
from eqcorrscan.utils import pre_processing
from obspy import read

st = read("24h/015/*")
st = st.select(station="JAVS").select(channel="HHZ")
for tr in st:
        # Change channel names to two letters because EQcorrscan uses Seisan
        # style channel names, which are not standard, and should be changed!
        # Note that I might change EQcorrscan to use proper three letter
        # chanel names in a future release, but I will ensure it works with
        # two letter channel names too.
		tr.stats.channel = tr.stats.channel[0] + tr.stats.channel[-1]
		pre_processing.shortproc(st=tr, lowcut=3.0, highcut=6.0, filt_order=3, samp_rate=20)
print(tr)
template = read("templates/2010-01-12T08:20:26.044000Z.mseed")
template = template.select(station="JAVS").select(channel="HZ")
print(template)
template_name = "2010-01-12T08:20:26.044000Z"
detections = read_detections("detections/6s/015_detections_unique")

times = []

for detection in detections:
	if str(detection.template_name[12:-6]) == template_name:
		#print(detection)
		times.append(detection.detect_time)
	#print(str(detection.template_name[12:-6]), template[0].stats.starttime)


times = sorted(times)

detection_multiplot(stream=st, template=template, times=times, streamcolour=u'k',
                    templatecolour=u'r', save=False, savefile=None, size=(10.5, 7.5), title=None)
