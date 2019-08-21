#! /bin/sh

### BEGIN INIT INFO
# Provides:          easy.py
# Required-Start:    $remote_fs $syslog $network $named
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting easy.py"
    /home/pi/easy/easy.py &
    ;;
  stop)
    echo "Stopping easy.py"
    touch /home/pi/easy/stop
    ;;
  *)
    echo "Usage: /etc/init.d/easybutton.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
