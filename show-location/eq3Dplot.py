def threeD_seismplot(stations, nodes, templates, **kwargs):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from eqcorrscan.utils.plotting import _finalise_figure
    stalats, stalongs, staelevs = zip(*stations)
    evlats, evlongs, evdepths = zip(*nodes)
    templats, templongs, tempdepths = zip(*templates) #iman
    # Cope with +/-180 latitudes...

    _evlongs = []
    for evlong in evlongs:
        if evlong < 0:
            evlong = float(evlong)
            evlong += 360
        _evlongs.append(evlong)
    evlongs = _evlongs

    _stalongs = []
    for stalong in stalongs:
        if stalong < 0:
            stalong = float(stalong)
            stalong += 360
        _stalongs.append(stalong)
    stalongs = _stalongs

    _templongs = [] #iman
    for templong in templongs: #iman
        if templong < 0: #iman
            templong = float(templong) #iman
            templong += 360 #iman
        _templongs.append(templong) #iman
    templongs = _templongs #iman
    tempdepths = [-1 * depth for depth in tempdepths] #iman

    evdepths = [-1 * depth for depth in evdepths]

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(evlats, evlongs, evdepths, marker="x", c="k",
               label='Hypocenters')
    ax.scatter(stalats, stalongs, staelevs, marker="v", c="r",
               label='Stations')

    ax.scatter(templats, templongs, tempdepths, marker="x", c="b",#iman
               label='templates')#iman
    ax.set_ylabel("Longitude (deg)")
    ax.set_xlabel("Latitude (deg)")
    ax.set_zlabel("Elevation (km)")
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.legend()
    fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover
    return fig
