"""
Created on Sun Dec  8 16:17:03 2019

@author: imon
"""

#from eqcorrscan.utils.plotting import threeD_seismplot
from eq3Dplot import threeD_seismplot

nodes = []
inp = open('xyzm.dat')
inp.readline()
for line in inp:
    lon = float(line.split()[0])
    lat = float(line.split()[1])
    depth = float(line.split()[2])
    
    nodes.append((lat, lon, depth))
    
stations = []
for line in open('station.txt'):
    lat = float(line.split()[1])
    lon = float(line.split()[0])
    stations.append((lat, lon, 0))

templates = []
for line in open('xyz-templates.txt'):
    lat = float(line.split()[1])
    lon = float(line.split()[0])
    depth = float(line.split()[2])
    templates.append((lat, lon, depth))

threeD_seismplot(stations, nodes, templates, show=True)
