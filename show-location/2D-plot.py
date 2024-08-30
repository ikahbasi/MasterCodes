import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np




data = np.genfromtxt("./tmp.txt")
lon = data[:,0]
lat = data[:,1]
dep = data[:,2] * -1


fig = plt.figure()
fig.patch.set_facecolor('xkcd:silver')
plt.scatter(lon, lat, marker=',', c=dep, cmap='gist_rainbow',lw=0, s=2)
plt.gca().set_facecolor('darkgray')
plt.colorbar()
plt.show()

'''
colors = plt.cm.jet(np.linspace(0,1,len(dep)))
for ii in range(len(dep)):
    plt.plot(lon[ii], lat[ii], marker='x', c=colors[ii], linewidth=0.6)
plt.colorbar()
plt.show()
'''
