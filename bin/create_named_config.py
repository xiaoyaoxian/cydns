#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /usr/local/named/etc/named.conf
# @zyqf
# email:xiaoyaoxian007@gmail.com

import urllib
import re


def getip():
    url = "http://pv.sohu.com/cityjson?ie=utf-8"
    request = urllib.urlopen(url).read()
    myip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}",request)[0]
    if myip:
        return myip
    else:
        raise RuntimeError("Failed to automatically get current IP address!")


IP_ADR = getip()  # no need to manually input current IP now :)
IP_ADR_list = IP_ADR.split('.')


print "\n Creating named.conf ....... \n"
named_conf = '''
options {
    directory "/usr/local/named/var";
    pid-file "named.pid";
    listen-on port 53 { any; };
    #listen-on port 5353 { any; };
    listen-on-v6 port 53 { any; };
    allow-query     { any; };

    rate-limit {
            ipv4-prefix-length 32;
            window 10;
            responses-per-second 20;
            errors-per-second 5;
            nxdomains-per-second 5;
            slip 2;
        };


    response-policy {
        zone "rpz.zone" policy given;
    }
    qname-wait-recurse no;
};

zone "." IN {
        type hint;
        file "named.root";
};


zone "rpz.zone" {
    type master;
    file "/usr/local/named/var/rpz.zone";
};
include "/usr/local/named/var/named.rfc1912.zones";

'''

with open('/usr/local/named/etc/named.conf', 'a') as f:
    f.write(str(named_conf))

print "named.conf has been created! \n"
print "--------------------------------------------------------- \n"


print "Creating named.empty ......."

named_empty = '''
$TTL 3H
@	IN SOA	@ rname.invalid. (
                    0    ; serial
                    1D	; refresh
                    1H	; retry
                    1W	; expire
                    3H )	; minimum
    NS	@
    A	127.0.0.1
    AAAA	::1
'''

with open('/usr/local/named/var/named.empty', 'a') as f:
    f.write(str(named_empty))

print "named.empty has been created! \n"
print "--------------------------------------------------------- \n"


print "Creating named.localhost ......."


named_localhost = '''
$TTL 1D
@	IN SOA	@ rname.invalid. (
                    0	; serial
                    1D	; refresh
                    1H	; retry
                    1W	; expire
                    3H )	; minimum
    NS    @
    A    127.0.0.1
    AAAA    ::1
'''

with open('/usr/local/named/var/named.localhost', 'a') as f:
    f.write(str(named_localhost))

print "named.localhost has been created! \n"
print "--------------------------------------------------------- \n"


print "Creating named.loopback ......."


named_loopback = '''
$TTL 1D
@	IN SOA	@ rname.invalid. (
                    0	; serial
                    1D	; refresh
                    1H	; retry
                    1W	; expire
                    3H )	; minimum
    NS    @
    A    127.0.0.1
    AAAA    ::1
'''

with open('/usr/local/named/var/named.loopback', 'a') as f:
    f.write(str(named_loopback))

print "named.loopback has been created! \n"
print "--------------------------------------------------------- \n"


print "Creating named.rfc1912.zones ......."

named_rfc1912_zones = '''
// named.rfc1912.zones:
//
// Provided by Red Hat caching-nameserver package
//
// ISC BIND named zone configuration for zones recommended by
// RFC 1912 section 4.1 : localhost TLDs and address zones
// and http://www.ietf.org/internet-drafts/draft-ietf-dnsop-default-local-zones-02.txt
// (c)2007 R W Franks
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

zone "localhost.localdomain" IN {
    type master;
    file "named.localhost";
    allow-update { none; };
};

zone "localhost" IN {
    type master;
    file "named.localhost";
    allow-update { none; };
};

zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
    type master;
    file "named.loopback";
    allow-update { none; };
};

zone "1.0.0.127.in-addr.arpa" IN {
    type master;
    file "named.loopback";
    allow-update { none; };
};

zone "0.in-addr.arpa" IN {
    type master;
    file "named.empty";
    allow-update { none; };
};

//
zone "cydns.pw" IN {
    type master;
    file "cydns.pw.b";
};

zone "%s.%s.%s.in-addr.arpa" IN {
type master;
file "cydns.pw.arpa";
};
''' % (IP_ADR_list[2], IP_ADR_list[1], IP_ADR_list[0])

with open('/usr/local/named/var/named.rfc1912.zones', 'a') as f:
    f.write(str(named_rfc1912_zones))

print "named.rfc1912.zones has been created! \n"
print "--------------------------------------------------------- \n"


print "Creating cydns.pw.arpa ......."


cydns_pw_arpa = '''
$TTL 1D
@	IN SOA	ns1.cydns.pw. root.cydns.pw. (
                    1997022700	; serial
                    28800	; refresh
                    1H	; retry
                    1W	; expire
                    3H )	; minimum
@	IN	NS	ns1.cydns.pw.
%s	IN	PTR	ns1.cydns.pw.
''' % IP_ADR_list[3]

with open('/usr/local/named/var/cydns.pw.arpa', 'a') as f:
    f.write(str(cydns_pw_arpa))

print "cydns.pw.arpa has been created! \n"
print "--------------------------------------------------------- \n"


print "Creating cydns.pw.b ......."


cydns_pw_b = '''
$TTL 1D
@	IN SOA	ns1.cydns.pw. root.cydns.pw. (
                    0	; serial
                    1D	; refresh
                    1H	; retry
                    1W	; expire
                    3H )	; minimum
@	IN	NS	ns1.cydns.pw.
ns1	IN	A	%s
www	IN	A	%s
''' % (IP_ADR, IP_ADR)

with open('/usr/local/named/var/cydns.pw.b', 'a') as f:
    f.write(str(cydns_pw_b))

print "cydns.pw.b has been created! \n"
