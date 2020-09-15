# usage ./dualnat.sh vm.qcow2

# config the iptables for DNAT
# ./dnat.sh

sudo qemu-system-x86_64 \
	-enable-kvm -cpu host \
	-m 2048 -smp 2 \
	-netdev tap,id=nd0,ifname=tap0,script=./nat_up.py,downscript=./nat_down.py \
	-device e1000,id=e1k,netdev=nd0,mac=52:54:00:ff:3b:f5,bus=pci.0,addr=0x3 \
	-netdev tap,id=nd1,ifname=tap1,script=./nat_up.py,downscript=./nat_down.py \
	-device e1000e,id=e1ke,netdev=nd1,mac=52:54:00:68:00:22,bus=pci.0,addr=0x7 \
	-qmp unix:/tmp/vm.monitor,server,nowait \
	-D ./vm.log -writeconfig ./vm.conf \
	-vnc 0.0.0.0:2 \
	$@
