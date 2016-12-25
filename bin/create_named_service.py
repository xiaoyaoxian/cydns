#!/usr/bin/env python
# -*- coding: utf-8 -*
# /etc/rc.d/init.d/named
# @zyqf
# email:xiaoyaoxian007@gmail.com

named = '''
#！/bin/bash
# vim /etc/rc.d/init.d/named
# chkconfig: 2345 70 50
# description: named

[ -r /etc/rc.d/init.d/functions ] && . /etc/rc.d/init.d/functions

PidFile=/usr/local/named/var/named.pid
LockFile=/var/lock/subsys/named
named=named

start() {
    [ -x /usr/local/named/sbin/$named ] || exit 4
    if [ -f $LockFile ]; then
        echo -n "$named is already running..."
        failure
        echo
        exit 5
    fi

    echo -n "Starting $named: "
    daemon --pidfile "$PidFile" /usr/local/named/sbin/$named -u named -4
    RETVAL=$?
    echo
    if [ $RETVAL -eq 0 ]; then
        touch $LockFile
        return 0
    else
        rm -f $LockFile $PidFile
        return 1
    fi
}

stop() {
    if [ ! -f $LockFile ];then
        echo "$named is not started."
        failure
    fi

    echo -n "Stopping $named: "
    killproc $named
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && rm -f $LockFile
    return 0
}

restart() {
    stop
    sleep 1
    start
}

reload() {
    echo -n "Reloading $named: "
    killproc $named -HUP
    RETVAL=$?
    echo
    return $RETVAL
}

status() {
    if pidof $named > /dev/null && [ -f $PidFile ]; then
        echo "$named is running..."
        /usr/local/named/sbin/rndc status
    else
        echo "$named is stopped..."
    fi
}

case $1 in
start)
    start ;;
stop)
    stop ;;
restart)
    restart ;;
reload)
    reload ;;
status)
    status ;;
*)
    echo "Usage:service named start | stop | restart |reload |status"
    exit 2;;
esac
'''
with open('/etc/rc.d/init.d/named', 'a') as f:
    f.write(str(named))

print "\n it has been done now!"
