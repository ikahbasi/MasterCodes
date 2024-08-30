#!/bin/bash

numRun=3
maxDist=75
distInt=25
maxDep=20
pOutlier=2
sOutlier=2
Reduced=6

f=nordic.out

PyNordic2HypEL_V2.py << EOF
$f

EOF


for i in `seq 1 $numRun`;
do

echo "Run $i"

hypoell-loc.sh hypoel
PyHypELStat.py << EOF
$Reduced
EOF

PyHypELTTCleaner.py << EOF
$maxDist
$distInt
$maxDep
$pOutlier
$sOutlier
EOF

[ -d run_${i} ] && rm -rf run_${i}
mkdir run_${i}
cp *png outliers.dat xyzm.dat hypoel.out run_${i}
cp hypoel_clean.pha hypoel.pha

done

:'
cp nordic.out nordic-old.out

hyp2nordinp=hypoel.out
genmag=n
PyHypEL2Nordic.py << EOF
$hyp2nordinp
$n
EOF
'
