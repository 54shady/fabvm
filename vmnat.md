# IPTABLE, NAT, ROUTE

## 不同桥接框架图

不同桥接模式

![bridge](./bridges.png)

## 相关信息前提

- HOSTIP: 172.20.101.236
- VMIP: 192.168.53.206

## HOOKS in linux kernel

内核中的5个hooks

![hooks](./hooks.png)

## 报文在内核中的路径

- 报文流入本机: PREROUTING->INPUT->UserApp
- 报文流出本机: UserApp->OUTPUT->POSTROUTING
- 转发: PREROUTING->FORWARD->POSTROUTING

## DNAT/SNAT应用

- SNAT: 用于局域网访问互联网(数据包中源ip被修改)
- DNAT: 用于互联网访问局域网(数据包中目的ip被修改)

### SNAT配置

配置SNAT后在虚拟机能访问外网(将192.168.53.0/24网段发出的包原地址改成172.20.101.236)

	sudo iptables -t nat -A POSTROUTING -s 192.168.53.0/255.255.255.0 -j SNAT --to-source 172.20.101.236

或者使用MASQUERADE做动态SNAT

	sudo iptables -t nat -A POSTROUTING -s 192.168.53.0/255.255.255.0 -j MASQUERADE

### DNAT配置

将访问host:6022(6080)端口的数据修改为访问guest:22(80)端口

	sudo iptables -t nat -A PREROUTING -d 172.20.101.236 -p tcp -m tcp --dport 6022 -j DNAT --to-destination 192.168.53.206:22
	sudo iptables -t nat -A PREROUTING -d 172.20.101.236 -p tcp -m tcp --dport 6080 -j DNAT --to-destination 192.168.53.206:80

## 双网卡双NAT

HOST上有一张有线网卡eth0(br0)和一张无线网卡(wlan0)

- eth0(br0) 		172.20.101.101(gw 172.20.101.1)
- wlan0				172.20.238.101(gw 172.20.236.1)
- natbr0           	194.168.53.1/24
- natbr1           	193.168.53.1/24

### multipath route setting(多重路由,负载均衡设置)

设置多重路由和负载均衡

	ip ro add default nexthop via 172.20.101.1 dev br0 weight 1 nexthop via 172.20.236.1 dev wlan0 weight 1

查看路由情况(ip route show)

	default
			nexthop via 172.20.101.1  dev br0 weight 1
			nexthop via 172.20.236.1  dev wlan0 weight 1
	172.20.101.0/24 dev br0  proto kernel  scope link  src 172.20.101.101  metric 425
	172.20.236.0/22 dev wlan0  proto kernel  scope link  src 172.20.238.101  metric 600
	193.168.53.0/24 dev natbr1  proto kernel  scope link  src 193.168.53.1
	194.168.53.0/24 dev natbr0  proto kernel  scope link  src 194.168.53.1

### 防火墙设置(下面三种中任意一种即可)

第一种设置

	iptables -t nat -A POSTROUTING -s 194.168.53.0/24 -j SNAT --to-source 172.20.101.101
	iptables -t nat -A POSTROUTING -s 193.168.53.0/24 -j SNAT --to-source 172.20.238.101

第二种设置

	iptables -t nat -A POSTROUTING -s 194.168.53.0/24 -o br0 -j MASQUERADE
	iptables -t nat -A POSTROUTING -s 193.168.53.0/24 -o wlan0 -j MASQUERADE

第三种设置

	iptables -t nat -A POSTROUTING -s 193.168.53.174 -o wlan0 -j MASQUERADE
	iptables -t nat -A POSTROUTING -s 194.168.53.173 -o br0 -j MASQUERADE

### 调试过程中抓ICMP包

	tcpdump -nn icmp -i [ br0 | tap0 | wlan0 ]

### FAQ

对于虚拟机是linux系统,在host和guest中都需要配置反向过滤才能使两块网卡同时使用

需要修改(改成0或2)相应的网卡的rp_filter配置

	echo 0 > /proc/sys/net/ipv4/conf/wlan0/rp_filter

## 网络模式热切换,网卡热插拔(使用qmp命令, 示例如下)

- netdev_add对应qemu命令行启动参-netdev
- device_add对应qemu命令行启动参-device

### NAT模式下网卡热插拔

移除网卡

	device_del e1ke
	netdev_del nd1

	device_del e1k
	netdev_del nd0

添加网卡

	netdev_add tap,id=nd0,ifname=tap0,script=./nat_up.py,downscript=./nat_down.py
	device_add e1000,id=e1k,netdev=nd0,mac=52:54:00:ff:3b:f5,bus=pci.0,addr=0x3

	netdev_add tap,id=nd1,ifname=tap1,script=./nat_up.py,downscript=./nat_down.py
	device_add e1000,id=e1ke,netdev=nd1,mac=52:54:00:68:00:22,bus=pci.0,addr=0x7

### 桥接模式网卡热插拔

移除网卡

	device_del net-0
	netdev_del hostnet-0

添加网卡

	netdev_add tap,id=hostnet-0,vhost=on,script=./bridge_up.sh,downscript=./bridge_down.sh
	device_add virtio-net-pci,netdev=hostnet-0,id=net-0,mac=52:54:00:ff:3b:f5,bus=pci.0,addr=0x03
