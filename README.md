在已翻墙环境下，实现不会被污染、也不会被国内网站误判所在地的域名解析。

我们配置好翻墙工具后，还要解决 DNS 污染的问题才能正常访问全部网站。  
但是简单地让 DNS 解析全部走翻墙线路，在访问国内网站（如淘宝、豆瓣FM）时，经常被误判成海外用户，影响访问。  

通过此工具，可以基本解决上面的问题。  
它会判断一个域名是否被污染，若被污染，使用安全渠道（国外的 DNS）进行解析；若未被污染，使用本地渠道（如 ISP 提供的 DNS）进行解析。  
这样就不会得到不合适的 IP 地址了。  

有的翻墙服务器可能不支持 DNS 请求（UDP）的转发。此工具支持通过 Google Public DNS 提供的 DNS-Over-HTTPS 服务获取解析结果，也就是走 TCP 连接而不是 UDP 连接，也就不用担心翻墙服务器不支持了。

## 名词说明
本地渠道：解析未被污染的域名的渠道，能返回适合本地线路的解析结果  
安全渠道：解析被污染的域名的渠道  
伪造渠道：一个并没有提供 DNS 服务的国外 IP 地址，用来初步检测一个域名是否被污染

## 判断规则（符合任意一条规则视为被污染）
- 域名与白名单匹配
- 向伪造渠道发起请求并获得了解析结果
- 向安全渠道发起请求，获得的解析结果中的 CNAME 记录与白名单匹配
- 向本地渠道发起请求，获得的解析结果中的 CNAME 记录与白名单匹配

## 环境要求
本地能够运行 Python 2.7  
若在 OpenWrt 下运行，需安装 python-light、python-logging、python-openssl、python-codecs 包  
（注意检查路由器存储空间是否足够，详见 https://wiki.openwrt.org/doc/software/python ）

## 使用方法
把 `config/config.default.py` 复制一份，更名为 config.py，修改其中的参数值  
执行 `python rightdns.py`，现在此脚本就成了一个运行在指定端口上的 DNS 服务  
接下来只要把本机的 DNS 请求指向它即可

若需自定义白名单，可以创建一个 `config/whitelist.txt`，格式参见 `config/whitelist.default.txt`。（技术上，文件的每一行内容会被识别为一个正则表达式）

### 在 openwrt 中使用
将 rightdns 目录复制到 openwrt 的 /root 目录下  
把 /root/rightdns/rightdns.init 复制并重命名成 /etc/init.d/rightdns  
执行 `/etc/init.d/rightdns start` 开始运行  
执行 `/etc/init.d/rightdns enable` 以使其能在 openwrt 开机时自动开始运行

可以让此脚本作为 dnsmasq 的上级服务器  
修改 `/etc/dnsmasq.conf`，设置如下几行：
```
no-resolv
server=127.0.0.1#9999
```
（9999 是 config.py 里设置的端口号）  
执行 `/etc/init.d/dnsmasq restart` 重启 dnsmasq

因为此脚本解析速度相对直接解析会慢一点，建议加大 dnsmasq 的缓存，以尽量减少重复解析  
在 `/etc/dnsmasq.conf` 中加一句 `cache-size=1000` 即可

#### 另一个使用方式：用 rightdns 代替 dnsmasq
这种方式少了一部交接过程，也减少了出问题的可能性。  
不过问题在于，dnsmasq 在 openwrt 里除了是 dns server，还是 dhcp server，  
因此还要用另一个东西代替 dnsmasq 的 dhcp 部分。这里选择了 odhcpd

DNS 部分，配置 rightdns，让它运行在 53 端口且开机启动

DHCP 部分：
```
opkg remove dnsmasq odhcpd-ipv6only
opkg install odhcpd
```
编辑 `/etc/config/dhcp`  
把 `config odhcpd 'odhcpd'` 下的 `maindhcp` 的值改为 1  
然后在 `option dhcpv6 'server'` 下面加上一行 `option dhcpv4 'server'`
```
/etc/init.d/odhcpd restart
```

参考资料： https://github.com/openwrt/odhcpd


## 鸣谢
daemon.py 来自 https://github.com/serverdensity/python-daemon

## 相关资料
### socket(TCP) 相关教程
https://docs.python.org/2/howto/sockets.html  
http://openexperience.iteye.com/blog/145701

### udp 相关教程
http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868325264457324691c860044c5916ce11b305cb814000

### DNS 相关资料
DNS 流程说明： http://blog.csdn.net/crazw/article/details/8986504  
DNS 报文格式：  
http://www.cnblogs.com/cobbliu/archive/2013/04/02/2996333.html  
http://blog.csdn.net/tigerjibo/article/details/6827736

ASCII table:   http://www.asciitable.com/  
二进制计算器:    http://cn.calcuworld.com/%E4%BA%8C%E8%BF%9B%E5%88%B6%E8%AE%A1%E7%AE%97%E5%99%A8  
Google DNS:    https://developers.google.com/speed/public-dns/docs/dns-over-https

### 关于 DNS 污染
https://www.zhihu.com/question/19751271  
https://program-think.blogspot.com/2014/01/dns.html  
http://gfwrev.blogspot.jp/2009/11/gfwdns.html
