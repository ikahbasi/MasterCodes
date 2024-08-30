mkdir -p output/log-pictures; while true; do scrot -d 3600 '%Y-%m-%d-%H:%M:%S.png' -e 'mv $f ./output/log-pictures'; done
