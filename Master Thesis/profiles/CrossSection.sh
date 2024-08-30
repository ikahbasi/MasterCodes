#!/bin/bash

clear

#________LOADING FILES

#~ root="DB/event/Bushehr_Hypo71"
root="DB/event/nordic-reference"
#~ root="DB/event/Ilam_HypoDD_1DC1_jadid"
#~ root="DB/event/Bushehr_HypoDD_1DC2"
#~ root="DB/event/Bushehr_HypoDD_3DC1"
#~ root="DB/event/Bushehr_HypoDD_3DC2"
#~ root="DB/event/Bushehr_NLLOC_1D"
#~ root="DB/event/Bushehr_NLLOC_3D"
#~ root="DB/event/Bushehr_Hypoellipse"


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
topo_grd=DB/grd/Ilam.grd
OUTNAME=`echo $root | awk '{split($0, a, "/"); print a[3]}'`

[ ! -d $root ] && echo "Directory $root DOES NOT exists." && exit

#________CREATE DIRECTORY FOR SAVING FIGS

mkdir -p FIG/$OUTNAME

#________RESET GMT DEFAULS

FONT="--FONT_ANNOT_PRIMARY=8p,27,black --FONT_LABEL=8p,27,black"
gmt gmtset MAP_TICK_LENGTH_PRIMARY=2.5p

#________EXTARCT EARTHQUAKE INTO CALSSES

python << EOF
import os

from PyEQ_Quality import sum_reader

root="$root"
sum_reader(root=root, sum_type="xyzm")
EOF

eq_xyz_A=$root/QA.dat
eq_xyz_B=$root/QB.dat
eq_xyz_C=$root/QC.dat
eq_xyz_D=$root/OT.dat

#________LOOP OVER CROSS SECTIONS

c=1

while read line
do

echo "Working on CrossSection $c"

#___DEFINE TEMPORARY VARIABLES

OUTPUT=FIG/$OUTNAME/Cross_${c}.ps
track=track_$c
topo_xyz=topo_xyz_${c}.dat
stlon=`echo $line | awk '{print $1}'`
stlat=`echo $line | awk '{print $2}'`
azimut=`echo $line | awk '{print $3}'`
semilen=`echo $line | awk '{print $4}'`
p_width=`echo $line | awk '{print $5}'`
xy_res=1.0
maxdep=20

#___PLOT TOPOGRAPHY

gmt project	-C$stlon/$stlat	-A$azimut	-L0/$semilen	-G$xy_res	-Q	>	$track
gmt grdtrack	$track	-fg	-G$topo_grd	|	awk '{print $3, $4/1000}'	>	$topo_xyz

awk 'NR==1{print $1,0,$3}' $topo_xyz > tmp
cat $topo_xyz >> tmp
awk 'END{print $1,0,$3}' $topo_xyz >> tmp
mv tmp $topo_xyz

R=`minmax -C -I1 topo_xyz_${c}.dat | awk '{printf "-R%.1f/%.1f/%.1f/%.1f", $1, $2, 0, 2}'`
J="-JX12c/1.2c"
B=`minmax -C -I1 topo_xyz_${c}.dat | awk '{printf "-Ba%.ff%.1f/a1f.5:Height(km):W",($2-$1)/4,($2-$1)/8}'`
POS="-X8 -Y15"

gmt psbasemap	$R	$J	$B	$FONT	$POS	-K	>	$OUTPUT
gmt psxy	$topo_xyz	-R	-J	-W1	-Gp300/30:BKHAKI	-L	-K	-O	>>	$OUTPUT

Ax=`awk 'NR==1{print $1}' $track` 
Ay=`awk 'NR==1{print $2}' $track`
Bx=`awk 'END{print $1}' $track`
By=`awk 'END{print $2}' $track`

PyFaultOnProfile.py 5 $Ax $Ay $Bx $By `minmax -C $track | awk '{print 0,$5}'`
gmt pstext fault_on_profile.dat	-R -J	-F+f+a+j	-N	-O	-K	>>	$OUTPUT

#___PLOT SEISMICITY

R=`minmax topo_xyz_${c}.dat -C | awk -v maxdep=$maxdep '{print "-R"$1"/"$2"/0/"maxdep}'`
J=`minmax topo_xyz_${c}.dat -C | awk -v maxdep=$maxdep '{print "-JX12c/-"12*maxdep/$2"c"}'`
B=`minmax -C -I1 topo_xyz_${c}.dat | awk '{printf "-Ba%.ff%.1f:Distance(km):/a5f5:Depth(km):WSe",($2-$1)/5,($2-$1)/3}'`
POS="-Y-4.8"
p_lable_right="47 1.5 N\260$azimut"
p_lable_left="4 1.5 Profile $c"

if [ `minmax -C -I1 topo_xyz_${c}.dat | awk '{print $2}'` -eq 90 ];
then
B=`minmax -C -I1 topo_xyz_${c}.dat | awk '{printf "-Ba%.ff%.1f:Distance(km):/a10f5:Depth(km):WSe",($2-$1)/3,($2-$1)/6}'`
POS="-Y-4"
p_lable_right="47 1.5 N\260$azimut"
p_lable_left="6 1.5 Profile $c"
fi

gmt project $eq_xyz_A -A$azimut -C$stlon/$stlat -L0/$semilen -W-$p_width/$p_width -Fpz -Q > eqA.dat
gmt project $eq_xyz_B -A$azimut -C$stlon/$stlat -L0/$semilen -W-$p_width/$p_width -Fpz -Q > eqB.dat
gmt project $eq_xyz_C -A$azimut -C$stlon/$stlat -L0/$semilen -W-$p_width/$p_width -Fpz -Q > eqC.dat
gmt project $eq_xyz_D -A$azimut -C$stlon/$stlat -L0/$semilen -W-$p_width/$p_width -Fpz -Q > eqD.dat

gmt psbasemap	$R	$J	$B	$FONT	$POS	-K	-O	>>	$OUTPUT

python << EOF
import os

d1=("eqA.dat", "$d1_clr")
d2=("eqB.dat", "$d2_clr")
d3=("eqC.dat", "$d3_clr")
d4=("eqD.dat", "$d4_clr")

for c,i in enumerate([d4, d3, d2, d1]):

    fc = i[1]
    ec = "black"

    if c==0:
        fc = "white"
        ec = i[1]

    cmd = "awk '{print \$1,\$2,\$3*0.125}' "+i[0]+" | gmt psxy -R -J -Sc.1 -G"+fc+" -W.5,black -K -O >> $OUTPUT"
    os.system(cmd)

EOF

# Profile-lable
echo $p_lable_right	| gmt pstext -R -J -F+f7p,27,black	-Gwhite	-W.1p	-K	-O	>>	$OUTPUT
echo $p_lable_left	| gmt pstext -R -J -F+f7p,27,black	-Gwhite	-W.1p	-K	-O	>>	$OUTPUT

#___PLOT FOCAL MECHANISM

X1=`awk 'NR==1{print $1}' $track`
Y1=`awk 'NR==1{print $2}' $track`
X2=`awk 'END{print $1}' $track`
Y2=`awk 'END{print $2}' $track`

A="-Aa"$X1"/"$Y1"/"$X2"/"$Y2"/90/"$p_width"/0/"$maxdep

#_CLASS A
#FM1=DB/focal/Y1/b1_fmsA.dat
#FM2=DB/focal/Y2/b2_fmsA.dat
#FM3=DB/focal/Y3/b3_fmsA.dat
#FM_TMP=FM_TMP.dat
#3FMC.py -iAR -oAR $FM1 > $FM_TMP
#FMC.py -iAR -oAR $FM2 >> $FM_TMP
#FMC.py -iAR -oAR $FM3 >> $FM_TMP
#grep " R\|R-SS\| N\|N-SS" $FM_TMP | awk '!/#/{$NF="";OFS="\t"; print $0}' > tmp_foc.dat
#gmt pscoupe tmp_foc.dat	-R	-J	$A	-Sa.5/7p/5p	-L.1	-M	-Gblue	-K	-O > /dev/null
#AaFile=`ls Aa* | awk 'NR==1{print $1}'`
#mv $AaFile DB1A.dat
#cat DB1A.dat > psmeca_A.out

#_CLASS B
#FM1=DB/focal/Y1/b1_fmsB.dat
#FM2=DB/focal/Y2/b2_fmsB.dat
#FM3=DB/focal/Y3/b3_fmsB.dat
#FM_TMP=FM_TMP.dat
#FMC.py -iAR -oAR $FM1 > $FM_TMP
#FMC.py -iAR -oAR $FM2 >> $FM_TMP
#FMC.py -iAR -oAR $FM3 >> $FM_TMP
#grep " R\|R-SS\| N\|N-SS" $FM_TMP | awk '!/#/{$NF="";OFS="\t"; print $0}' > tmp_foc.dat
#gmt pscoupe tmp_foc.dat	-R	-J	$A	-Sa.5/7p/5p	-L.1	-M	-K	-O > /dev/null
#AaFile=`ls Aa* | awk 'NR==1{print $1}'`
#mv $AaFile DB1B.dat
#cat DB1B.dat > psmeca_B.out

#_CMT
#FM1=DB/focal/CMT/CMT.dat
#FM_TMP=FM_TMP.dat
#FMC.py -iAR -oAR $FM1 > $FM_TMP
#grep " R\|R-SS\| N\|N-SS" $FM_TMP | awk '!/#/{$NF="";OFS="\t"; print $0}' > tmp_foc.dat
#gmt pscoupe tmp_foc.dat	-R	-J	$A	-Sa.5/7p/5p	-L.1	-M	-K	-O > /dev/null
#AaFile=`ls Aa* | awk 'NR==1{print $1}'`
#mv $AaFile DBC.dat
#cat DBC.dat > psmeca_C.out


#_MERGE

#awk '{print $0,1}' psmeca_A.out  > Total.dat
#awk '{print $0,2}' psmeca_B.out >> Total.dat
#awk '{print $0,3}' psmeca_C.out >> Total.dat

#_AUTO-ADJUST

#xy=`echo $R | awk -F'[R|/]' '{print $2+3,$3-3,$4+3,$5-3}'`
#nx=3 # Number of grid point in Distance
#ny=4 # Number of grid point in Depth
#PyAdjustFM.py Total.dat $xy $nx $ny
#FM=Adjusted_FM.dat

#awk '{if ($15==1) print $0}' Adjusted_FM.dat > FM_CA.dat
#awk '{if ($15==2) print $0}' Adjusted_FM.dat > FM_CB.dat
#awk '{if ($15==3) print $0}' Adjusted_FM.dat > FM_CC.dat

#awk '{NF-=2; print $0}' FM_CA.dat | gmt psmeca -R	-J	-C.5,black,.,P.05	-Sc.5/7p/5p	-L.1	-M	-Gred	-K	-O	>>	$OUTPUT
#awk '{print $1,$2}' FM_CA.dat  | gmt psxy -R -J -Sc0.10 -Gblack -W.1,black	-K	-O >> $OUTPUT
#awk '{print $1,$2}' FM_CA.dat  | gmt psxy -R -J -Sc0.08 -Gwhite -W.1,black	-K	-O >> $OUTPUT
#awk '{print $12,$13+1.5,$14}' FM_CA.dat | gmt pstext -R -J -F+f6p,27,black	-Gwhite	-K	-O	>>	$OUTPUT

#awk '{NF-=2; print $0}' FM_CB.dat | gmt psmeca -R	-J	-C.5,black,.,P.05	-Sc.5/7p/5p	-L.1	-M	-Gblue	-K	-O	>>	$OUTPUT
#awk '{print $1,$2}' FM_CB.dat  | gmt psxy -R -J -Sc0.10 -Gblack -W.1,black	-K	-O >> $OUTPUT
#awk '{print $1,$2}' FM_CB.dat  | gmt psxy -R -J -Sc0.08 -Gwhite -W.1,black	-K	-O >> $OUTPUT
#awk '{print $12,$13+1.5,$14}' FM_CB.dat | gmt pstext -R -J -F+f6p,27,black+jMR	-K	-O	>>	$OUTPUT

#awk '{NF-=2; print $0}' FM_CC.dat | gmt psmeca -R	-J	-C.5,black,.,P.05	-Sc.5/7p/5p	-L.1	-M	-Gblack	-K	-O	>>	$OUTPUT
#awk '{print $1,$2}' FM_CC.dat  | gmt psxy -R -J -Sc0.10 -Gblack -W.1,black	-K	-O >> $OUTPUT
#awk '{print $1,$2}' FM_CC.dat  | gmt psxy -R -J -Sc0.08 -Gwhite -W.1,black	-K	-O >> $OUTPUT
#awk '{print $12,$13+1.5,$14}' FM_CC.dat | gmt pstext -R -J -F+f6p,27,black+jMR	-K	-O	>>	$OUTPUT

#rm Aa* FM_CA.dat FM_CB.dat FM_CC.dat Total.dat psmeca_A.out psmeca_B.out psmeca_C.out
echo "0 0 0 0" | gmt psxy -R -J -Sc0 -Gblack	-O >> $OUTPUT

gmt psconvert ${OUTPUT} -A0.2 -Tg  -E900 -Qt4
rm ${OUTPUT}
let c=c+1

done < $profiles

rm *.dat track*
