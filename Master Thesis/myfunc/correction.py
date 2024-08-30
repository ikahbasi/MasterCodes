############################
#     by IMAN KAHBASI      #
# master students in IIEES #
#               1399-03-02 #
############################


#########################################################################
def select_proper_events(cat, min_num_stations, min_azimuthal_gap):
    for ev in cat:
        for pick in ev.picks:
            if pick.phase_hint is None:
                continue
            if len(pick.waveform_id.station_code) == 3:
                pick.clear()
            elif pick.waveform_id.station_code in ['KHRI', 'NADH']:
                pick.clear()
        ev.picks = [p for p in ev.picks if p.phase_hint is not None]

    cat.events = [ev for ev in cat if len(ev.picks) != 0]
    for ev in cat:
        stations_count = len({pick.waveform_id.station_code
                              for pick in ev.picks})
        ev.origins[0].quality.used_station_count = stations_count
    new_cat = cat.filter(f'used_station_count >= {min_num_stations}',
                         f'azimuthal_gap <= {min_azimuthal_gap}')
    return new_cat


#############################################################################
def dic_max_cc(detect):
    max_cc = {}
    for pick in detect.event.picks:
        if pick.comments == []:
            continue
        _id = pick.waveform_id.get_seed_string()
        cc = float(pick.comments[0].text.split('=')[-1])
        max_cc[_id] = cc
    return max_cc


#############################################################################
def mag2event(ev, mag=0, magType='ML'):
    from obspy.core.event.magnitude import Magnitude
    from obspy.core.event.base import CreationInfo
    from obspy import UTCDateTime as utc

    resource_id = ev.resource_id
    magnitude_type = magType
    origin_id = ev.preferred_origin_id
    creation_info = CreationInfo(agency_id='IIEES', author='Iman-Kahbasi',
                                 creation_time=utc())
    mag = Magnitude(
                resource_id=resource_id,
                mag=mag,
                magnitude_type=magnitude_type,
                origin_id=origin_id,
                creation_info=creation_info
                    )
    ev.magnitudes.append(mag)


#########################################################################
def remove_low_weight_phases(catalog, min_p=3, min_s=1, min_weight=4):
    removed = 0
    for ii in range(catalog.count()):
        event = catalog[ii]
        origin = event.origins[0]
        arrivals = origin.arrivals
        for arrival in arrivals:
            # print(arrival)
            weight = arrival.time_weight
            if weight >= min_weight:
                pick_id = arrival.pick_id
                for pick in event.picks:
                    if str(pick_id) == str(pick.resource_id):
                        pick.clear()
        event.picks = [p for p in event.picks if p.waveform_id is not None]
        len_p = 0
        len_s = 0
        for pick in event.picks:
            if pick.phase_hint[0] == 'P':
                len_p += 1
            elif pick.phase_hint[0] == 'S':
                len_s += 1
        if len_p < min_p:
            catalog[ii] = None
            removed += 1
        if len_s < min_s:
            catalog[ii] = None
            removed += 1
    print(f'Number of detection that removed: {removed}')
    catalog.events = [event for event in catalog if event]
    

#########################################################################
def correction_phases(events):
    print('correaction-function: Start correct phases in catalog')
    for ev in events:
        ev.picks = [p for p in ev.picks if p.phase_hint is not None]
        ev.picks = [p for p in ev.picks if p.phase_hint != '']
        ev.picks = [p for p in ev.picks if p.phase_hint[:-1] != 'AM']
        for pick in ev.picks:
            # Get phase and channel of each pick
            phase = pick.phase_hint
            channel = pick.waveform_id.channel_code.replace('S', 'HH')
            # If phase is ok
            if (phase[0] == 'P' and channel[-1] == 'Z') or \
               (phase[0] == 'S' and channel[-1] in ['E', 'N']):
                pick.waveform_id.channel_code = channel
            # If P phase is not on channel Z
            elif (phase[0] == 'P' and channel[-1] != 'Z'):
                # change channel to Z in this pick
                channel = channel.replace('E', 'Z').replace('N', 'Z')
                pick.waveform_id.channel_code = channel
                print('event: ', str(ev.origins[0].time))
                print('P phase in station: ', pick.waveform_id.station_code)
                print('move from (E or N) to Z component\n')
            # If S phase is on channel Z
            elif (phase[0] == 'S' and channel[-1] == 'Z'):
                # change channel to E in this pick
                channel = channel.replace('Z', 'E')
                pick.waveform_id.channel_code = channel
                print('event: ', str(ev.origins[0].time))
                print('S phase in station: ', pick.waveform_id.station_code)
                print('move from Z to E component\n')
            else:
                print('event: ', str(ev.origins[0].time))
                print('!!! some unkown things happend !!!')
                print('station:', pick.waveform_id.station_code)
                print('phase:', phase, 'channel:', channel)


#############################################################################
def correction_stations(st):
    print('correaction-function: Start convert station name same as catalog')
    na_stations = {'6266': 'TONL', '6180': 'SKAR', '6289': 'EINS',
                   '6269': 'ANJR', '6254': 'ABTF', '6252': 'MAHO',
                   '6219': 'MIME', '6260': 'DLRN', 'CMG6': 'MAHO',
                   '6226': 'TIAK', '6259': 'JHAD', '6215': 'HONG',
                   '6267': 'GLGL', '6249': 'BARE',
                   '5645': 'TONL'}
    pass_list = []
    for tr in st:
        # Check for NA network
        if tr.stats.station in na_stations.keys():
            if tr.id not in pass_list:
                pass_list.append(tr.id)
                print('{} ---> {}'
                      .format(tr.id, na_stations[tr.stats.station]))
            tr.stats.network = 'NA'
            tr.stats.station = na_stations[tr.stats.station]
        # Find unknown station
        else:
            print('There is an unknow station:{}'.format(tr.id))


#############################################################################
def remove_gap_spike(st, len_spike=60):
    print(f'correaction-function:',
          'Remove probably gap-spike less than {len_spike}s')
    st.detrend('constant')
    # Remove short spike-gap of guralp data
    for tr in st:
        if abs(tr.data[0]) > 2.5 * abs(tr.data[1]):
            print('First sample changed to second sample value:', tr)
            tr.data.put([0], tr.data[1])
        if tr.stats.npts * tr.stats.delta <= len_spike:
            print('Probably gap-spike removed at', tr.id)
            st.remove(tr)


#############################################################################
def good_detections_in_party(party=None, catalog=None, min_stations=3):
    if party:
        num_dirty_cats = party.get_catalog().count()
        for family in party:
            for ii in range(len(family)):
                detection = family[ii]
                num_stations = len(set([pick.waveform_id.station_code for pick in detection.event.picks]))
                if num_stations < min_stations:
                    print(family.detections[ii].id, f'ignored.({num_stations} < {min_stations})')
                    family.detections[ii] = None
            family.detections = [d for d in family.detections if d is not None]
        num_clear_cats = party.get_catalog().count()
        print(f'* good_detections_in_party: {num_clear_cats} of {num_dirty_cats}')
    if catalog:
        for ev in cat:
            stations_count = len({pick.waveform_id.station_code
                                  for pick in ev.picks})
            ev.origins[0].quality.used_station_count = stations_count
        new_cat = cat.filter(f'used_station_count >= {min_stations}')
        return new_cat


#############################################################################
#ms2deci = lambda ms: int(ms[0:2]) + (float(ms[2:]))/60
def DMM2DD(minute_second):
    '''
    convert coordinate: `Degrees°.decimal_minutes ---> Decimal.degrees
                         2245.45                  ---> 22.7575
    '''
    minute = int(minute_second[0:2])
    second = float(minute_second[2:])
    decimal = minute + second/60
    return decimal

def DMS2DD(dg=None, mm=None, sc=None):
    '''
    convert coordinate: Degrees°minutes'seconds" --> Decimal.degrees
                        22°45'45                 --> 22.7625
    '''
    deci1 = dg
    deci2 = mm / 60
    deci3 = sc / 3600
    decimal = deci1 + deci2 + deci3
    return decimal

def deci2ms(decimal):
    pass
