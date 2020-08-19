# usage ./nat_vm.sh vm.qcow2

# config the iptables for DNAT
# ./dnat.sh

# clean all the nat config
# ./cleannat.sh

sudo qemu-system-x86_64 \
	-enable-kvm -cpu host \
	-m 2048 -smp 2 \
	-netdev tap,id=nd0,ifname=tap0,script=./bridge_nat_helper \
	-device e1000,netdev=nd0,mac=52:54:00:12:34:27 \
	$@
