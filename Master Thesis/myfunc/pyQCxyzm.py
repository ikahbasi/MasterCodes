import numpy as np
import matplotlib.pyplot as plt
import glob
from os.path import join
import os
class XYZM:
    def __init__(self):
        self.LON   = []
        self.LAT   = []
        self.DEPTH = 0
        self.MAG   = 0
        self.PHUSD = 0
        self.NO_ST = 0
        self.MIND  = 0
        self.GAP   = 0
        self.RMS   = 0
        self.SEH   = 0
        self.SEZ   = 0
        self.YYYY  = 0
        self.MM    = 0
        self.DD    = 0
        self.HH    = 0
        self.MN    = 0
        self.SEC   = 0
    def read(self, file_name):
        data_file = np.genfromtxt(file_name, skip_header=1)
        self.LON   = data_file[:, 0]
        self.LAT   = data_file[:, 1]
        self.DEPTH = data_file[:, 2]
        self.MAG   = data_file[:, 3]
        self.PHUSD = data_file[:, 4]
        self.NO_ST = data_file[:, 5]
        self.MIND  = data_file[:, 6]
        self.GAP   = data_file[:, 7]
        self.RMS   = data_file[:, 8]
        self.SEH   = data_file[:, 9]
        self.SEZ   = data_file[:, 10]
        self.YYYY  = data_file[:, 11]
        self.MM    = data_file[:, 12]
        self.DD    = data_file[:, 13]
        self.HH    = data_file[:, 14]
        self.MN    = data_file[:, 15]
        self.SEC   = data_file[:, 16]


def autolabel(rects, fontsize=10):
    """Attach a text label above each bar in *rects*, displaying its height."""
    rects = zip(rects[0], rects[1])
    rects = list(rects)
    ax = plt.gca()
    width = rects[1][1] - rects[0][1]
    for rect in rects:
        height = rect[0]
        ax.annotate('{}'.format(int(height)),
                    xy=(rect[1] + width/2, height),
                    xytext=(0, 0.5),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontsize)
                    

def _finalise_figure(fig, **kwargs):  # pragma: no cover
    """
    Internal function to wrap up a figure.
    {plotting_kwargs}
    """
    ax = plt.gca()
    ax.xaxis.set_tick_params(labelsize=15)
    ax.yaxis.set_tick_params(labelsize=15)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    show = kwargs.get("show", True)
    save = kwargs.get("save", False)
    savefile = kwargs.get("savefile", "EQcorrscan_figure.png")
    title = kwargs.get("title")
    xlim = kwargs.get("xlim")
    ylim = kwargs.get("ylim")
    if title:
        plt.title(title, fontsize=25)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(top=ylim[1])
    if save:
        path = os.path.dirname(savefile)
        if path:
            os.makedirs(path, exist_ok=True)
    return_fig = kwargs.get("return_figure", False)
    size = kwargs.get("size", (10.5,10))#(10.5, 7.5))
    fig.set_size_inches(size)
    if save:
        fig.savefig(savefile, bbox_inches="tight", dpi=130)
        print("Saved figure to {0}".format(savefile))
    if show:
        plt.show(block=True)
    if return_fig:
        return fig
    fig.clf()
    plt.close(fig)
    return None


class qc_xyzm:
    def __init__(self):
        self.RMS   = None
        self.SEH   = None
        self.SEZ   = None
        self.GAP   = None
        self.MIND  = None
        self.NO_ST = None
        self.PHUSD = None
    def read(self, path_file):
        xyzm = XYZM()
        xyzm.read(path_file)
        #
        self.RMS = xyzm.RMS
        self.SEH = xyzm.SEH
        self.SEZ = xyzm.SEZ
        self.GAP = xyzm.GAP
        self.MIND = xyzm.MIND
        self.NO_ST = xyzm.NO_ST
        self.PHUSD = xyzm.PHUSD
    def rms(self, **kwargs):
        RMS = self.RMS
        bins = np.arange(0, 1.1, 0.1)
        fig = plt.figure()
        rects = plt.hist(RMS, bins, align='mid', edgecolor='black', linewidth=1.2)
        autolabel(rects)
        plt.ylabel('Abundance [count]', fontsize=17)
        plt.xlabel('RMS [s]', fontsize=17)
        fig = _finalise_figure(fig=fig, **kwargs)

    def seh(self, **kwargs):
        SEH = self.SEH
        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11]
        ##########################################################################################
        last_tick = max(SEH)                                                   # change last label
        if last_tick > bins[-1]:                                               # change last label
            tmp = bins.copy()                                                  # change last label
            tmp[-1] = str(int(last_tick))                                      # change last label
            last_tick = tmp                                                    # change last label
            SEH[SEH > bins[-1]] = bins[-1] - 0.5                               # change last label
        else:                                                                  # change last label
            last_tick = bins                                                   # change last label
        ##########################################################################################
        fig = plt.figure()
        rects = plt.hist(SEH, bins, align='mid', edgecolor='black', linewidth=1.2)
        autolabel(rects)
        plt.ylabel('Abundance [count]', fontsize=17)
        plt.xlabel('Horizontal error [km]', fontsize=17)
        plt.xticks(bins, last_tick)                                            # change last label
        fig = _finalise_figure(fig=fig, **kwargs)
# SEZ
    def sez(self, **kwargs):
        SEZ = self.SEZ
        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11]
        ##########################################################################################
        last_tick = max(SEZ)                                                   # change last label
        if last_tick > bins[-1]:                                               # change last label
            tmp = bins.copy()                                                  # change last label
            tmp[-1] = str(int(last_tick))                                      # change last label
            last_tick = tmp                                                    # change last label
            SEZ[SEZ > bins[-1]] = bins[-1] - 0.05                              # change last label
        else:                                                                  # change last label
            last_tick = bins                                                   # change last label
        ##########################################################################################
        fig = plt.figure()
        rects = plt.hist(SEZ, bins, align='mid', edgecolor='black', linewidth=1.2)
        autolabel(rects)
        plt.ylabel('Abundance [count]', fontsize=17)
        plt.xlabel('Vertical error [km]', fontsize=17)
        plt.xticks(bins, last_tick)                                            # change last label
        fig = _finalise_figure(fig=fig, **kwargs)
# GAP
    def gap(self, binsize=30, **kwargs):
        GAP = self.GAP
        bins = np.arange(0, 361, binsize)
        fig = plt.figure()
        rects = plt.hist(GAP, bins, align='mid', edgecolor='black', linewidth=1.2)
        autolabel(rects)
        plt.ylabel('Abundance [count]', fontsize=17)
        plt.xlabel('Azimuthal gap [degree]', fontsize=17)
        fig = _finalise_figure(fig=fig, **kwargs)
# NO_ST
    def num_st(self, all_stations=13, **kwargs):
        NO_ST = self.NO_ST
        bins = np.arange(0, all_stations+1)
        fig = plt.figure()
        rects = plt.hist(NO_ST, bins, align='left', width=0.8, edgecolor='black', linewidth=1.2)
        rects = (rects[0], rects[1] - 0.6)
        autolabel(rects)
        plt.ylabel('Abundance [count]', fontsize=17)
        plt.xlabel('Number of stations [count]', fontsize=17)
        plt.xticks(bins, bins)  
        fig = _finalise_figure(fig=fig, **kwargs)
# PHUSD
    def num_ph(self, max_phase=20, **kwargs):
        PHUSD = self.PHUSD
        bins = np.arange(0, max_phase+1)
        ##########################################################################################
        last_tick = max(PHUSD)                                                   # change last label
        if last_tick > bins[-1]:                                               # change last label
            tmp = bins.copy()                                                  # change last label
            tmp[-1] = str(int(last_tick))                                      # change last label
            last_tick = tmp                                                    # change last label
            PHUSD[PHUSD > bins[-1]] = bins[-1] - 0.5                          # change last label
        else:                                                                  # change last label
            last_tick = bins                                                   # change last label
        ##########################################################################################
        fig = plt.figure()
        rects = plt.hist(PHUSD, bins, align='left', width=0.8, edgecolor='black', linewidth=1.2)
        rects = (rects[0], rects[1] - 0.6)
        autolabel(rects)
        plt.ylabel('Abundance [count]', fontsize=17)
        plt.xlabel('Number of phases [count]', fontsize=17)
        plt.xticks(np.arange(0, max_phase, 2), np.arange(0, max_phase, 2))     # change last label
        fig = _finalise_figure(fig=fig, **kwargs)
        #

'''
if __name__ == '__main__':
    qc = qc_xyzm()
    qc.read('xyzm.dat')
    qc.rms(save=True,    savefile='rms.png',    show=False, title='RMS')
    qc.sez(save=True,    savefile='sez.png',    show=False, title='ErrZ')
    qc.seh(save=True,    savefile='seh.png',    show=False, title='ErrH')
    qc.gap(save=True,    savefile='gap.png',    show=False, title='GAP')
    qc.num_st(save=True, savefile='num_st.png', show=False, title='Num st')
    qc.num_ph(save=True, savefile='num_ph.png', show=False, title='Num ph')
'''
import glob
runs = glob.glob('run*')
for run in runs:
    run_name = run[3:]
    qc = qc_xyzm()
    qc.read(run+'/location/xyzm.dat')
    outpath = f'qcxyzm/{run_name}'
    qc.rms(save=True,    savefile=f'qcxyzm/rms/{run_name}_rms.png',       show=False, title=run_name+' HZ', ylim=[0, 50])
    qc.sez(save=True,    savefile=f'qcxyzm/sez/{run_name}_sez.png',       show=False, title=run_name+' HZ', ylim=[0, 40])
    qc.seh(save=True,    savefile=f'qcxyzm/seh/{run_name}_seh.png',       show=False, title=run_name+' HZ', ylim=[0, 40])
    qc.gap(save=True,    savefile=f'qcxyzm/gap/{run_name}_gap.png',       show=False, title=run_name+' HZ', ylim=[0, 35])
    qc.num_st(save=True, savefile=f'qcxyzm/num_st/{run_name}_num_st.png', show=False, title=run_name+' HZ', ylim=[0, 30])
    qc.num_ph(save=True, savefile=f'qcxyzm/num_ph/{run_name}_num_ph.png', show=False, title=run_name+' HZ', ylim=[0, 22])
