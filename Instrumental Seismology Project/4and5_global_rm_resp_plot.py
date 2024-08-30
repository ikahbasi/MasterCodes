#origin time of earthquake
time_event = '2017-11-12 18:18:17.8'
lat_event = 34.877
lon_event = 45.841
depth_event = 18
################### import library ###################
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import matplotlib.pyplot as plt
import os
#from matplotlib.pyplot import figure
save = True
show = False
size = 30
############# def #############
def plot_rm_resp(st):
    time_window = st[0].times().tolist()
    name =  str(st[0].id)
    pre_filt = (0.005, 0.006, 30.0, 35.0)
    
    ##### dispelacement
    st_copy = st.copy()
    st_copy.remove_response(output='DISP', pre_filt=pre_filt)
    tr_rm_resp_disp = st_copy[0].data.tolist()
    ##### velocity
    st_copy = st.copy()
    st_copy.remove_response(output='VEL', pre_filt=pre_filt)
    tr_rm_resp_vel = st_copy[0].data.tolist()
    #### acceleration
    st_copy = st.copy()
    st_copy.remove_response(output='ACC', pre_filt=pre_filt)
    tr_rm_resp_acc = st_copy[0].data.tolist()
    
    ############## subplot of origin_DISP_VEL_ACC
    #### make subplot
    f = plt.figure(figsize=(25,20),dpi=100)
    plt.subplots_adjust(hspace=0.6)
    f.suptitle(name,fontsize=40,fontweight='black')
    #### ORIGIN
    f.add_subplot(411).plot(time_window, st[0].data.tolist(), color='black',lw=1.3)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('count',fontsize=size,fontweight='black')
    plt.title('origin trace', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    #### DISP
    f.add_subplot(412).plot(time_window, tr_rm_resp_disp, color='green',lw=1.3)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('displacement',fontsize=size,fontweight='black')
    plt.title('displacement', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    #### VEL
    f.add_subplot(413).plot(time_window, tr_rm_resp_vel, color='blue',lw=1.3)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('velocity',fontsize=size,fontweight='black')
    plt.title('velocity', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    #### ACC
    f.add_subplot(414).plot(time_window, tr_rm_resp_acc, color='red',lw=0.9)
    plt.xlabel('time',fontsize=size,fontweight='black')
    plt.ylabel('acceleration',fontsize=size,fontweight='black')
    plt.title('acceleration', fontweight='black',fontsize=size)
    plt.tick_params(labelsize=size)
    
    ###
    if show:
        f.show()
    if save:
        path = './output/rmresp/'
        if not os.path.isdir(path): os.makedirs(path)
        f.savefig(path+name+'_subplot_'+'.png') # save image(optional)
    
    ############# plot all trace in one
    plt.figure(figsize=(30,10),dpi=100)
    plt.plot(time_window,tr_rm_resp_acc,'r',lw=0.6,label= 'ACC')
    plt.plot(time_window,tr_rm_resp_vel,'b',lw=1, label ='VELOCITY')
    plt.plot(time_window,tr_rm_resp_disp,'g',lw=1.2,label='DISP')
    plt.xlabel('time',fontsize=size+15,fontweight='black')
    plt.ylabel('amplitude',fontsize=size+15,fontweight='black')
    plt.suptitle(st[0].id,fontsize=40,fontweight='black')
    plt.tick_params(labelsize=size)
    plt.legend(fontsize=30)
    ###
    if show:
        plt.show()
    if save:
        plt.savefig(path+st[0].id+'_all.in.one_'+'.png') # save image(optional)
    
############# set some parameter #############
client = Client("IRIS")
origine_time = UTCDateTime(time_event)

def get_waveform(name_station):
    print name_station,' in progeres'
    ############# get data from station #############
    end_of_waveform = origine_time + 2500
    try:
        st = client.get_waveforms("IU", name_station , "00", "LHZ", 
                                  origine_time-360,
                                  end_of_waveform,
                                  attach_response=True)
    except:
        print 'NOTE: waveform not exist'
        print '-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-','\n'
    ############# station parameter #############
    print name_station,' recieved'
    return st

stream = get_waveform('ANTO')
plot_rm_resp(stream)
