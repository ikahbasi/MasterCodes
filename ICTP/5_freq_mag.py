from eqcorrscan.utils.plotting import freq_mag
from eqcorrscan.utils.mag_calc import calc_max_curv

magfile=open("event_magnitudes_ml", "r")

magnitudes=[]

for line in magfile:
    element = line.split(" ")
    dt = element[0]
    mag_v = float(element[1].rstrip())
    magnitudes.append(mag_v)

completeness = calc_max_curv(magnitudes, plotvar=False)
print("Completeness of catalogue is: ",completeness)

max_mag=max(magnitudes)
print("Maximum magnitude is: ",max_mag)

freq_mag(magnitudes=magnitudes, completeness=completeness, max_mag=max_mag, binsize=0.2, save=False, savefile=None)
