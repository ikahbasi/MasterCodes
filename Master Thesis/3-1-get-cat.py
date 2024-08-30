from myfunc.helper_eq import read_party
import os
from os.path import join
from myfunc.parameters import parameters
# parameters
params = parameters.get_cat()
print(params)
Input = params.Input
output = params.output
# read party
path = join(Input, 'repicked-parties', '*party*')
party = read_party(path)
party.min_chans(min_chans=params.min_chans)
cat = party.get_catalog()


output = join(output, 'catalog')
os.makedirs(output, exist_ok=True)

if params.nordic:
    cat.write(join(output, 'nordic.out'),
              format="NORDIC")

if params.quakeml:
    cat.write(join(output, 'quakeml.xml'),
              format="QUAKEML")

if params.nlloc:
    os.makedirs(join(output, 'nlloc'), exist_ok=True)
    list_of_problem = []
    for ev in cat:
        _id = ev.resource_id.id
        try:
            ev.write(join(output, 'nlloc', f'{_id}.hyp'),
                     format="NLLOC_OBS")
        except Exception as error:
            list_of_problem.append(ev)
            print(error)
            print(_id)
