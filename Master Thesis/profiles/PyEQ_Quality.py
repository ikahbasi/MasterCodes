#!/home/imon/anaconda3/envs/SaeedCodes/bin/python3
#/home/saeed/Programs/miniconda3/bin/python

from LatLon import lat_lon as ll
from random import gammavariate, choice, seed
import os
from glob import glob
from pandas import read_csv
from numpy import abs

def get_mag():

    seed(1)
    mag = [gammavariate(2,2) for _ in range(500)]
    mag = [_/max(mag) for _ in mag]
    mag = [_*5.5 for _ in mag]

    return mag

random_mag = get_mag()

def sum_reader(root, sum_type, method='hypoell'):

## Historical & Instrumental & Regional
    # ~ CA = {"MIN_OBS":0, "MAX_GAP":360, "MAX_RMS":9.9, "MAX_ERH":999, "MAX_ERZ":999}
    # ~ CB = {"MIN_OBS":0, "MAX_GAP":360, "MAX_RMS":9.9, "MAX_ERH":999, "MAX_ERZ":999}
    # ~ CC = {"MIN_OBS":0, "MAX_GAP":360, "MAX_RMS":9.9, "MAX_ERH":999, "MAX_ERZ":999}
    # ~ OT = {"MIN_OBS":0, "MAX_GAP":360, "MAX_RMS":9.9, "MAX_ERH":999, "MAX_ERZ":999}

# Hypoellipse & NLLOC
    if method == 'hypoell':
        CA = {"MIN_OBS":6, "MAX_GAP":180, "MAX_RMS":0.3, "MAX_ERH":3.0, "MAX_ERZ":5.0}
        CB = {"MIN_OBS":5, "MAX_GAP":200, "MAX_RMS":0.4, "MAX_ERH":7.0, "MAX_ERZ":10.}
        CC = {"MIN_OBS":5, "MAX_GAP":250, "MAX_RMS":0.5, "MAX_ERH":10., "MAX_ERZ":15.}
        OT = {"MIN_OBS":4, "MAX_GAP":250, "MAX_RMS":1.0, "MAX_ERH":99., "MAX_ERZ":99.}

# ~ # HypoDD
    if method == 'hypodd':
        CA = {"MIN_OBS":1, "MAX_GAP":400, "MAX_RMS":0.1, "MAX_ERH":1.0, "MAX_ERZ":2.0}
        CB = {"MIN_OBS":1, "MAX_GAP":400, "MAX_RMS":0.2, "MAX_ERH":2.0, "MAX_ERZ":4.0}
        CC = {"MIN_OBS":1, "MAX_GAP":400, "MAX_RMS":0.3, "MAX_ERH":4.0, "MAX_ERZ":8.0}
        OT = {"MIN_OBS":1, "MAX_GAP":400, "MAX_RMS":1.0, "MAX_ERH":99., "MAX_ERZ":99.}


    out_A = os.path.join(root, "QA.dat")
    out_B = os.path.join(root, "QB.dat")
    out_C = os.path.join(root, "QC.dat")
    out_O = os.path.join(root, "OT.dat")
        
    if sum_type == "nlloc":

        inp = glob(os.path.join(root, "*hypo_71"))[0]
       
        with open(inp) as f, open(out_A, "w") as A, open(out_B, "w") as B, open(out_C, "w") as C, open(out_O, "w") as O:

            for i, l in enumerate(f):

                if i>2 and len(l)<135:

                    lat = ll.Latitude(degree=float(l[19:21]), minute=float(l[21:27])).decimal_degree
                    lon = ll.Longitude(degree=float(l[29:31]), minute=float(l[31:37])).decimal_degree
                    dep = float(l[39:44])
                    nob = float(l[52:54])
                    gap = float(l[58:61])
                    rms = float(l[64:68])
                    erh = float(l[69:73])
                    erz = float(l[74:78])
                    mag = choice(random_mag)

                    # CLASS A
                    condition_A = (nob>CA["MIN_OBS"])&(gap<CA["MAX_GAP"])&(rms<CA["MAX_RMS"])&(erh<CA["MAX_ERH"])&(erz<CA["MAX_ERZ"])
                    if condition_A: A.write("%7.3f %7.3f %5.1f %4.1f\n"%(lon, lat, dep, mag))

                    # CLASS B
                    condition_B = (nob>CB["MIN_OBS"])&(gap<CB["MAX_GAP"])&(rms<CB["MAX_RMS"])&(erh<CB["MAX_ERH"])&(erz<CB["MAX_ERZ"])
                    if condition_B: B.write("%7.3f %7.3f %5.1f %4.1f\n"%(lon, lat, dep, mag))

                    # CLASS C
                    condition_C = (nob>CC["MIN_OBS"])&(gap<CC["MAX_GAP"])&(rms<CC["MAX_RMS"])&(erh<CC["MAX_ERH"])&(erz<CC["MAX_ERZ"])
                    if condition_C: C.write("%7.3f %7.3f %5.1f %4.1f\n"%(lon, lat, dep, mag))

                    # Others
                    condition_O = (nob>OT["MIN_OBS"])&(gap<OT["MAX_GAP"])&(rms<OT["MAX_RMS"])&(erh<OT["MAX_ERH"])&(erz<OT["MAX_ERZ"])
                    if condition_O: O.write("%7.3f %7.3f %5.1f %4.1f\n"%(lon, lat, dep, mag))

    if sum_type == "xyzm":

        inp = os.path.join(root, "xyzm.dat")

        db = read_csv(inp, delim_whitespace=True)
        db = db.sort_values(by="MAG")

        db.DEPTH = abs(db.DEPTH)
        db.MAG = [choice(random_mag) if not i else i for i in db.MAG.values]
        nob = db.NO_ST.values
        gap = db.GAP.values
        rms = db.RMS.values
        erh = db.SEH.values
        erz = db.SEZ.values

        # CLASS A
        db_A = db[(nob>CA["MIN_OBS"])&(gap<CA["MAX_GAP"])&(rms<CA["MAX_RMS"])&(erh<CA["MAX_ERH"])&(erz<CA["MAX_ERZ"])]
        db_A.to_csv(out_A, sep="\t", float_format="%7.3f", columns=["LON", "LAT", "DEPTH", "MAG"], index=False, header=False)

        # CLASS B
        db_B = db[(nob>CB["MIN_OBS"])&(gap<CB["MAX_GAP"])&(rms<CB["MAX_RMS"])&(erh<CB["MAX_ERH"])&(erz<CB["MAX_ERZ"])]
        db_B.to_csv(out_B, sep="\t", float_format="%7.3f", columns=["LON", "LAT", "DEPTH", "MAG"], index=False, header=False)

        # CLASS C
        db_C = db[(nob>CC["MIN_OBS"])&(gap<CC["MAX_GAP"])&(rms<CC["MAX_RMS"])&(erh<CC["MAX_ERH"])&(erz<CC["MAX_ERZ"])]
        db_C.to_csv(out_C, sep="\t", float_format="%7.3f", columns=["LON", "LAT", "DEPTH", "MAG"], index=False, header=False)

        # Others
        db_O = db[(nob>OT["MIN_OBS"])&(gap<OT["MAX_GAP"])&(rms<OT["MAX_RMS"])&(erh<OT["MAX_ERH"])&(erz<OT["MAX_ERZ"])]
        db_O.to_csv(out_O, sep="\t", float_format="%7.3f", columns=["LON", "LAT", "DEPTH", "MAG"], index=False, header=False)

    
