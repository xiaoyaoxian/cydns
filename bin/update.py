#!/usr/bin/python
import hashlib
import os
# import sys


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash


def CalcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        return hash


def update_rpz(oldfile):
    check_exist(oldfile)
    newfile = 'rpz.zone.new'

    if os.path.isfile(newfile):
        os.system('rm -rf ' + newfile)
    url = "https://raw.githubusercontent.com/xiaoyaoxian/forginDNS/master/files/rpz.zone"
    os.system('wget -O ' + newfile + ' ' + url + '  --no-check-certificate')

    old = CalcMD5(oldfile)
    new = CalcMD5(newfile)

    if old == new:
        print('nothing to update')

    else:
        os.system('')
        os.system('mv ' + oldfile + ' ' + oldfile + '.bak')
        os.system('mv ' + newfile + ' ' + oldfile)
        os.system('sudo rndc reload')
        print('update have done,thanks!')


def check_exist(path):
    if os.path.isfile(path):
        print 'Find old rpz.zone'
    else:
        os.system('touch ' + path)


if __name__ == '__main__':
    oldfile = '/usr/local/named/var/rpz.zone'
    update_rpz(oldfile)
