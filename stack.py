from eqcorrscan.utils.clustering import space_cluster
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
time_event = '2017-11-12'
lat_event = 34.877
lon_event = 45.841
client = Client("IRIS")
starttime = UTCDateTime(time_event)
endtime = UTCDateTime("2018-01-01")
cat = client.get_events(starttime=starttime, endtime=endtime,
                        latitude = lat_event,
                                longitude = lon_event,
                                maxradius = 1)
groups = space_cluster(catalog=cat, d_thresh=1000, show=False)
cat.plot()
