#!/bin/bash

# normal boot
# ./virtio-input-host-pass.sh -hda disk.img -name "vm name"

# lsusb figure out the usb mouse and keyboard on host
# cat /proc/bus/input/devices
# passthrough the evdev of mouse and keyboard
# -device virtio-input-host-pci,evdev=/dev/input/eventN

# don't passthrough the usb controller to the guest

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
	-device virtio-input-host-pci,evdev=/dev/input/event4 \
	-device virtio-input-host-pci,evdev=/dev/input/event3 \
	-device virtio-net,netdev=vmnic \
	-netdev tap,id=vmnic,ifname=vnet0,script=no,downscript=no \
	-full-screen \
	-nodefaults \
	-nographic
