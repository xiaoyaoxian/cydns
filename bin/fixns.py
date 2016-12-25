#!/usr/bin/env python
# dig @a.root-servers.net . ns > /usr/local/named/var/named.root

import os
import sys

filename = '/usr/local/named/var/named.root'
if os.path.isfile(filename):
    print 'OK,file exists.'
else:
    os.system('touch ' + filename)

while True:
    with open(filename, 'rb') as f:
        text = f.read()
        if 'b.root-servers' not in text:
            os.system('dig @a.root - servers.net . ns > ' + filename)
        else:
            print 'named.root is ok'
            os.system('service named restart')
            sys.exit()
