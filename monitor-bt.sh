#! /bin/sh

while true; do
    BTSTATUS=`echo "info 3C:5C:C4:E7:0B:9A" | bluetoothctl | grep -i "connected" | grep "yes" | wc -l`
    if [ $BTSTATUS -ne "1" ]
    then
       echo "connect 3C:5C:C4:E7:0B:9A" | bluetoothctl
    fi
   
    sleep 5
done

