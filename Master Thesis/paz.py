import numpy as np
# sac and obspy get pole and zero in radian then all pole and zero must multiple in 2pi
# if pole and zero were in radian, then normalization factor must multiple in
# 2pi*(number of pole - number of zero)
paz = {
    'poles': [complex(-70.7e-3, 70.7e-3) * (2*np.pi),
              complex(-70.7e-3, -70.7e-3) * (2*np.pi),
              -393.011 * (2*np.pi),
              -7.4904 * (2*np.pi),
              complex(-53.5979, -21.7494) * (2*np.pi),
              complex(-53.5979, 21.7494) * (2*np.pi)],
    'zeros': [-5.03207 * (2*np.pi),
              0,
              0]
    }

sensor = dict( # 1
                T6180 = {'Z': {'sens': 1092.78, # V/m/s
                               'gain': 0.2732}, # uV/count
                         'N': {'sens': 1069.38,
                               'gain': 0.2553},
                         'E': {'sens': 1217.79,
                               'gain': 0.2597}},
                # 2
                T6215 = {'Z': {'sens': 1053.92,
                               'gain': 0.2760},
                         'N': {'sens': 1092.26,
                               'gain': 0.2676},
                         'E': {'sens': 1063.90,
                               'gain': 0.2555}},
                # 3
                T6219 = {'Z': {'sens': 1113.19,
                               'gain': 0.2702},
                         'N': {'sens': 1117.38,
                               'gain': 0.2654},
                         'E': {'sens': 1139.79,
                               'gain': 0.2724}},
                # 4
                T6226 = {'Z': {'sens': 1097.04,
                               'gain': 0.2702},
                         'N': {'sens': 1149.07,
                               'gain': 0.1677},
                         'E': {'sens': 1164.90,
                               'gain': 0.2642}},
                # 5
                T6249 = {'Z': {'sens': 1100.15,
                               'gain': 0.2723},
                         'N': {'sens': 1129.53,
                               'gain': 0.2694},
                         'E': {'sens': 1140.20,
                               'gain': 0.2654}},
                # 6
                T6252 = {'Z': {'sens': 1138.58,
                               'gain': 0.2674},
                         'N': {'sens': 1130.10,
                               'gain': 0.2663},
                         'E': {'sens': 1192.19,
                               'gain': 0.2789}},
                # 7
                T6254 = {'Z': {'sens': 1092.28,
                               'gain': 0.2720},
                         'N': {'sens': 1129.47,
                               'gain': 0.2695},
                         'E': {'sens': 1179.27,
                               'gain': 0.2711}},
                # 8
                T6259 = {'Z': {'sens': 1041.25,
                               'gain': 0.2680},
                         'N': {'sens': 1121.98,
                               'gain': 0.2645},
                         'E': {'sens': 1022.41,
                               'gain': 0.2554}},
                # 9
                T6260 = {'Z': {'sens': 1053.52,
                               'gain': 0.2780},
                         'N': {'sens': 1079.70,
                               'gain': 0.2674},
                         'E': {'sens': 1131.16,
                               'gain': 0.2863}},
                # 10
                T6266 = {'Z': {'sens': 1121.06,
                               'gain': 0.2702},
                         'N': {'sens': 1016.18,
                               'gain': 0.2551},
                         'E': {'sens': 991.07,
                               'gain': 0.2531}},
                # 11
                T6267 = {'Z': {'sens': 1070.22,
                               'gain': 0.2852},
                         'N': {'sens': 1138.04,
                               'gain': 0.2656},
                         'E': {'sens': 1095.86,
                               'gain': 0.2616}},
                # 12
                T6269 = {'Z': {'sens': 999.35,
                               'gain': 0.2616},
                         'N': {'sens': 1016.23,
                               'gain': 0.2498},
                         'E': {'sens': 1078.15,
                               'gain': 0.2595}},
                # 13
                T6289 = {'Z': {'sens': 1086.90,
                               'gain': 0.2752},
                         'N': {'sens': 1105.58,
                               'gain': 0.2655},
                         'E': {'sens': 1373.95,
                               'gain': 0.2896}})
               
               

from obspy import read
from obspy.signal import PPSD
from os.path import join
from myfunc.correction import correction_stations
import glob
import os
from obspy.imaging.cm import pqlx
list_days = sorted(glob.glob(join('..', 'days', '*')))
for day in list_days:
    list_files = sorted(glob.glob(join(day, '*')))
    for f in list_files:
        print(f)
        paz1 = paz
        try:
            st = read(f)
            _sensor = st[0].stats.station
            if _sensor == 'CMG6':
                _sensor = '6252'
            comp = st[0].stats.channel[-1]
            paz1['gain'] = 1/(sensor[f'T{_sensor}'][comp]['gain'] * 1e-6)
            paz1['sensitivity'] = sensor[f'T{_sensor}'][comp]['sens'] * (1.983*1e6)*(2*np.pi)**3
            correction_stations(st)
            st.detrend('constant')
            st.merge(method=1, fill_value=0)
            tr = st[0]
            print(tr)
            ppsd = PPSD(tr.stats, paz1, ppsd_length=600.0, overlap=0.5)
            ppsd.add(st)
            outpath = join('PSD', tr.stats.station, tr.stats.channel)
            os.makedirs(outpath, exist_ok=True)
            name = f'{tr.stats.starttime.date}_{tr.id}_PPSD.png'
            ppsd.plot(filename=join(outpath, name), show=False, cmap=pqlx)
        except Exception as error:
            print('!!!!!!!!!!!!!!!!!!! Problem !!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(error)
            #raise
