import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

from matplotlib.cm import ScalarMappable



data = np.genfromtxt("./tmp.txt")
lon = data[:,0]
lat = data[:,1]
dep = data[:,2] * -1
time = range(len(dep))

fig = plt.figure(figsize=(15, 10))
fig.patch.set_facecolor('xkcd:silver')

gs = gridspec.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[3,1]) 
gs.update(wspace=0.01, hspace=0.01)

# lat and lon
ax0 = plt.subplot(gs[0])
ax0.set_xticks([])
ax0.set_facecolor('gray')

map0 = ax0.scatter(lon, lat, marker=',', c=time, cmap='gist_rainbow', lw=0, s=2)

plt.ylabel('Latitude')
#location of colorbar
divider0 = make_axes_locatable(ax0)
cax0 = divider0.append_axes("top", size="4%", pad="2%")
cbar0 = fig.colorbar(map0, ax=ax0, cax=cax0, orientation="horizontal")
cbar0.set_label('time', rotation=0, labelpad=-45, y=1.05)
cax0.xaxis.set_ticks_position("top")

# lat and depth
ax1 = fig.add_subplot(gs[1])
ax1.set_facecolor('gray')
ax1.set_yticks([])
map1 = ax1.scatter(dep, lat, marker=',', c=time, cmap='gist_rainbow',lw=0, s=2)
plt.xlabel('Depth')
ax1.invert_xaxis()
ax1_divider = make_axes_locatable(ax1)
cbaxes1 = ax1_divider.append_axes("top", size="4%", pad="2%")
cbar1 = fig.colorbar(map1, ax=ax1, cax=cbaxes1, orientation="horizontal")
cbar1.set_label('time', rotation=0, labelpad=-45, y=1.03)
cbaxes1.xaxis.set_ticks_position("top")


# long and depth
ax2 = plt.subplot(gs[2])
map2 = ax2.scatter(lon, dep, marker=',', c=time, cmap='gist_rainbow',lw=0, s=2)
plt.ylabel('Depth')
plt.xlabel('Longitude')
plt.gca().set_facecolor('gray')
ax2_divider = make_axes_locatable(ax2)
cbaxes2 = ax2_divider.append_axes("bottom", size="7%", pad="35%")
cbar2 = fig.colorbar(map2, ax=ax2, cax=cbaxes2, orientation="horizontal", pad=0.7)
cbar2.set_label('time', rotation=0, labelpad=-8, x=1.02)
ax2.xaxis.set_label_coords(1.02, -0.1)

fig.savefig('./time.png', dpi=200)
plt.show()

'''
colors = plt.cm.jet(np.linspace(0,1,len(dep)))
for ii in range(len(dep)):
    plt.plot(lon[ii], lat[ii], marker='x', c=colors[ii], linewidth=0.6)
plt.colorbar()
plt.show()
'''
