import numpy as np
import sys, os

inp = "DB/focal/R3_/psmeca_A.dat"
cmd = "./Seismicity_R3.sh"

data = np.loadtxt(inp , delimiter="\t")
ind_dic = {j:i for i,j in enumerate(data[:,-1])}

if len(sys.argv) == 3:
    
    ref = int(sys.argv[1])
    tar = int(sys.argv[2])

    x_ref = data[ind_dic[ref]][7]
    y_ref = data[ind_dic[ref]][8]

    x_tar = data[ind_dic[tar]][7]
    y_tar = data[ind_dic[tar]][8]

    data[ind_dic[tar]][7] = x_ref
    data[ind_dic[tar]][8] = y_ref

    data[ind_dic[ref]][7] = x_tar
    data[ind_dic[ref]][8] = y_tar

if len(sys.argv) == 4:

    ev_id = int(sys.argv[1])
    n_lon = float((sys.argv[2]))
    n_lat = float((sys.argv[3]))

    data[ind_dic[ev_id]][7] = n_lon
    data[ind_dic[ev_id]][8] = n_lat

    
np.savetxt("test.dat", data, fmt="%6.3f\t%6.3f\t%4.1f\t%3d\t%2d\t%4d\t%3.1f\t%6.3f\t%6.3f\t%3d")

os.rename("test.dat", inp)
os.system(cmd)
