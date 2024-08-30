import numpy as np
from collections import Counter

def _finalise_figure(fig, **kwargs):  # pragma: no cover
    """
    Internal function to wrap up a figure.
    {plotting_kwargs}
    """
    import matplotlib.pyplot as plt
    #
    title = kwargs.get("title")
    show = kwargs.get("show", True)
    save = kwargs.get("save", False)
    savefile = kwargs.get("savefile", "EQcorrscan_figure.png")
    return_fig = kwargs.get("return_figure", False)
    size = kwargs.get("size", (10.5, 7.5))
    fig.set_size_inches(size)
    if title:
        fig.suptitle(title)
    if save:
        fig.savefig(savefile, bbox_inches="tight")
        print("Saved figure to {0}".format(savefile))
    if show:
        plt.show(block=True)
    if return_fig:
        return fig
    #fig.clf()
    plt.close(fig)
    return None


###############################################################################
def twoD_seismplot(catalog=None, locations=None, bgcolor='#909090',
                   method='depth', **kwargs):
    """
    Plot seismicity in a 2D map with two cross section along latitude and
    longitude.
    :type catalog: obspy.core.event.catalog.Catalog
    :param catalog: Obspy catalog class containing event metadata
    :type locations: list
    :param locations:
        list of one tuple per event of (lat, long, depth, time) with
        down positive.
    :type bgcolor: string
    :param bgcolor: Background's color of map and sections.
        all name or RGB code that acceptable in matplotlib.
    :type method: string
    :param method:
        making color palette of locations according to 'depth', 'time' or
        'sequence'.
    {plotting_kwargs}
    :returns: :class:`matplotlib.figure.Figure`
    .. note::
        If each location doesn't have time or depth, set them to zero.
    .. note::
        kwargs accepts all option that available in
        `matplotlib.axes.Axes.scatter`.
    """
    import matplotlib.pyplot as plt
    from matplotlib import gridspec
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    assert (catalog and locations) or catalog or locations,\
        "Requires catalog and/or locations"
    # set default parameters of plt.scatter()
    default_parameters = {'cmap': 'jet_r', 'marker': ',', 's': 1, 'lw': 1}
    for key in default_parameters.keys():
        if key not in kwargs.keys():
            kwargs[key] = default_parameters[key]
    # get parameters of _finalise_figure
    _kwargs = {}
    for key in ['title', 'show', 'save', 'savefile', 'return_fig', 'size']:
        if key in kwargs.keys():
            _kwargs[key] = kwargs[key]
            del kwargs[key]
    # making coordinates
    locations = locations or []
    msg = "An event of the catalog got ignored, because it didn't have origin"
    if catalog:
        for event in catalog:
            try:
                origin = event.preferred_origin() or event.origins[0]
            except IndexError:  # No origin found
                Warning(msg)
                continue
            _lat = origin.latitude
            _lon = origin.longitude
            _dep = origin.depth / 1000
            _time = origin.time
            locations.append((_lat, _lon, _dep, _time))
    # sort location according to method
    if method in ['time', 'sequence']:
        locations.sort(key=lambda ind: ind[3])
    elif method == 'depth':
        locations.sort(reverse=False, key=lambda ind: ind[2])
    lat, lon, dep, time = zip(*locations)
    if method == 'depth':
        c0, c1, c2 = dep, lon, lat
        label0, label1, label2 = 'Depth (km)', 'Longitude', 'Latitude'
    elif method == 'time':
        dt = [t - time[0] for t in time]
        c0 = c1 = c2 = dt
        label = f'Origin-time offset from {time[0]} (s)'
    elif method == 'sequence':
        c0 = c1 = c2 = range(len(dep))
        label = 'Event number'
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[3, 1],
                           wspace=0.01, hspace=0.01)
    # map view
    ax0 = plt.subplot(gs[0])
    ax0.set_facecolor(bgcolor)
    ax0.set_ylabel('Latitude')
    ax0.set_xticks([])
    map0 = ax0.scatter(lon, lat, c=c0, **kwargs)
    # cross section parallel to latitude (lat ,depth)
    ax1 = fig.add_subplot(gs[1])
    ax1.set_facecolor(bgcolor)
    ax1.set_yticks([])
    ax1.set_xlabel('Depth')
    map1 = ax1.scatter(dep, lat, c=c1, **kwargs)
    # cross section parallel to longitude (lon ,depth)
    ax2 = plt.subplot(gs[2])
    ax2.set_facecolor(bgcolor)
    ax2.invert_yaxis()
    ax2.set_ylabel('Depth')
    ax2.set_xlabel('Longitude')
    map2 = ax2.scatter(lon, dep, c=c2, **kwargs)
    # location of color bar
    if method == 'depth':
        #
        divider0 = make_axes_locatable(ax0)
        cax0 = divider0.append_axes("top", size="4%", pad="2%")
        cbar0 = fig.colorbar(map0, ax=ax0, cax=cax0, orientation="horizontal")
        cbar0.set_label(label0, rotation=0, labelpad=-45, y=1.05)
        cax0.xaxis.set_ticks_position("top")
        #
        divider1 = make_axes_locatable(ax1)
        cax1 = divider1.append_axes("top", size="4%", pad="2%")
        cbar1 = fig.colorbar(map1, ax=ax1, cax=cax1, orientation="horizontal")
        cbar1.set_label(label1, rotation=0, labelpad=-45, y=1.03)
        cax1.xaxis.set_ticks_position("top")
        #
        divider2 = make_axes_locatable(ax2)
        cax2 = divider2.append_axes("bottom", size="7%", pad="35%")
        cbar2 = fig.colorbar(map2, ax=ax2, cax=cax2, orientation="horizontal",
                             pad=0.7)
        cbar2.set_label(label2, rotation=0, labelpad=-8, x=1.02)
        ax2.xaxis.set_label_coords(1.02, -0.1)
    elif method == 'time' or method == 'sequence':
        divider1 = make_axes_locatable(ax1)
        cax1 = divider1.append_axes("right", size="4%", pad="2%")
        cbar1 = fig.colorbar(map1, ax=ax1, cax=cax1, orientation="vertical")
        cbar1.set_label(label)
    fig = _finalise_figure(fig=fig, **_kwargs)  # pragma: no cover
    return fig


###############################################################################
def freq_mag(ch_magnitudes=None, ch_completeness=None, ch_max_mag=None,
             tm_magnitudes=None, tm_completeness=None, tm_max_mag=None,
             binsize=0.2, **kwargs):
    """
    Plot a frequency-magnitude histogram and cumulative density plot.

    Currently this will compute a b-value, for a given completeness.
    B-value is computed by linear fitting to section of curve between
    completeness and max_mag.

    :type ch_magnitudes: list
    :param ch_magnitudes: list of float of children magnitudes (optional)
    :type ch_completeness: float
    :param ch_completeness: Level to compute the b-value above for children
        (optional)
    :type ch_max_mag: float
    :param ch_max_mag: Maximum magnitude to try and fit a b-value to children
        (optional)
    :type tm_magnitudes: list
    :param tm_magnitudes: list of float of templates magnitudes (optional)
    :type tm_completeness: float
    :param tm_completeness: Level to compute the b-value above for templates
        (optional)
    :type tm_max_mag: float
    :param tm_max_mag: Maximum magnitude to try and fit a b-value to templates
        (optional)
    :type binsize: float
    :param binsize: Width of histogram bins, defaults to 0.2
    {plotting_kwargs}

    :returns: :class:`matplotlib.figure.Figure`

    .. Note::
        See :func:`eqcorrscan.utils.mag_calc.calc_b_value` for a least-squares
        method of estimating completeness and b-value. For estimating maximum
        curvature see :func:`eqcorrscan.utils.mag_calc.calc_max_curv`.

    .. rubric:: Example

    >>> from obspy.clients.fdsn import Client
    >>> from obspy import UTCDateTime
    >>> from eqcorrscan.utils.plotting import freq_mag
    >>> client = Client('IRIS')
    >>> t1 = UTCDateTime('2012-03-26T00:00:00')
    >>> t2 = t1 + (3 * 86400)
    >>> catalog = client.get_events(starttime=t1, endtime=t2, minmagnitude=3)
    >>> ch_magnitudes = [event.preferred_magnitude().mag for event in catalog]
    >>> freq_mag(
    ...     ch_magnitudes, ch_completeness=4, ch_max_mag=7) # doctest: +SKIP

    .. plot::

        from obspy.clients.fdsn import Client
        from obspy import UTCDateTime
        from eqcorrscan.utils.plotting import freq_mag
        client = Client('IRIS')
        t1 = UTCDateTime('2012-03-26T00:00:00')
        t2 = t1 + (3 * 86400)
        catalog = client.get_events(starttime=t1, endtime=t2, minmagnitude=3)
        ch_magnitudes = [event.preferred_magnitude().mag for event in catalog]
        freq_mag(ch_magnitudes, ch_completeness=4, ch_max_mag=7)
    """
    import matplotlib.pyplot as plt
    # Ensure ch_magnitudes are sorted
    if ch_magnitudes:
        ch_magnitudes.sort()
    if tm_magnitudes:
        tm_magnitudes.sort()
    # Check that there are no nans or infs
    # Children
    if ch_magnitudes and np.isnan(ch_magnitudes).any():
        Logger.warning('Found nan values, removing them')
        ch_magnitudes = [mag for mag in ch_magnitudes if not np.isnan(mag)]
    if ch_magnitudes and np.isinf(ch_magnitudes).any():
        Logger.warning('Found inf values, removing them')
        ch_magnitudes = [mag for mag in ch_magnitudes if not np.isinf(mag)]
    # Templates
    if tm_magnitudes and np.isnan(tm_magnitudes).any():
        Logger.warning('Found nan values, removing them')
        tm_magnitudes = [mag for mag in tm_magnitudes if not np.isnan(mag)]
    if tm_magnitudes and np.isinf(tm_magnitudes).any():
        Logger.warning('Found inf values, removing them')
        tm_magnitudes = [mag for mag in tm_magnitudes if not np.isinf(mag)]
    fig, ax1 = plt.subplots()
    # Set up the bins, the bin-size could be a variables
    # Children
    if ch_magnitudes:
        ch_bins = np.arange(int(min(ch_magnitudes) - 1),
                            int(max(ch_magnitudes) + 1), binsize)
        ch_n, ch_bins, ch_patches = ax1.hist(
            ch_magnitudes, ch_bins, facecolor='g', alpha=0.5,
            label='Children magnitudes', edgecolor='black', linewidth=1.2)
    # Templates
    if tm_magnitudes:
        tm_bins = np.arange(int(min(tm_magnitudes) - 1),
                            int(max(tm_magnitudes) + 1), binsize)
        tm_n, tm_bins, tm_patches = ax1.hist(
            tm_magnitudes, tm_bins, facecolor='b', alpha=0.5,
            label='templates magnitudes', edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Frequency')
    if ch_magnitudes and tm_magnitudes:
        _max_y = max(max(ch_n), max(tm_n))
    elif ch_magnitudes:
        _max_y = max(ch_n)
    elif tm_magnitudes:
        _max_y = max(tm_n)
    ax1.set_ylim([0, _max_y * 1.5])
    plt.xlabel('Magnitude')
    # Now make the cumulative density function
    # Children
    if ch_magnitudes:
        ch_counts = Counter(ch_magnitudes)
        ch_cdf = np.zeros(len(ch_counts))
        ch_mag_steps = np.zeros(len(ch_counts))
        for i, magnitude in enumerate(sorted(ch_counts.keys(), reverse=True)):
            ch_mag_steps[i] = magnitude
            if i > 0:
                ch_cdf[i] = ch_cdf[i - 1] + ch_counts[magnitude]
            else:
                ch_cdf[i] = ch_counts[magnitude]
    # Templates
    if tm_magnitudes:
        tm_counts = Counter(tm_magnitudes)
        tm_cdf = np.zeros(len(tm_counts))
        tm_mag_steps = np.zeros(len(tm_counts))
        for i, magnitude in enumerate(sorted(tm_counts.keys(), reverse=True)):
            tm_mag_steps[i] = magnitude
            if i > 0:
                tm_cdf[i] = tm_cdf[i - 1] + tm_counts[magnitude]
            else:
                tm_cdf[i] = tm_counts[magnitude]
    # Plot
    ax2 = ax1.twinx()
    # ax2.scatter(ch_magnitudes, np.log10(cdf), c='k', marker='+', s=20, lw=2,
    # Children
    if ch_magnitudes:
        ax2.scatter(
            ch_mag_steps, np.log10(ch_cdf), c='g', marker='+', s=20, lw=2,
            label='Magnitude cumulative density of children')
    # Templates
    if tm_magnitudes:
        ax2.scatter(
            tm_mag_steps, np.log10(tm_cdf), c='b', marker='+', s=20, lw=2,
            label='Magnitude cumulative density of templates')
    # Now we want to calculate the b-value and plot the fit
    # Children
    if ch_magnitudes:
        ch_x = []
        ch_y = []
        for i, magnitude in enumerate(ch_mag_steps):
            if ch_completeness <= magnitude <= ch_max_mag:
                ch_x.append(magnitude)
                ch_y.append(ch_cdf[i])
        ch_fit = np.polyfit(ch_x, np.log10(ch_y), 1)
        ch_fit_fn = np.poly1d(ch_fit)
    # Templates
    if tm_magnitudes:
        tm_x = []
        tm_y = []
        for i, magnitude in enumerate(tm_mag_steps):
            if tm_completeness <= magnitude <= tm_max_mag:
                tm_x.append(magnitude)
                tm_y.append(tm_cdf[i])
        tm_fit = np.polyfit(tm_x, np.log10(tm_y), 1)
        tm_fit_fn = np.poly1d(tm_fit)
    # Children
    #if ch_magnitudes:
    #    ax2.plot(ch_magnitudes, ch_fit_fn(ch_magnitudes), '--g',
    #             label=f'GR trend, b-value (children) = {abs(ch_fit[0]):.5}' +
    #             f'\n $M_C$ = {ch_completeness}')
    # Templates
    if tm_magnitudes:
        ax2.plot(tm_magnitudes, tm_fit_fn(tm_magnitudes), '--b',
                 label=f'GR trend, b-value (templates) = {abs(tm_fit[0]):.5}' +
                 f'\n $M_C$ = {tm_completeness}')
    ax2.set_ylabel('$Log_{10}$ of cumulative density')
    if ch_magnitudes and tm_magnitudes:
        _min_mags = min(min(ch_magnitudes), min(tm_magnitudes))
        _max_mags = max(max(ch_magnitudes), max(tm_magnitudes))
        _min_cdf = min(min(np.log10(ch_cdf)), min(np.log10(tm_cdf)))
        _max_cdf = max(max(np.log10(ch_cdf)), max(np.log10(tm_cdf)))
    elif ch_magnitudes:
        _min_mags = min(ch_magnitudes)
        _max_mags = max(ch_magnitudes)
        _min_cdf = min(np.log10(ch_cdf))
        _max_cdf = max(np.log10(ch_cdf))
    elif tm_magnitudes:
        _min_mags = min(tm_magnitudes)
        _max_mags = max(tm_magnitudes)
        _min_cdf = min(np.log10(tm_cdf))
        _max_cdf = max(np.log10(tm_cdf))
    plt.xlim([_min_mags - 0.1, _max_mags + 0.2])
    plt.ylim([_min_cdf - 0.5, _max_cdf + 1.0])
    plt.legend(loc=1)
    fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover
    return fig


###############################################################################
def threeD_seismplot(stations=None, inventory=None,
                     location_templates=None, catalog_template=None,
                     location_children=None, catalog_children=None, **kwargs):
    """
    Plot seismicity and stations in a 3D, movable, zoomable space.

    Uses matplotlibs Axes3D package.

    :type stations: list
    :param stations:
        list of one tuple per station of (lat, long, elevation), with up
        positive. (optional)
    :type inventory: obspy.core.inventory.inventory.Inventory
    :param inventory:
        Obspy inventory class containing station metadata. (optional)
    :type location_templates: list
    :param location_templates:
        list of one tuple per event of (lat, long, depth) with down negetive.
        (optional)
    :type catalog_template: obspy.core.event.Catalog
    :param catalog_template:
        Obspy catalog class containing event metadata.(optional)
    :type location_children: list
    :param location_children:
        list of one tuple per event of (lat, long, depth) with down negetive.
        (optional)
    :type catalog_children: obspy.core.event.Catalog
    :param catalog_children:
        Obspy catalog class containing event metadata. (optional)
    {plotting_kwargs}

    :returns: :class:`matplotlib.figure.Figure`

    .. rubric:: Example:

    >>> from obspy.clients.fdsn import Client
    >>> from obspy import UTCDateTime
    >>> from eqcorrscan.utils.plotting import threeD_seismplot
    >>> client = Client('IRIS')
    >>> t1 = UTCDateTime(2012, 3, 26)
    >>> t2 = t1 + 86400
    >>> catalog = client.get_events(starttime=t1, endtime=t2, latitude=-43,
    ...                             longitude=170, maxradius=5)
    >>> inventory = client.get_stations(starttime=t1, endtime=t2, latitude=-43,
    ...                                 longitude=170, maxradius=10)
    >>> threeD_seismplot(inventory=inventory,
    ...                  catalog_template=catalog) # doctest: +SKIP

    .. plot::

        from obspy.clients.fdsn import Client
        from obspy import UTCDateTime
        from eqcorrscan.utils.plotting import threeD_seismplot
        client = Client('IRIS')
        t1 = UTCDateTime(2012, 3, 26)
        t2 = t1 + 86400
        catalog = client.get_events(starttime=t1, endtime=t2, latitude=-43,
                                    longitude=170, maxradius=5)
        inventory = client.get_stations(starttime=t1, endtime=t2, latitude=-43,
                                        longitude=170, maxradius=10)
        threeD_seismplot(inventory=inventory, catalog_template=catalog)
    .. Note::
        See :func:`eqcorrscan.utils.plotting.obspy_3d_plot` for example output.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    # making coordinates of stations
    # Will plot borehole instruments at elevation - depth if provided
    stations = stations or []
    if inventory:
        for net in inventory:
            for sta in net:
                if len(sta.channels) > 0:
                    stations.append(
                        (sta.latitude, sta.longitude,
                         sta.elevation / 1000 - sta.channels[0].depth / 1000))
                else:
                    Logger.warning('No channel information attached, '
                                   'setting elevation without depth')
                    stations.append(
                        (sta.latitude, sta.longitude, sta.elevation / 1000))
    # making coordinates of templates
    location_templates = location_templates or []
    msg = "An event of the template's catalog got ignored,\
        because it didn't have origin"
    if catalog_template:
        for event in catalog_template:
            try:
                origin = event.preferred_origin() or event.origins[0]
            except IndexError:  # No origin found
                Logger.info(msg)
                continue
            _lat = origin.latitude
            _lon = origin.longitude
            _dep = origin.depth / -1000
            location_templates.append((_lat, _lon, _dep))
    # making coordinates of children
    location_children = location_children or []
    msg = "An event of the children's catalog got ignored,\
        because it didn't have origin"
    if catalog_children:
        for event in catalog_children:
            try:
                origin = event.preferred_origin() or event.origins[0]
            except IndexError:  # No origin found
                Logger.info(msg)
                continue
            _lat = origin.latitude
            _lon = origin.longitude
            _dep = origin.depth / -1000
            location_children.append((_lat, _lon, _dep))
    if stations:
        stalats, stalongs, staelevs = zip(*stations)
    if location_children:
        evlats, evlongs, evdepths = zip(*location_children)
    if location_templates:
        temlats, temlongs, temdepths = zip(*location_templates)
    # Cope with +/-180 templates' latitudes...
    if location_templates:
        _evlongs = []
        for evlong in temlongs:
            if evlong < 0:
                evlong = float(evlong)
                evlong += 360
            _evlongs.append(evlong)
        temlongs = _evlongs
    # Cope with +/-180 childrens' latitudes...
    if location_children:
        _evlongs = []
        for evlong in evlongs:
            if evlong < 0:
                evlong = float(evlong)
                evlong += 360
            _evlongs.append(evlong)
        evlongs = _evlongs
    # Cope with +/-180 stations' latitudes...
    if stations:
        _stalongs = []
        for stalong in stalongs:
            if stalong < 0:
                stalong = float(stalong)
                stalong += 360
            _stalongs.append(stalong)
        stalongs = _stalongs
        evdepths = [-1 * depth for depth in evdepths]
    # set default parameters of scatter()
    default_parameters = {'marker': '.', 's': 4}
    for key in default_parameters.keys():
        if key not in kwargs.keys():
            kwargs[key] = default_parameters[key]
    # get parameters of _finalise_figure
    _kwargs = {}
    for key in ['title', 'show', 'save', 'savefile', 'return_fig', 'size']:
        if key in kwargs.keys():
            _kwargs[key] = kwargs[key]
            del kwargs[key]
    # 3D-plot
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.invert_yaxis()
    if location_children:
        ax.scatter(evlats, evlongs, evdepths, label='Hypocenters-children',
                   c="b", **kwargs)
    kwargs['s'] = 10
    if location_templates:
        ax.scatter(temlats, temlongs, temdepths, label='Hypocenters-templates',
                   c="r", **kwargs)
    if stations:
        ax.scatter(stalats, stalongs, staelevs, label='Stations',
                   marker="v", c="r")
    ax.set_ylabel("Longitude (deg)")
    ax.set_xlabel("Latitude (deg)")
    ax.set_zlabel("Elevation (km)")
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.legend()
    fig = _finalise_figure(fig=fig, **_kwargs)  # pragma: no cover
    return fig
