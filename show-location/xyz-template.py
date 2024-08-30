from obspy import read_events
import glob

path_of_quakeml = './quakeml/'
catalog = glob.glob(path_of_quakeml+"*.xml")
events = read_events(path_of_quakeml+'*.xml')

output = open('xyz-templates.txt', 'w')

for ev in events:
    cord = ev.origins[0]
    lat = cord.latitude
    lon = cord.longitude
    depth = cord.depth
    print(lat, lon, depth)
    output.write('{}\t{}\t{}\n'.format(lon, lat, depth/1000))

output.close()
