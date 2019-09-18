#! /bin/sh

BTSTATUS=`echo "info 3C:5C:C4:E7:0B:9A" | bluetoothctl | grep -i "connected" | grep "yes" | wc -l`

echo $BTSTATUS

