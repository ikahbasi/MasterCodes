##################
## Iman Kahbasi ##
##### IIEES ######
##################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
from matplotlib import cm
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

# time or depth
color_mode = 'depth'

data = np.genfromtxt("./AHAN.txt")
lon = data[:,0]
lat = data[:,1]
dep = data[:,6] * -1

if color_mode=='time':
    clon = clat = cdep = range(len(dep))
elif color_mode=='depth':
    clon, clat, cdep = lon, lat, dep

lon_lat = []
lat_dep = []
lon_dep = []
for n, t, p in zip(lon, lat, dep):
    lon_lat.append([n, t])
    lon_dep.append([n, p])
    lat_dep.append([p, t])


def init():
    map0.set_offsets([[], []])
    map0.set_facecolor([])
    map1.set_offsets([[], []])
    map1.set_facecolor([])
    map2.set_offsets([[], []])
    map2.set_facecolor([])
    return [map0, map1, map2,]

def update(i, map0, map1, map2, lon_lat, lat_dep, lon_dep):
    #lon-lat
    map0.set_offsets(lon_lat[:i])
    map0.set_color(cmap0(norm0(cdep[:i])))
    #lat-dep
    map1.set_offsets(lat_dep[:i])
    map1.set_color(cmap1(norm1(clon[:i])))
    #lon-dep
    map2.set_offsets(lon_dep[:i])
    map2.set_color(cmap2(norm2(clat[:i])))
    return map0, map1, map2

#fig,[ax, cax] = plt.subplots(1, 2, gridspec_kw={"width_ratios":[50,1]})
fig = plt.figure(figsize=(10, 7))
fig.patch.set_facecolor('#009999')
gs = gridspec.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[3,1]) 
gs.update(wspace=0.03, hspace=0.03)

xmin, xmax = np.min(lon), np.max(lon)
ymin, ymax = np.min(lat), np.max(lat)
dmin, dmax = np.min(dep), np.max(dep)

# color
if color_mode=='time':
    cmap0 = cm.gist_rainbow #hsv #rainbow
    norm0 = mpl.colors.Normalize(vmin=0, vmax=len(cdep))
    cmap2 = cmap1 = cmap0
    norm2 = norm1 = norm0
elif color_mode=='depth':
    cmap0 = cm.gist_rainbow #hsv #rainbow
    norm0 = mpl.colors.Normalize(vmin=np.min(cdep), vmax=np.max(cdep))

    cmap1 = cm.gist_rainbow #hsv #rainbow
    norm1 = mpl.colors.Normalize(vmin=np.min(clon), vmax=np.max(clon))

    cmap2 = cm.gist_rainbow #hsv #rainbow
    norm2 = mpl.colors.Normalize(vmin=np.min(clat), vmax=np.max(clat))

ax0 = plt.subplot(gs[0])
#ax0.set_xlim(xmin-0.5, xmax+0.5)
#ax0.set_ylim(ymin+0.5, ymax-0.5)
ax0.set_facecolor('#808080')
map0 = ax0.scatter(lon, lat, marker=',', c=cdep, cmap=cmap0, lw=0, s=2)
ax0.set_xlabel('long')
ax0.set_ylabel('lat')
ax0.set_xticks([])
divider0 = make_axes_locatable(ax0)
cax0 = divider0.append_axes("top", size="4%", pad="2%")
cbar0 = fig.colorbar(map0, ax=ax0, cax=cax0, orientation="horizontal")
cbar0.set_label('Depth', rotation=0, labelpad=-45, y=1.05)
cax0.xaxis.set_ticks_position("top")
#cbar0.ax.set_xticklabels(np.linspace(0, min(dep), 5), rotation=90)

ax1 = plt.subplot(gs[1])
#ax1.set_xlim(dmin+0.5, dmax0.5)
#ax1.set_ylim(ymin+0.5, ymax-0.5)
ax1.set_facecolor('#808080')
map1 = ax1.scatter(dep, lat, marker=',', c=clon, cmap=cmap1, lw=0, s=2)
ax1.set_xlim(dmin, dmax)
ax1.set_ylim(ymin, ymax)
ax1.set_xlabel('depth')
ax1.set_yticks([])
ax1.invert_xaxis()
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("top", size="4%", pad="2%")
cbar1 = fig.colorbar(map1, ax=ax1, cax=cax1, orientation="horizontal")
cbar1.set_label('Longitude', rotation=0, labelpad=-45, y=1.03)
cax1.xaxis.set_ticks_position("top")
#cbar1.ax.set_xticklabels(rotation=90)




ax2 = plt.subplot(gs[2])
#ax2.set_xlim(xmin-0.5, xmax+0.5)
#ax2.set_ylim(dmin+0.5, dmax-0.5)
ax2.set_facecolor('#808080')
map2 = ax2.scatter(lon, dep, marker=',', c=clat, cmap=cmap2, lw=0, s=2)
ax2.set_xlim(xmin, xmax)
ax2.set_ylim(dmin, dmax)
ax2.set_xlabel('long')
ax2.set_ylabel('depth')
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="7%", pad="35%")
cbar2 = fig.colorbar(map2, ax=ax2, cax=cax2, orientation="horizontal", pad=0.7)
cbar2.set_label('Latitude', rotation=0, labelpad=-8, x=1.02)
ax2.xaxis.set_label_coords(1.02, -0.1)
#cbar2.ax.set_xticklabels(cbar2.ax.get_xticklabels(), rotation=90)


anim = FuncAnimation(fig, update, init_func=init, fargs=(map0, map1, map2, lon_lat, lat_dep, lon_dep),
                     interval=0.02, frames=len(lon), blit=True, repeat=True,
                     repeat_delay=3*10**3)
plt.show()
'''
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=20)
anim.save("/home/imon/Desktop/demo3.gif", writer = "pillow", fps=5)


import matplotlib.animation as animation
Writer = animation.writers['ffmpeg']
#Writer = animation.writers['pillow']
writer = Writer(fps=40, metadata=dict(artist='Me'), bitrate=800)
anim.save('/home/imon/Desktop/time.mp4', writer=writer) #'imagemagick')

'''
