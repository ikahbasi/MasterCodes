from eqcorrscan.utils.plotting import cumulative_detections
from eqcorrscan.core.match_filter import read_detections
import datetime as dt
import os

path ="detections/6s/"
inputfilelist = os.listdir(path)

for inputfile in inputfilelist:
    print(inputfile)
    detections = read_detections("detections/6s/"+str(inputfile))

    if len(detections) <= 2:
        pass

    else:

        dates = []
        template_names = []
        detections_list = []

        for detection in detections:
            date = detection.detect_time
            dates.append(date)
            template_name = detection.template_name[11:]
            template_names.append(template_name)
            detections_list.append(detection)

        cumulative_detections(dates=dates, template_names=template_names, detections=detections_list, plot_grouped=True, show=True, plot_legend=False, save=False, savefile=None)
