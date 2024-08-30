from pandas import read_csv
import numpy as np
import sys, os

inp = sys.argv[1]

x1 = float(sys.argv[2])
x2 = float(sys.argv[3])
y1 = float(sys.argv[4])
y2 = float(sys.argv[5])

db=read_csv(inp, names=["STA", "LON", "LAT", "Evel", "Nvel", "SigVe", "SigVn", "AZ", "LEN"], delimiter="\t", index_col=False)

new_db = db[(db.LON>=x1)&(db.LON<=x2)&(db.LAT>=y1)&(db.LAT<=y2)]

x_m = new_db.LON.mean()
y_m = new_db.LAT.mean()
a_m = np.rad2deg(np.arctan2(new_db.Nvel.mean(), new_db.Evel.mean()))
d_m = np.sqrt(new_db.Nvel.mean()**2 + new_db.Evel.mean()**2)*.1

print x_m, y_m, a_m, d_m

    
