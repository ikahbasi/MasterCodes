import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
from matplotlib import cm

# time or depth
color_mode = 'depth'
data = np.genfromtxt("./AHAN.txt")
lon = data[:,0]
lat = data[:,1]
dep = data[:,6] * -1

if color_mode == 'time':
    color_mode=list(range(len(dep)))
else:
    color_mode = dep
lon_lat = []
for n, t in zip(lon, lat):
    lon_lat.append([n, t])

def init():
    pathcol.set_offsets([[], []])
    pathcol.set_facecolor([])
    return [pathcol]

def update(i, pathcol, lon_lat):
    pathcol.set_offsets(lon_lat[:i])
    pathcol.set_color(cmap(norm(color_mode[:i])))
    return pathcol,

fig,[ax, cax] = plt.subplots(1, 2, gridspec_kw={"width_ratios":[50,1]})
xmin, xmax = np.min(lon), np.max(lon)
ymin, ymax = np.min(lat), np.max(lat)
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_facecolor('darkgray')
fig.patch.set_facecolor('xkcd:silver')
pathcol = ax.scatter([], [], c=[], lw=0.2, s=2)
# color
cmap = cm.gist_rainbow #hsv #rainbow
norm = mpl.colors.Normalize(vmin=np.min(color_mode), vmax=np.max(color_mode))
cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                norm=norm,
                                orientation='vertical')
cb1.set_label('Depth', rotation=270)

anim = FuncAnimation(fig, update, init_func=init, fargs=(pathcol, lon_lat),
                     interval=0.2, frames=len(lon), blit=True, repeat=True,
                     repeat_delay=3*10**3)
plt.show()
'''
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=20)
ani.save("demo2.gif", writer=writer)
'''
#anim.save('tmp.gif', writer='imagemagick')
