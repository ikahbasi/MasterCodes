from myfunc.helper_eq import read_party
import numpy as np
import matplotlib.pyplot as plt
def autolabel(rects, fontsize=10):
    """Attach a text label above each bar in *rects*, displaying its height."""
    rects = zip(rects[0], rects[1])
    rects = list(rects)
    ax = plt.gca()
    width = 1#rects[1][1] - rects[0][1]
    for rect in rects:
        height = rect[0]
        ax.annotate('{}'.format(int(height)),
                    xy=(height, rect[1]),
                    xytext=(5, -5),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontsize)

party = read_party('/home/ehsan/Documents/kahbasi/main/run3/repicked-parties/*')

templates = []
detections = []
for family in party:
    #familyname = family.template.name
    #familyname = family.template.event.origins[0].time.datetime
    familyname = str(family.template.event.magnitudes[0].mag)
    number     = len(family.detections)
    if number == 59:
        print(familyname, number)
    templates.append(familyname)
    detections.append(number)

tem = [t for d, t in sorted(zip(detections, templates))]
det = sorted(detections)

templates = tem[-10:]
detections = det[-10:]
y = np.arange(len(templates))
fig, ax = plt.subplots(figsize=(10, 10))
rects1 = ax.barh(y, detections, 0.8, label='good phase', edgecolor='black', linewidth=1)
autolabel([detections, y])
ax.set_yticks(y)
ax.set_yticklabels(templates, weight='bold')

fig.savefig('temVSnum.png', dpi=120, bbox_inches="tight")
