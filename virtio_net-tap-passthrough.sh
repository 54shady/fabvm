#!/bin/bash

# create disk image
# qemu-img create -f qcow2 disk.img 15G

# Virtual network cable(TAP)

# create vnet0
# tunctl -b -t vnet0

# active vnet0
# ip link set vnet0 up

# create a bridge name br0
# brctl addbr br0

# add vnet0 to bridge
# brctl addif br0 vnet0

# add eth0(physical net card) to bridge
# brctl addif br0 eth0

# brctl show
#
# br0 aa.bb.cc.dd
# eth0 (no ip)
# vnet0 (no ip)

# virtual machine ip address aa.bb.cc.xx
exec qemu-system-x86_64 \
	-enable-kvm \
	-cpu host,kvm=off \
	-machine pc-i440fx-2.7,accel=kvm,usb=off,dump-guest-core=off,mem-merge=off \
	-smp 4 \
	-m 2048 \
	-realtime mlock=off \
	-boot d \
	$@ \
	-vnc 0.0.0.0:1 \
	-rtc base=localtime,clock=vm,driftfix=slew \
	-no-hpet \
	-no-shutdown \
	-global PIIX4_PM.disable_s3=1 \
	-global PIIX4_PM.disable_s4=0 \
	-realtime mlock=off \
	-object iothread,id=iothread1 \
	-object iothread,id=iothread2 \
	-no-user-config \
	-vga none \
	-device vfio-pci,host=00:02.0,bus=pci.0,addr=0x2 \
	-device vfio-pci,host=00:14.0 \
	-device virtio-net,netdev=vmnic \
	-netdev tap,id=vmnic,ifname=vnet0,script=no,downscript=no \
	-full-screen \
	-nodefaults \
	-nographic
