#!/bin/bash
# usage:
# ./boot-disk.sh disk.qcow2

# blk
#-drive file=$@,format=qcow2,if=none,id=disk0,cache=none \
#-device virtio-blk,drive=disk0 \

# scsi
#-device virtio-scsi-pci,id=scsi0 \
#-drive file=$@,format=qcow2,if=none,id=scsidisk0,cache=writeback \
#-device scsi-hd,bus=scsi0.0,channel=0,scsi-id=0,lun=2,drive=scsidisk0,bootindex=1,write-cache=on \

exec qemu-system-aarch64 \
	-enable-kvm \
	-cpu host \
	-machine virt,accel=kvm,usb=off,dump-guest-core=off,gic-version=3 \
	-name guest=demo,debug-threads=on \
	-drive file=/usr/share/AAVMF/AAVMF_CODE.fd,if=pflash,format=raw,unit=0,readonly=on \
	-m 8192 \
	-smp 8 \
	-no-user-config \
	-nodefaults \
	-rtc base=localtime \
	-no-shutdown \
	-boot strict=on \
	-k en-us \
	-device pcie-root-port,id=pcierp0,multifunction=on \
	-device pcie-pci-bridge,id=pcibus0,bus=pcierp0 \
	-device piix3-usb-uhci,bus=pcibus0,addr=0x1 \
	-netdev tap,id=hostnet0,vhost=on,script=./bridge_up.sh,downscript=./bridge_down.sh \
	-device virtio-net-pci,netdev=hostnet0,id=net0,mac=52:54:00:1b:fa:b2 \
	-drive file=$@,format=qcow2,if=none,id=disk0,cache=none \
	-device virtio-blk,drive=disk0 \
	-device virtio-gpu-pci \
	-device virtio-tablet-pci \
	-device virtio-keyboard-pci \
	-vnc 0.0.0.0:0 \
	-sandbox off \
	-msg timestamp=on
