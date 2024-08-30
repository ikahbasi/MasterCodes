
#path=../filter_test
path=$1
list_runs=$(ls $path)
current_path=$(pwd)
mkdir $path/located-nordics
for run in $list_runs
do

    if [[ $run != run* ]]
    then
        echo skip from $path/$run./filter_test
        continue
    fi

    echo $path/$run
    mkdir $path/$run/location
    cp $path/$run/catalog/nordic.out    $path/$run/location/nordic.out
    cp ./loc_func/*   $path/$run/location
    cd $path/$run/location

    bash run_hypoellipse.sh

cp nordic.out nordic-$run-old.out
hyp2nordinp=hypoel.out
genmag=n
PyHypEL2Nordic.py << EOF
$hyp2nordinp
$n
EOF
mv nordic.out nordic-$run.out

    cd $current_path
    cp $path/$run/location/nordic-$run.out  $path/located-nordics
    cp $path/$run/location/xyzm.dat         $path/located-nordics/xyzm-$run.dat
done
