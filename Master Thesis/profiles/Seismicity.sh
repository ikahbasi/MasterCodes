#!/bin/bash
#===================================================
#
#
#===================================================

#
#__________CLEAN SCREEN, REMOVE initial PREVIOUS COMMANDS
#

clear

#->>> LOADING FILES
root="DB/event/nordic-reference"




# Theme1
#d1_clr="#f45905"
#d2_clr="#ffc785"
#d3_clr="#72d6c9"
#d4_clr="#dedef0"

# Theme2
d1_clr="darkred"
d2_clr="red"
d3_clr="pink"
d4_clr="gray"

profiles="DB/profiles/profiles.dat"
regions="DB/regions/regions.dat"
regnames="DB/regions/names.dat"

#Baladeh_st="DB/station/Baldeh.dat"
#IIEES_st="DB/station/IIEES.dat"
#TDMT_st="DB/station/TDMT.dat"
#CAlborz_st="DB/station/CAlborz.dat"
#IRSC_st="DB/station/IRSC.dat"
#Garmsar_st="DB/station/Garmsar.dat"
#Mosha_st="DB/station/Mosha.dat"
#Bushehr_st="DB/station/Bushehr.dat"
Ilam_st="DB/station/Ilam.dat"
#-<<<

#->>> CREATE DIRECTORY FOR SAVING FIGS

OUTNAME=`echo $root | awk '{split($0, a, "/"); print a[3]}'`
mkdir -p FIG/$OUTNAME
OUTPUT=FIG/$OUTNAME/Sismicity.ps

#-<<<

#->>> FETCH REQUIRED FILES

iran_grd=DB/grd/Ilam.grd
gradient_grd=gradient.grd
colormap=colors.cpt

NOR=$GMTHOME/fault/IranFaults/NOR
SSL=$GMTHOME/fault/IranFaults/SSL
SSR=$GMTHOME/fault/IranFaults/SSR
THL=$GMTHOME/fault/IranFaults/THL
THR=$GMTHOME/fault/IranFaults/THR
MIN=$GMTHOME/fault/IranFaults/minor.dat
TehB=$GMTHOME/fault/Tehran/Tehran.dat
FLN=$GMTHOME/fault/FN.dat

#-<<<

#->>> SET GMT GLOBALS/PARAMETERS

LON_min=47.0600
LON_max=48.1800
LAT_min=32.1800
LAT_max=33.1200

R="-R$LON_min/$LON_max/$LAT_min/$LAT_max"
J="-JM10c"
B="-Ba.3f.1/a.2f.1WSne"
x=$(echo $LON_min + 0.15 | bc)
y=$(echo $LAT_min + 0.05 | bc)
L="-Lf$x/$y/32/20k+lKm"
POS="-X2 -Y10"
FRAME="--MAP_FRAME_WIDTH=4p"
FONT="--FONT_ANNOT_PRIMARY=8p,Times-Bold,black"
LABLE="--FONT=6p,Times-Bold,black"

#-<<<

#->>> GMT BASIC-MAP

#grdraster	8	$R		-I1m		-G$iran_grd
gmt psbasemap	$R		$J		$B	$POS	-P	$FRAME	$FONT	-K	>	$OUTPUT
gmt grdgradient	$iran_grd	-A40		-G$gradient_grd			-Nt.5
#gmt grd2cpt 	$gradient_grd  	-L0/4000	-T-2500/5000/100	-Z	-Ctopo	>	$colormap
gmt grd2cpt 	$gradient_grd  	-L1/4000	-T-2500/5000/100	-Z	-Ctopo	>	$colormap
gmt grdimage 	$R		$J		$iran_grd	-C$colormap	-I$gradient_grd		-K	-O	>>	$OUTPUT
gmt pscoast		$R	$J	-S90/180/255	-Df	-C90/180/225	$L	-W.5p,midnightblue	-Na/.5p,black,-	$LABLE	-K	-O	>>	$OUTPUT

#-<<<

#->>> ADD FEATURE NAMES

#echo "50.85 28.98 Bushehr"	| gmt pstext -R -J -F+f8p,27,black=.3p,black	-N	-O	-K	>>	$OUTPUT
#echo "50.85 28.965"			| gmt psxy   -R -J -Ss0.2 -Gblack -L -W 		-O 	-K	>>	$OUTPUT
#echo "50.88 28.85 BNPP"		| gmt pstext -R -J -F+f8p,27,black=.3p,black	-N	-O	-K	>>	$OUTPUT
#echo "50.88 28.83"			| gmt psxy   -R -J -Si.5 -Gyellow -W3,red	-L -W 		-O 	-K	>>	$OUTPUT

#-<<<

#->>> ADD SEISMICITY

python << EOF
import os
from PyEQ_Quality import sum_reader

root="$root"
sum_reader(root=root, sum_type="xyzm")

d1=(os.path.join(root, "QA.dat"), "$d1_clr")
d2=(os.path.join(root, "QB.dat"), "$d2_clr")
d3=(os.path.join(root, "QC.dat"), "$d3_clr")
d4=(os.path.join(root, "OT.dat"), "$d4_clr")

for i in [d4, d3, d2, d1]:

    cmd = "awk '{print \$1,\$2,\$4*0.125}' "+i[0]+" | gmt psxy -R -J -Sc.1 -G"+i[1]+" -W.5,black -K -O >> $OUTPUT"
    os.system(cmd)

EOF

#-<<<

#->>> ADD FAULTS


# Normal Faults
#for i in `ls $NOR`
#do
#gmt psxy	$NOR/$i	-R	-J	-W1.2	-K	-O	>>	$OUTPUT
#done

# Strike-Slip Faults

#for i in `ls $SSL`
#do
#gmt psxy	$SSL/$i	-R	-J	-Sf2c/.2c+l+s+o0.6+p0.6	-W1.2	-K	-O  	>>	$OUTPUT
#done

#for i in `ls $SSR`
#do
#gmt psxy	$SSR/$i	-R	-J	-Sf2c/.3c+r+s+o.5+p0.5	-W1.2	-K	-O  	>>	$OUTPUT
#done

# Thrust Faults

#for i in `ls $THL`
#do
#gmt psxy	$THL/$i	-R	-J	-Sf.3c/.10c+l+t+o.25+p0.5	-Gblack	-W1.2	-K	-O  	>>	$OUTPUT
#done

#for i in `ls $THR`
#do
#gmt psxy	$THR/$i	-R	-J	-Sf.3c/.10c+r+t+o.25+p0.5	-Gblack	-W1.2	-K	-O  	>>	$OUTPUT
#done

#-<<<


#->>> ADD HORIZONTAL CROSS

c=1
while read line
do
track=track_$c
stlon=`echo $line | awk '{print $1}'`
stlat=`echo $line | awk '{print $2}'`
azimut=`echo $line | awk '{print $3}'`
semilen=`echo $line | awk '{print $4}'`
xy_res=0.5

gmt project -C$stlon/$stlat -A$azimut -L0/$semilen -G$xy_res -Q > $track
awk 'NR==1; END{print}' $track |	gmt psxy	-R	-J	-W2	-K	-O	>>	$OUTPUT
awk -v n=$c 'NR==1 {print$1, $2, n}' $track | gmt pstext	-R	-J	-F+f9p,Times-Bold,black+jLM	-Gwhite	-W1,black	-O	-K	>>	$OUTPUT
let c=c+1

done < $profiles

#-<<< ADD HORIZONTAL CROSS

#->>> ADD REGIONS

#~ gmt psxy	$regions	-R	-J	-W1.5,black			-K	-O	>>	$OUTPUT
#~ gmt pstext 	$regnames	-R 	-J	-F+f+a+j	-Gwhite		-K	-O	>>	$OUTPUT

#-<<<_ADD REGIONS

#->>> ADD STATIONS

#awk '{print $5,$4}' $Ilam_st		| gmt psxy	-R	-J	-St.50	-Gwhite	-W3,darkred	-K	-O	>>	$OUTPUT
#awk '{print $5,$4}' $Ilam_st		| gmt psxy	-R	-J	-St.50	-Gwhite	-W3,green	-K	-O	>>	$OUTPUT
#awk '{print $5,$4-.018,$2}' $Ilam_st	| gmt pstext	-R	-J	-F+f8p,27,black=.3p,black	-N	-O	-K	>>	$OUTPUT

#-<<< ADD STATIONS

#->>> ADD FAULT NAME

#gmt pstext $FLN	-R -J	-F+f+a+j	-Gwhite	-O	-K	>>	$OUTPUT

#-<<<


#->>> ADD 50km CIRCLE

#~ echo "50.88 28.85" | gmt psxy -R -J -Sc16  -W2,blue -K -O >> $OUTPUT

#-<<<

#->>> ADD LEGEND

##_STATIONS
#echo "54.20 35.70"	|	gmt psxy	-R	-J	-St.25	-Gwhite		-W2,darkred	-N	-K	-O	>> $OUTPUT
#echo "54.20 35.60"	|	gmt psxy	-R	-J	-St.25	-Gwhite		-W2,darkblue	-N	-K	-O	>> $OUTPUT
#echo "54.20 35.50"	|	gmt psxy	-R	-J	-St.25	-Gwhite		-W2,darkgreen	-N	-K	-O	>> $OUTPUT
#echo "54.20 35.40"	|	gmt psxy	-R	-J	-St.25	-Gwhite		-W2,gray18	-N	-K	-O	>> $OUTPUT
#echo "54.20 35.30"	|	gmt psxy	-R	-J	-St.25	-Gwhite		-W2,red	-N	-K	-O	>> $OUTPUT
#echo "54.20 35.20"	|	gmt psxy	-R	-J	-St.25	-Gwhite		-W2,yellow	-N	-K	-O	>> $OUTPUT
#echo "54.20 35.10"	|	gmt psxy	-R	-J	-St.25	-Gwhite		-W2,aquamarine	-N	-K	-O	>> $OUTPUT

#echo "54.15 35.85 Stations"	| gmt pstext -R -J -F+f12p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
#echo "54.30 35.70 Baladeh"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
#echo "54.30 35.60 CAlborz"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
#echo "54.30 35.50 Garmsar"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
#echo "54.30 35.40 Mosha"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
#echo "54.30 35.30 IRSC"		| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
#echo "54.30 35.20 IIEES"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
#echo "54.30 35.10 TDMT"		| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
##_STATIONS

#~ #_QUALITIES
refx=47.95
refy=33.08
#
x=$(echo $refx + 0.03 | bc)
y=$(echo $refy - 0.04 | bc)
echo "$x $y"	|	gmt psxy	-R	-J	-Ss.5	-G$d1_clr	-W.5,black	-N	-K	-O	>> $OUTPUT
#
y=$(echo $y - 0.03 | bc)
echo "$x $y"	|	gmt psxy	-R	-J	-Ss.5	-G$d2_clr	-W.5,black	-N	-K	-O	>> $OUTPUT
#
y=$(echo $y - 0.03 | bc)
echo "$x $y"	|	gmt psxy	-R	-J	-Ss.5	-G$d3_clr	-W.5,black	-N	-K	-O	>> $OUTPUT
#
y=$(echo $y - 0.03 | bc)
echo "$x $y"	|	gmt psxy	-R	-J	-Ss.5	-G$d4_clr	-W.5,black	-N	-K	-O	>> $OUTPUT


echo "$refx $refy Quality"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT
x=$(echo $refx + 0.07 | bc)
y=$(echo $refy - 0.04 | bc)
echo "$x $y A"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM		-N	-O	-K	>>	$OUTPUT
#
y=$(echo $y - 0.03 | bc)
echo "$x $y B"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM		-N	-O	-K	>>	$OUTPUT
#
y=$(echo $y - 0.03 | bc)
echo "$x $y C"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM		-N	-O	-K	>>	$OUTPUT
#
y=$(echo $y - 0.03 | bc)
echo "$x $y Others"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM	-N	-O	-K	>>	$OUTPUT

#~ #_QUALITIES

##_MAGNITUDES
#echo "48.21 32.72 .500"	|	gmt psxy	-R	-J	-Sc	-W1,black	-N	-K	-O	>> $OUTPUT
#echo "48.21 32.69 .375"	|	gmt psxy	-R	-J	-Sc	-W1,black	-N	-K	-O	>> $OUTPUT
#echo "48.21 32.66 .250"	|	gmt psxy	-R	-J	-Sc	-W1,black	-N	-K	-O	>> $OUTPUT
#echo "48.21 32.63 .125"	|	gmt psxy	-R	-J	-Sc	-W1,black	-N	-K	-O	>> $OUTPUT

#echo "48.29 32.615 Magnitude"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM+a90	-N	-O	-K	>>	$OUTPUT
#echo "48.25 32.72 4"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM		-N	-O	-K	>>	$OUTPUT
#echo "48.25 32.69 3"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM		-N	-O	-K	>>	$OUTPUT
#echo "48.25 32.66 2"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM		-N	-O	-K	>>	$OUTPUT
#echo "48.25 32.63 1"	| gmt pstext -R -J -F+f10p,Times-Bold,black+jLM		-N	-O	-K	>>	$OUTPUT
##_MAGNITUDES

#->>> ADD LEGEND


#->>> SMALL MAP

#R="-R43/64/23/41"
#J="-JC5c"
#B="-Ba6f3/a6f3wSnE"
#POS="-X11 -Y-1"
#FRAME="--MAP_FRAME_WIDTH=4p"
#FONT="--FONT_ANNOT_PRIMARY=10p,Times-Bold,black"
#gmt psbasemap	$R	$J		$B	$POS	-P	$FRAME	$FONT	-K	-O	>>	$OUTPUT
#gmt pscoast	$R	$J	-S90/180/255	-Df	-C90/180/225	-Gwhite -W.5p,midnightblue	-Na/.5p,black,-	-K	-O	>>	$OUTPUT

#gmt psxy -R -J -W1,red -K	-O << EOF >>	$OUTPUT
#50.0 34.7
#54.0 34.7
#54.0 37.0
#50.0 37.0
#50.0 34.7
#EOF

#-<<< SMALL MAP

#->>> ADD Legend

gmt pslegend -R -J -Fred -Dx10.2c/-1c+w2c/3c+jBL+l1.2 -C0.1i/0.1i --FONT=8p,Times-Bold,black -O << EOF >> $OUTPUT
#S 0.15i f0.1c/9i+l+t 0.25i black 1p 0.30i Thrust
#G 0.1i
#S 0.15i f0.1c/9i+l+s 0.25i black 1p 0.30i Strike-slip
#G 0.1i
#S 0.15i - 0.25i black 1p 0.30i Normal
EOF

#-<<< ADD Legend

#->>> SAVE & CONVERT

gmt psconvert ${OUTPUT} -A0.2 -Tg  -E900 -Qt4
rm ${OUTPUT} *.grd *.cpt track*

#-<<< SAVE & CONVERT
