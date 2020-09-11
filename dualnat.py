# usage ./dualnat.sh vm.qcow2

# config the iptables for DNAT
# ./dnat.sh

sudo qemu-system-x86_64 \
	-enable-kvm -cpu host \
	-m 2048 -smp 2 \
	-netdev tap,id=nd0,ifname=tap0,script=./nat_up.py,downscript=./nat_down.py \
	-device e1000,netdev=nd0,mac=52:54:00:12:34:27 \
	-netdev tap,id=nd1,ifname=tap1,script=./nat_up.py,downscript=./nat_down.py \
	-device e1000e,netdev=nd1,mac=52:54:00:12:34:28 \
	-vnc 0.0.0.0:2 \
	$@
