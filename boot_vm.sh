#!/bin/bash

# create disk image
# qemu-img create -f qcow2 disk.img 15G
# dd if=/dev/zero of=disk.img bs=512 count=10000000

# install from iso
# ./boot_win.sh -hda disk.img -cdrom /path/to/iso/os.iso

# normal boot
# ./boot_win.sh -hda disk.img -name "vm name"
exec qemu-system-x86_64 \
	-enable-kvm \
	-cpu host,kvm=off \
	-machine pc-i440fx-2.7,accel=kvm,usb=off,dump-guest-core=off,mem-merge=off \
	-smp 6 \
	-m 4096 \
	-realtime mlock=off \
	-boot d \
	$@ \
	#-vnc 0.0.0.0:1 \
	-rtc base=localtime,clock=vm,driftfix=slew \
	-no-hpet \
	-no-shutdown \
	-global PIIX4_PM.disable_s3=1 \
	-global PIIX4_PM.disable_s4=0 \
	-realtime mlock=off \
	-object iothread,id=iothread1 \
	-object iothread,id=iothread2 \
	-no-user-config \
	-nodefaults
