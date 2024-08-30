"""
Created on Mon Dec  9 18:05:23 2019

@author: imon
cat xyzm.dat |sort -nk13 -nk14 -nk15 -nk16 -nk17 > tmp.txt
"""
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animat

def update_graph(num):
    graph.set_data (x[:num], y[:num])
    graph.set_3d_properties(z[:num])
#    title.set_text('3D Test, events={}'.format(num))
    return title, graph, 


data = np.genfromtxt("tmp.txt")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
title = ax.set_title('3D Test')

graph, = ax.plot(x, y, z, linestyle="", marker=",")

ani = animat.FuncAnimation(fig, update_graph, len(x), interval=1, blit=True)

plt.show()
