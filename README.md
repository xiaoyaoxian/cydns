
# NOTE
* Your VPS must be in China
* Only support Centos 6.7 64  or Ubuntu|Debian
* You need remove old bind version RUN `yum remove bind*`


# Install (root required)
## (rehl series only, redhat/centos/fedora which uses YUM)


### No need to manually input IP address now :)

#Update file rpz.zone

Centos系统将自动执行任务,Ubuntu暂未测试,如不自动执行请按照下方手动添加

* `crontab -e`

* 0 2 * * * python /root/forginDNS/bin/update.py
* 0 3 * * * service named restart


#thanks list
* [@HuanMeng](https://github.com/HuanMeng0)
* [@codexss](https://github.com/codexss)
* [@tonyxue](https://github.com/tonyxue)
* [@fangzhengjin](https://github.com/fangzhengjin)
* [@brunobell](https://github.com/brunobell)
# cydns
