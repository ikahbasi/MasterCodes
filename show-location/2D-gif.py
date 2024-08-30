"""
Created on Mon Dec  9 14:53:41 2019

@author: imon
https://stackoverflow.com/questions/37111571/how-to-pass-arguments-to-animation-funcanimation
cat xyzm.dat |sort -nk13 -nk14 -nk15 -nk16 -nk17 > tmp.txt

"""
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np

data = np.genfromtxt("AHAN.txt")
lon = data[:, 0]
lat = data[:, 1]

fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot([], [], ',', linewidth=4)
line2, = ax.plot([], [], ',', linewidth=4)
ax.set_xlim(np.min(lon), np.max(lon))
ax.set_ylim(np.min(lat), np.max(lat))

def animate(i,factor):
    line.set_xdata(lon[:i])
    line.set_ydata(lat[:i])
#    line2.set_xdata(lon[:i])
#    line2.set_ydata(factor*lat[:i])
    return line, line2

K = 0.75 # any factor 
ani = animation.FuncAnimation(fig, animate, frames=len(lon), fargs=(K,),
                              interval=0.2, blit=True, repeat_delay=3*10**3)
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.show()
#ani.save('tmp.gif', writer='imagemagick')
'''
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=20)
ani.save("demo2.gif", writer=writer)
'''
