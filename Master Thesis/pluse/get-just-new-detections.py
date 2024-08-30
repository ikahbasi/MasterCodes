from myfunc.helper_eq import read_party
import os
from os.path import join
from myfunc.parameters import parameters

def get_just_new_detections(party):
    for family in party:
        for ii, detect in enumerate(family):
            no_chans = detect.no_chans
            no_phase = len(detect.event.picks)
            if round(detect.detect_val, 2) == detect.no_chans:
                family.detections[ii] = None
        family.detections = [d for d in family if d is not None]

# parameters
params = parameters.get_cat()
print(params)
Input = params.Input
output = params.output
# read party
path = join('..', Input, 'repicked-parties', '*party*')
party = read_party(path)
party.min_chans(min_chans=params.min_chans)

get_just_new_detections(party)
cat = party.get_catalog()


output = join(output, 'catalog_just-new')
os.makedirs(output, exist_ok=True)

cat.write(join(output, 'nordic.out'), format="NORDIC")

