#!/bin/bash

# create disk image
# qemu-img create -f qcow2 disk.img 15G
# dd if=/dev/zero of=disk.img bs=512 count=10000000

# install from iso
# ./boot_win.sh -cdrom /path/to/iso/os.iso

# normal boot
exec qemu-system-x86_64 \
	-enable-kvm \
	-cpu host,kvm=off \
	-machine pc-i440fx-2.7,accel=kvm,usb=off,dump-guest-core=off,mem-merge=off \
	-smp 6 \
	-m 4096 \
	-realtime mlock=off \
	-boot d \
	-hda myvm10.img \
	-name "win10 WM" \
	-vnc 0.0.0.0:1 \
	$@
