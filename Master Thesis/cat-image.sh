currentpath=$(pwd)
listpath=$(ls)

for path in $listpath
do
    echo $path
    cd $path
    d=$(pwd)
    name=$(basename $d)

    for lowcut in 0.1 0.5 1 2
    do
        echo $lowcut
        convert *run$lowcut-8*.png *run$lowcut-10*.png *run$lowcut-12*.png *run$lowcut-15*.png -append $lowcut.png
    done
    convert 0.1.png    0.5.png    1.png     2.png +append 00-$name.png
    rm      0.1.png    0.5.png    1.png     2.png
    mv      00-$name.png          $currentpath
    cd $currentpath
done
