#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
from bin.update import CalcMD5

DowdloadURL = 'http://oiq47m3hh.bkt.clouddn.com/bind.tar.gz'
GccFilepath = '/tmp/bind.tar.gz'
system_platform = platform.platform()

if os.getuid() != 0:
    print "Please run with root!"
    sys.exit(1)


def select_platform(system_platform):
    if "buntu" in system_platform:
        print 'start Install on Ubuntu '
        os.system('sudo bash bin/alpha_ubuntu.sh')
    elif "entos" in system_platform:
        print 'start Install on Centos '
        os.system('sudo bash bin/centos.sh')
    elif "debian" in system_platform:
        print 'start Install on Debian '
        os.system('sudo bash bin/debian.sh')
    else:
        print "WARM:NOT SUPPORT YOUR SYSTEM!"


def Downloadfile(URL):
    if not os.path.isfile(GccFilepath):
        os.system('wget -O bind.tar.gz ' + URL + ' --no-check-certificate')
        os.system('mv bind.tar.gz /tmp')
        print "File download success."
    else:
        print 'File already exists!'

    if not checkfile(GccFilepath):
        print 'File hash does not match, consider check your network!'
        sys.exit(1)
    print "File hash matches remote file."


def checkfile(ck_filepath):
    MD5 = CalcMD5(ck_filepath)

    # why not put a coresponding text file containing the hash
    # of ck_filepath in the same dir as DowdloadURL, say,
    # https://o5obpsd7a.qnssl.com/bind.hash'? Then you can just
    # download and read hash value online, which would make it
    # easier to maintain if the bind.tar.gz should change.

    if MD5 != '173ce5e83e9ba31f8368367ee1ff7807':
        print 'But Md5 mismatch found!'
        print 'error MD5:', MD5
        os.system('rm -rf /tmp/bind.tar.gz')
        # Downloadfile(DowdloadURL)
        return False
    return True


if __name__ == '__main__':
    Downloadfile(DowdloadURL)
    select_platform(system_platform)

    os.system('crontab /root/foreignDNS/bin/dnscron.cron')
    os.system('/sbin/service crond reload')
    os.system('/sbin/service crond restart')
