#!/bin/bash
# @zyqf
# email:xiaoyaoxian007@gmail.com
# NOT run !
RUNPATH=`pwd`
echo '|-------------------Installing---------------------|' ;
echo '|install gcc openssl openssl-devel perl bind-utils |' ;
echo '|Development Tools; About download size:60MB       |' ;
echo '|  PandaDNS Project : https://github.com/xiaoyaoxian/forginDNS  |' ;
echo '|--------------------------------------------------|' ;
sudo apt-get install libssl-dev make;
sudo  apt-get install gcc;

echo '|-------------------Downloading--------------------|' ;
echo '|download bind-9.10.3-P4 ..........................|' ;
echo '|--------------------------------------------------|' ;
cd /tmp;
#wget -O bind.tar.gz "http://oiq47m3hh.bkt.clouddn.com/bind.tar.gz";
tar -zxvf bind.tar.gz;


echo '|-------------------Configure----------------------|' ;
echo '|./configure --prefix=/usr/local/named ............|' ;
echo '|--------------------------------------------------|' ;


cd bind-9.10.3-P4;
./configure --prefix=/usr/local/named  --enable-threads --enable-largefile;

echo '|-------------------Make install-------------------|' ;
echo '|make install bind9.3.4 ...........................|' ;
echo '|--------------------------------------------------|' ;
make && make install;

echo '|-------------------Final setup--------------------|' ;
setenforce 0;
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config;

groupadd named;
useradd -g named -d /usr/local/named -s /sbin/nologin named;

cd /usr/local/named/etc;

/usr/local/named/sbin/rndc-confgen > /usr/local/named/etc/rndc.conf;
cat rndc.conf > /usr/local/named/etc/rndc.key;
chmod 777 /usr/local/named/var;
tail -10 rndc.conf | head -9 | sed s/#\ //g > /usr/local/named/etc/named.conf;

cd /usr/local/named/var;

dig @a.root-servers.net . ns > /usr/local/named/var/named.root;
#rm -rf /etc/rc.d/init.d/named;
python $RUNPATH/bin/create_named_config.py;
#chmod 755 /etc/rc.d/init.d/named;
#chkconfig --add named;

touch /usr/local/named/var/rpz.zone;
#python /root/DNS/bin/create_named.py;
python $RUNPATH/bin/update.py;

mkdir /var/named;
ln -s /usr/local/named/var/* /var/named/;
ln -s /usr/local/named/etc/named.conf /etc/;
ln -s /usr/local/named/sbin/* /usr/bin/;

chown -R root:named /usr/local/named/var;
named && echo 'service is running!';
echo '|-------------------COMPLETE-----------------------|' ;
echo '|      The script was finish.Please Check!         |' ;
echo '|  PandaDNS Project : https://github.com/xiaoyaoxian/forginDNS  |' ;
echo '|-------------------ENJOY IT!----------------------|' ;

echo '|USAG:| start:named | stop:killall named ' ;


