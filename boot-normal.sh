#!/bin/bash

# create disk image
# qemu-img create -f qcow2 disk.img 15G

# install from iso
# ./boot-normal.sh -hda disk.img -cdrom /path/to/iso/os.iso

# normal boot
# ./boot-normal.sh -hda disk.img -name "vm name"

# 3 hdd boot example
# ./boot-normal.sh -hda sda.qcow2 -hdb sdb.qcow2 -hdc sdc.qcow2 -drive file=disk.iso,index=3,media=cdrom

# Using spice protocol
# remote-viewer spice://localhost:3001

exec qemu-system-x86_64 \
	-enable-kvm \
	-cpu host,kvm=off \
	-machine pc-i440fx-2.7,accel=kvm,usb=off,dump-guest-core=off,mem-merge=off \
	-usb \
	-device usb-tablet \
	-smp 4 \
	-m 4096 \
	-boot d \
	$@ \
	-vnc 0.0.0.0:1 \
	-rtc base=localtime,clock=vm,driftfix=slew \
	-no-hpet \
	-no-shutdown \
	-global PIIX4_PM.disable_s3=1 \
	-global PIIX4_PM.disable_s4=0 \
	-object iothread,id=iothread1 \
	-object iothread,id=iothread2 \
	-no-user-config \
	-vga qxl \
	-nodefaults
