


def _finalise_figure(fig, **kwargs):  # pragma: no cover
    """
    Internal function to wrap up a figure.
    {plotting_kwargs}
    """
    import matplotlib.pyplot as plt

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
    if show:
        plt.show(block=True)
    if return_fig:
        return fig
    fig.clf()
    plt.close(fig)
    return None


def mapplot(events, bgcolor='#909090', mode='3bode', cpalette='jet_r',
            s=1, lw=1, marker=',', **kwargs):
    """
    Plot seismicity in a 2D map with two cross section along latitude and longitude.

    :type nodes: list
    :param template: list of one tuple per event of (lat, long, depth) with down positive.
    :type bgcolor: string
    :param bgcolor: all name or RGB code that acceptable in matplotlib.
    :type mode: string
    :param mode: make color pallete according to thrid part of area or occouring sequence. 
    :type cpalette: string
    :param cpalette: color palette for drawing events. acceptable with matplotlib.
    :type s: float
    :param s:
    :type lw: float
    :param lw:
    :type marker: string
    :param marker:
    {plotting_kwargs}

    :returns: :class:`matplotlib.figure.Figure`
    .. image:: ../../plots/xcorr_plot.png
    """
    import matplotlib.pyplot as plt 
    from matplotlib import gridspec
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from obspy.core.event.catalog import Catalog
    # set parameter
    if isinstance(events, list):
        lat, lon, dep, time = zip(*events)
    elif isinstance(events, Catalog):
        lat = lon = dep = time = []
        for ev in events:
            origin = ev.origins[0]
            lat.append(origin.latitude)
            lon.append(origin.longitude)
            dep.append(origin.depth)
            time.append(origin.time)
    dt = [t-time[0] for t in time]
    if mode=='3bode':
        c0, c1, c2 = dep, lon, lat
        label0 , label1, label2 = 'Depth' , 'Longitue', 'Latitude'
    elif mode=='time':
        c0 = c1 = c2 = dt #range(len(dep))
        label = 'second from first event'
    elif mode=='sequence':
        c0 = c1 = c2 = range(len(dep))
        label = 'sequence of occuring'
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[3,1],
                           wspace=0.01, hspace=0.01)     
    # map view
    ax0 = plt.subplot(gs[0])
    ax0.set_facecolor(bgcolor)  
    ax0.set_ylabel('Latitude')
    ax0.set_xticks([])
    map0 = ax0.scatter(lon, lat, marker=marker, c=c0, cmap=cpalette,
                       lw=lw, s=s)
    # cross section paralel to latitude (lat ,depth)
    ax1 = fig.add_subplot(gs[1])
    ax1.set_facecolor(bgcolor)
    ax1.set_yticks([])
    ax1.set_xlabel('Depth')
    ax1.invert_xaxis()
    map1 = ax1.scatter(dep, lat, marker=marker, c=c1, cmap=cpalette,
                       lw=lw, s=s)
    # cross section paralel to longitude (lon ,depth)
    ax2 = plt.subplot(gs[2])
    ax2.set_facecolor(bgcolor)
    ax2.set_ylabel('Depth')
    ax2.set_xlabel('Longitude')
    map2 = ax2.scatter(lon, dep, marker=marker, c=c2, cmap=cpalette,
                       lw=lw, s=s)
    # location of color bar
    if mode=='3bode':
        #location of colorbar
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
    elif mode=='time' or mode=='sequence':
        divider1 = make_axes_locatable(ax1)
        cax1 = divider1.append_axes("right", size="4%", pad="2%")
        cbar1 = fig.colorbar(map1, ax=ax1, cax=cax1, orientation="vertical")
        cbar1.set_label(label)
    fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover
    return fig

from obspy import UTCDateTime as utc
import numpy as np
data = np.genfromtxt("./tmp.txt")
lon = data[:,0]
lat = data[:,1]
dep = data[:,2] * -1

sec = data[:,-1].astype(str)
mint = data[:,-2].astype(int).astype(str)
hour = data[:,-3].astype(int).astype(str)
day = data[:,-4].astype(int).astype(str)
month = data[:,-5].astype(int).astype(str)
year = data[:,-6].astype(int).astype(str)
Date = []
for ii in range(len(year)):
    date = '{}-{}-{}T{}:{}:{}'.format(year[ii], month[ii], day[ii], hour[ii], mint[ii], sec[ii])
    Date.append(utc(date))
#
#dt = []
#for ii in range(len(Date)):
#    dt.append(Date[ii] - Date[0])

nodes=[]
for Lat, Lon, Dep, t in zip(lat, lon, dep, Date):
    nodes.append((Lat, Lon, Dep, t))
    
mapplot(nodes, mode='sequence', show=True, save='./kdfjlskdjfa.png')
