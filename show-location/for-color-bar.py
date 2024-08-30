'''
https://stackoverflow.com/questions/51017398/how-do-you-add-a-colormap-to-a-matplotlib-animation/51025196
'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation


dataX = np.linspace(-50,50,1000)
dataY = np.linspace(-50,50,1000)
dataZ = np.linspace(-50,50,1000)


def animate(num):
    data = np.hstack((dataX[:num,np.newaxis], dataY[:num, np.newaxis]))
    art.set_offsets(data)
    art.set_color(cmap(norm(dataZ[:num]))) # update colors using the colorbar and its normalization defined below
    return art,


fig,[ax,cax] = plt.subplots(1,2, gridspec_kw={"width_ratios":[50,1]})
# Set the colormap and norm to correspond to the data for which
# the colorbar will be used.
cmap = matplotlib.cm.winter
norm = matplotlib.colors.Normalize(vmin=-50, vmax=50)

cb1 = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap,
                                norm=norm,
                                orientation='vertical')

ax.set_xlim(-60,60)
ax.set_ylim(-60,60)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('test')
art = ax.scatter([],[],c=[])

ani = animation.FuncAnimation(fig, animate, interval=2, blit=True, repeat=True)

plt.show()
