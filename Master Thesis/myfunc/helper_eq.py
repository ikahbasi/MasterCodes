from eqcorrscan.core.match_filter.party import Party
import glob

def read_party(path, read_detection_catalog=True, estimate_origin=True):
    party = Party()
    _list = glob.glob(path)
    print('number of parties: ', len(_list))
    for ii, f in enumerate(sorted(_list)):
        print(f'{ii} of {len(_list)}')
        print(f)
        party += Party().read(f, read_detection_catalog=True, estimate_origin=True)
    return party

