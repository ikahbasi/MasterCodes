from datetime import datetime
import matplotlib.pyplot as plt


magfile=open("event_magnitudes_ml", "r")

#magnitudes_h = []
magnitudes_v = []
times = []

for line in magfile:
    element = line.split(" ")
    dt = element[0]
    #mag_h = element[2]
    mag_v = element[1].rstrip()

    time = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")

    #magnitudes_h.append(mag_h)
    magnitudes_v.append(mag_v)
    times.append(time)


fig = plt.figure()
ax = fig.add_subplot(2,1,1, axisbg='white')
ax.plot(times, magnitudes_v, 'ro')

plt.title('MAG vs TIME')
plt.xlabel('TIME')
plt.show()


