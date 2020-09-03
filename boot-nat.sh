# usage ./boot-nat.sh vm.qcow2

# config the iptables for DNAT
# ./dnat.sh

sudo qemu-system-x86_64 \
	-enable-kvm -cpu host \
	-m 2048 -smp 2 \
	-netdev tap,id=nd0,ifname=tap0,script=./nat_up,downscript=./nat_down \
	-device e1000,netdev=nd0,mac=52:54:00:12:34:27 \
	-vnc 0.0.0.0:2 \
	$@
