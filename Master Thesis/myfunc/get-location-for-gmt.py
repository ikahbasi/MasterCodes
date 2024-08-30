from obspy import read_events

catalog = read_events('Ilam_s1.out')

with open('1105events.txt', 'w') as out1105:
    for ev in catalog:
        lat = ev.origins[0].latitude
        lon = ev.origins[0].longitude
        print(f'{lon:.2f}   {lat:.2f}', file=out1105)


from myfunc.correction import select_proper_events

selected_cat = select_proper_events(cat=catalog,
                                    min_num_stations=3,
                                    min_azimuthal_gap=180)

with open('selected_events.txt', 'w') as out:
    for ev in selected_cat:
        lat = ev.origins[0].latitude
        lon = ev.origins[0].longitude
        print(f'{lon:.2f}   {lat:.2f}', file=out)

