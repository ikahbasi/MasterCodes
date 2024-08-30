import math

with open("GPS_vel_Farmarz_2016_281_stns.txt") as f, open("GPS.dat", "w") as g:

    next(f); next(f); next(f)

    for line in f:

        l = line.split()
        
        sta = l[0]
        lon = float(l[1])
        lat = float(l[2])
        
        if 50<lon<54 and 34<lat<37:
            
            Evel = float(l[3])
            Nvel = float(l[4])
            SVE = float(l[5])
            SVN = float(l[6])
            V_theta = math.degrees(math.atan2(Nvel, Evel))
            V_len = math.sqrt(Nvel**2 + Evel**2)
            g.write("%5s %9.4f %9.4f %6.2f %6.2f %5.2f %5.2f %6.1f %5.1f\n"%(sta, lon, lat, Evel, Nvel, SVE, SVN, V_theta, V_len))
