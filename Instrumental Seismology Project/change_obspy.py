import matplotlib.pyplot as plt
import numpy as np
from obspy.signal.trigger import trigger_onset
import os

def my_plot_trigger(trace, cft, thr_on, thr_off,jj, show=False):
    # jj is just a number name of image that want to save
    """
    Plot characteristic function of trigger along with waveform data and
    trigger On/Off from given thresholds.

    :type trace: :class:`~obspy.core.trace.Trace`
    :param trace: waveform data
    :type cft: :class:`numpy.ndarray`
    :param cft: characteristic function as returned by a trigger in
        :mod:`obspy.signal.trigger`
    :type thr_on: float
    :param thr_on: threshold for switching trigger on
    :type thr_off: float
    :param thr_off: threshold for switching trigger off
    :type show: bool
    :param show: Do not call `plt.show()` at end of routine. That way,
        further modifications can be done to the figure before showing it.
    """

    df = trace.stats.sampling_rate
    npts = trace.stats.npts
    t = np.arange(npts, dtype=np.float32) / df
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(t, trace.data, 'k')
    ax2 = fig.add_subplot(212, sharex=ax1)
    ax2.plot(t, cft, 'k')
    on_off = np.array(trigger_onset(cft, thr_on, thr_off))
    i, j = ax1.get_ylim()
    try:
        ax1.vlines(on_off[:, 0] / df, i, j, color='r', lw=2,
                   label="Trigger On")
        ax1.vlines(on_off[:, 1] / df, i, j, color='b', lw=2,
                   label="Trigger Off")
        ax1.legend()
    except IndexError:
        pass
    ax2.axhline(thr_on, color='red', lw=1, ls='--')
    ax2.axhline(thr_off, color='blue', lw=1, ls='--')
    ax2.set_xlabel("Time after %s [s]" % trace.stats.starttime.isoformat())
    fig.suptitle(trace.id)
    fig.canvas.draw()
    if show:
        plt.show()
    elif trace.stats.network == 'IU':
        path = './output/global_triger/'
        if not os.path.isdir(path): os.makedirs(path)
        fig.savefig(path+str(jj+1)+'_'+str(trace.id)+'.png')
    elif trace.stats.network == 'IR':
        path = './output/irsc_triger/'
        if not os.path.isdir(path): os.makedirs(path)
        fig.savefig(path+str(jj+1)+'_'+str(trace.id)+'.png')
    elif trace.stats.network == 'BI':
        path = './output/iiees_triger/'
        if not os.path.isdir(path): os.makedirs(path)
        fig.savefig(path+str(jj+1)+'_'+str(trace.id)+'.png')
