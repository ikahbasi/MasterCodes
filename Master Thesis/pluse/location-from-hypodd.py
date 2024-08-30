from obspy import UTCDateTime as utc
import numpy as np
from obspy import read_events
from myfunc.plot import twoD_seismplot, threeD_seismplot

data = np.genfromtxt("/home/ehsan/Documents/kahbasi/main_19mordad/hypodd/hypoDD.reloc")
lat = data[:,1]
lon = data[:,0]
depth = data[:,2] * -1

sec = data[:,-9].astype(str)
mint = data[:,-10].astype(int).astype(str)
hour = data[:,-11].astype(int).astype(str)
day = data[:,-12].astype(int).astype(str)
month = data[:,-13].astype(int).astype(str)
year = data[:,-14].astype(int).astype(str)


Date = []
for ii in range(len(year)):
    date = '{}-{}-{}T{}:{}:{}'.format(year[ii], month[ii], day[ii], hour[ii], mint[ii], sec[ii])
    print(date)
    Date.append(utc(date))

locations = []    
for ii in range(len(lat)):
    locations.append((lat[ii], lon[ii], depth[ii], Date[ii]))
    
    

#twoD_seismplot(locations=locations, method='depth')
#twoD_seismplot(locations=locations, method='time')



nodes = []    
for ii in range(len(lat)):
    nodes.append((lat[ii], lon[ii], depth[ii]))
threeD_seismplot(location_children=nodes)
#threeD_seismplot(stations=[nodes[0]], nodes=nodes)

