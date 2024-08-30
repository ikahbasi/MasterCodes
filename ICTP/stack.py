from obspy import read, Stream
import numpy as np
import matplotlib.pyplot as plt
import glob

Flag_Save_Figure=1

#Filtering
freqmin=3.0
freqmax=6.0
#Taper
max_percentage = 0.9

files = glob.glob('events/*.mseed')
x=0
y=10
print(len(files))
while y <= len(files):
    st=Stream()
    st_list = files[x:y]
    for file in st_list:
        st += read(file)
    print(len(st))
    st2 = st.select(station="JAVS").select(channel="HHZ").filter('bandpass', freqmin=freqmin, freqmax=freqmax, zerophase=True).taper(max_percentage=max_percentage, type="hann")
    npanels=10
    print(len(st2))
    #x=x+npanels
    x=x+10
    #y=y+npanels
    y=y+10
    # you can loop on fig only if you need to run multiple figures. If not
    fig, axarray = plt.subplots(npanels, sharex=True)
    count = 0
    for tt in st2:
        count=count+1

        # you have to start with common reference times
        tad=np.arange(0, (tt.stats.npts / tt.stats.sampling_rate), tt.stats.delta)
        tad = tad[:-1]

        # normalize
        ttn = tt.normalize()
        axarray[count-1].plot(tad, ttn, 'r', lw=1.5)
        axarray[count-1].text(4.0,0.7,tt.stats.station+"."+tt.stats.channel+"-"+str(tt.stats.starttime), fontsize=9)
    if Flag_Save_Figure==0:
        plt.show()
    if Flag_Save_Figure==1:
        fig = plt.gcf()
        fig.set_size_inches(6.0, 14.316)

        outfile="plots/postojna_template_stack" +str(tt.stats.starttime)+ ".png"
        fig.savefig(outfile,dpi=300)
        plt.close()
