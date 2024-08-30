from eqcorrscan.core.match_filter.helpers import extract_from_stream
from eqcorrscan.core.match_filter.party import read_party
from correction_functions import *
import glob
from os.path import join
from obspy import read
from eqcorrscan.utils.plotting import plot_repicked


list_party = glob.glob(join('Run1', 'parties', '*'))
for f in list_party:
    print(f)
    party = read_party(f)
    party.decluster(10)
    detections = []
    st = read(join('days', str(party[0][0].detect_time.date), '*'))
    st = processing_stream(st)
    for family in party:
        detection_streams = family.extract_streams(stream=st,
                                                  length=20,
                                                  prepick=10)
        for _id, _st in detection_streams.items():
            _st.write(f'_id.msd', format='MSEED')
        stream = extract_from_stream(st, [detection], pad=10.0, length=10.0)
        plot_repicked(family.template.st, detection.event.picks, det_stream=stream[0])#, **kwargs)

#for stream, detection in zip(streams, detections):
#   plot_repicked(template, picks, det_stream, **kwargs)
