# IPTABLE

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
