#! /bin/sh

### BEGIN INIT INFO
# Provides:          monitor-bt.sh
# Required-Start:    $remote_fs $syslog $network
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting monitor-bt.sh"
    /usr/local/bin/monitor-bt.sh &
    ;;
  stop)
    echo "Stopping monitor-bt.sh"
    pkill -f /usr/local/bin/monitor-bt.sh
    ;;
  *)
    echo "Usage: /etc/init.d/monitorbt.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
