from eqcorrscan.core.match_filter import read_detections
import glob
import os

#detection_files =os.listdir('./detections/6s/')
detection_path = './detections/6s/'
detection_files = glob.glob(os.path.join(detection_path, '*'))

for detection_file in detection_files:
  detections = read_detections(detection_file)

  for detection in detections:
    if float(detection.threshold) != 0 and (abs(float(detection.detect_val))/float(detection.threshold) > (1.05)):
      detection.write('6s_detections_unique', append=True)
