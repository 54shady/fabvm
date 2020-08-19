sudo iptables -F -t filter
sudo iptables -F -t nat
sudo ifconfig natbr0 down
sudo brctl delbr natbr0
sudo kill -9 `pidof dnsmasq`
