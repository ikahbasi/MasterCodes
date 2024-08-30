from myfunc.helper_eq import read_party
from myfunc.qcontrol import hist_sum_cc_repicked, detection_pre_template, run
import glob
from os.path import join, basename
_list = glob.glob('./filter_test/run*')
for path in _list:
    print(path)
    run(path)
    name = basename(path)
    '''
    party_path = join(path, 'repicked_parties', '*')
    print(name,
          path,
          party_path)
    party = read_party(party_path)
    '''
#    detection_pre_template(party, save=True, show=False,
#                           savefile=join(path, f'detection_pre_template({name}).png'))
#    hist_sum_cc_repicked(party, pre_channel=False, save=True, show=False,
#                         savefile=join(path, f'repicked_parties-not-pre-channel({name}).png'))
