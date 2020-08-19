VM_SUBNET="192.168.53.0"
VMIP="192.168.53.206"
HOSTIP="172.20.101.236"

# forward host:6022 to vm:22
VM_SSH_PO=22
HOST_SSH_PO=6022

# forward for web
VM_WEB_PO=80
HOST_WEB_PO=6080

#iptables -A INPUT -p tcp --dport $HOST_SSH_PO -j ACCEPT
# for ssh
sudo iptables -t nat -A PREROUTING -d $HOSTIP -p tcp -m tcp --dport $HOST_SSH_PO -j DNAT --to-destination $VMIP:$VM_SSH_PO

# for web(lighttpd)
sudo iptables -t nat -A PREROUTING -d $HOSTIP -p tcp -m tcp --dport $HOST_WEB_PO -j DNAT --to-destination $VMIP:$VM_WEB_PO

#sudo iptables -t nat -A POSTROUTING -s $VM_SUBNET/255.255.255.0 -d $VMIP -p tcp -m tcp --dport $VM_SSH_PO
