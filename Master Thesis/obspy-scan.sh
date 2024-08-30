#!/bin/bash
############################
#     by IMAN KAHBASI      #
# master students in IIEES #
############################

#path of output
output=${1}
dir2save=./$output/obspy-scan

rm -r $dir2save
mkdir -p $dir2save
# all directory and subdirectory
find "../days" -type d > alldire.txt
# for each dir
while IFS= read -r DIR; do
    echo $DIR

    fs=$DIR/*.msd
    count=`ls -1 $fs 2>/dev/null | wc -l`
    name=$(basename $DIR)
    #name=$(echo "$fs" | sed 's/\//_/g' |sed 's/\.//g')
    out=$dir2save/$name.png

    if [ $count != 0 ]; then
        echo "$fs ---------> $out"
        echo "$fs ---------> $out" >> $dir2save/gaps.txt

        obspy-scan $fs --print-gaps -o $out >> $dir2save/gaps.txt

        echo
        echo >> $dir2save/gaps.txt
    fi
done < ./alldire.txt
rm alldire.txt
