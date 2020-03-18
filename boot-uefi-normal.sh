#!/bin/bash

# normal boot
# ./boot-uefi-normal.sh -hda disk.img -name "vm name"

# ovmf firmware
# sys-firmware/edk2-ovmf

exec qemu-system-x86_64 \
	-enable-kvm \
	-cpu host,kvm=off \
	-machine pc-i440fx-2.7,accel=kvm,usb=off,dump-guest-core=off,mem-merge=off \
	-bios /usr/share/edk2-ovmf/OVMF_CODE.fd \
	-usb \
	-device usb-tablet \
	-m 2048 \
	-smp 2 \
	$@
