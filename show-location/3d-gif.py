"""
Created on Mon Dec  9 17:48:25 2019

@author: imon
https://stackoverflow.com/questions/41602588/matplotlib-3d-scatter-animations
cat xyzm.dat |sort -nk13 -nk14 -nk15 -nk16 -nk17 > tmp.txt
"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animat

def update_graph(num):
    graph._offsets3d = (x[:num], y[:num], z[:num])
#    title.set_text('3D Test, time={}'.format(num))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
title = ax.set_title('3D Test')

data = np.genfromtxt("tmp.txt")
x = data[:,0]
y = data[:,1]
z = data[:,2]

graph = ax.scatter(x, y, z, marker='x')

ani = animat.FuncAnimation(fig, update_graph, frames=len(x), interval=0.001, blit=False)
plt.show()
