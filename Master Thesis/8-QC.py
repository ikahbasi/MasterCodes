from myfunc.helper_eq import read_party
from myfunc.qcontrol import *
import glob
from os.path import basename, join
from obspy import read_events
from myfunc.parameters import parameters
params = parameters.QC()

basepath = params.Input
run_dirs = glob.glob(join(basepath, 'run*'))

for runpath in run_dirs:
    name = basename(runpath)
    repicked_parties = read_party(join(runpath, 'repicked-parties', '*'))
    repicked_catalog = repicked_parties.get_catalog()
    
    hist_scc(party=repicked_parties,
             path=join(basepath, 'QC'),
             name=name)
    
    hist_cc(party=repicked_parties,
            path=join(basepath, 'QC'),
            name=name)
    
    phases_pre_event(catalog=repicked_catalog,
                     path=join(basepath, 'QC', 'phases-pre-event'),
                     name=name)
                     
    phase_counter(catalog=repicked_catalog,
                  path=join(basepath, 'QC', 'phases-counter'),
                  name=name)
                  
    self_detection(party=repicked_parties,
                   num_reference_events=None,
                   path=join(basepath, 'QC', 'self-detection'),
                   name=name)
                    
# after locations
list_nordic_cats = glob.glob(join(basepath, 'located-nordics', 'nordic-*'))
for _dir in list_nordic_cats:
    print(_dir)
    run_name = basename(_dir)
    catalog = read_events(_dir)
    get_rms_phases_cat(catalog,
                       step=2,
                       name=f'{run_name}',
                       path=join(basepath, 'QC', 'rms'),
                       )

# after clean-locations
list_nordic_cats = glob.glob(join(basepath, 'clean-located-nordics', 'nordic-*'))
for _dir in list_nordic_cats:
    print(_dir)
    run_name = basename(_dir)
    catalog = read_events(_dir)
    get_rms_phases_cat(catalog,
                       step=0.1,
                       name=f'{run_name}',
                       path=join(basepath, 'QC', 'rms-clean'),
                       )


    phases_pre_event(catalog=catalog,
                     path=join(basepath, 'QC', 'phases-pre-event-clean-catalog'),
                     name=run_name)
                     
    phase_counter(catalog=catalog,
                  path=join(basepath, 'QC', 'phases-counter-clean-catalog'),
                  name=run_name)

