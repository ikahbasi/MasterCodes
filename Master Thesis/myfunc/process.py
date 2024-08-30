############################
#     by IMAN KAHBASI      #
# master students in IIEES #
#               1399-03-02 #
############################
import numpy as np


#########################################################################
def good_data(st, minhr=19.2, sps=100):
    #print('correaction-function: Remove short data or has too zeros')
    min_npts = minhr * 3600 * sps
    st.detrend('constant')
    # Remove traces that are shorter than the Hours
    st_ids = list({tr.id for tr in st})
    for st_id in st_ids:
        my_st = st.select(id=st_id)
        npts = 0
        for tr in my_st:
            npts += tr.stats.npts
        if npts < min_npts:
            print('This data removed (minimume time):', st_id, f'({npts/100/3600:.2f} hr)')
            for tr in my_st:
                st.remove(tr)
    # Remove traces that has too zeros
    st_ids = list({tr.id for tr in st})
    for st_id in st_ids:
        my_st = st.select(id=st_id)
        npts = 0
        zeros = 0
        for tr in my_st:
            npts += tr.stats.npts
            zeros += np.count_nonzero(abs(tr.data) <= 1)
        gap_npts = (24*3600*sps) - npts
        if zeros + gap_npts > 0.5*24*3600*sps:
            print('This data removed (had too zeros):', st_id, f'({gap_npts/100/3600:.2f}hr-gap & {zeros/100/3600:.2f}hr-zeros)')
            for tr in my_st:
                st.remove(tr)


#############################################################################
def processing_stream(st, good_data_run=True):
    from myfunc.correction import correction_stations
    correction_stations(st)  # name stations
    # remove_gap_spike(st) # remove data less than 60s
    st.merge(method=1)  # solve overlaps
    st = st.split()  # solve masked data
    if good_data_run:
        good_data(st, minhr=19.2)  # remove too gaps or zeros
    st.merge()
    return st
