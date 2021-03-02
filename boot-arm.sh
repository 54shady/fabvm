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

# virtio input device
#-device virtio-tablet-pci \
#-device virtio-keyboard-pci \

# scsi cdrom
#-device virtio-scsi-pci,id=scsi0 \
#-drive file=/path/to/cdrom.iso,format=raw,if=none,id=scsicdrom,readonly=on \
#-device scsi-cd,bus=scsi0.0,channel=0,scsi-id=0,lun=0,drive=scsicdrom,id=cdrom,bootindex=2 \

# spdk storage
#-object memory-backend-file,id=mem0,size=4G,mem-path=/dev/hugepages,share=on \
#-numa node,memdev=mem0 \
#-chardev socket,id=spdk_vhost_scsi0,path=/var/tmp/vhost.0 \
#-device vhost-user-scsi-pci,chardev=spdk_vhost_scsi0,num_queues=4,bootindex=2 \
#-chardev socket,id=spdk_vhost_blk0,path=/var/tmp/vhost.1 \
#-device vhost-user-blk-pci,chardev=spdk_vhost_blk0,bootindex=3 \

# monitor
#-monitor tcp:127.0.0.1:9999,server,nowait \
# nc 127.0.0.1 9999

# scsi storage
#-device megasas,id=scsi1 \
#-drive file=$@,format=qcow2,if=none,id=disk0,cache=none \
#-device scsi-hd,bus=scsi1.0,drive=disk0,scsi-id=1,bootindex=1 \

# for case that cpu can no schedule properly will case a slow gueset
# should schedule the cpu manually
# for example : set cpu run on range cpu from 100 to 120
#exec taskset -c 100-120 qemu-system-aarch64 \

gen_efi_firm()
{
	dd if=/dev/zero bs=1M count=64 of=QEMU_64M_CODE.fd
	dd if=/dev/zero bs=1M count=64 of=QEMU_64M_VARS.fd
	dd if=/usr/share/AAVMF/AAVMF_CODE.fd bs=1M of=QEMU_64M_CODE.fd conv=notrunc
}

# /dev/vda1 is the EFI partition
# efibootmgr -c -w -L "myubuntu" -d /dev/vda -p 1 -l EFI/ubuntu/grubaa64.efi
[ ! -f QEMU_64M_VARS.fd -o ! -f QEMU_64M_CODE.fd  ] && gen_efi_firm

exec qemu-system-aarch64 \
	-enable-kvm \
	-cpu host \
	-machine virt,accel=kvm,usb=off,dump-guest-core=off,gic-version=3 \
	-name guest=demo,debug-threads=on \
	-drive file=./QEMU_64M_CODE.fd,if=pflash,format=raw,unit=0,readonly=on \
	-drive file=./QEMU_64M_VARS.fd,if=pflash,format=raw,unit=1 \
	-m 4G \
	-smp 8 \
	-no-user-config \
	-nodefaults \
	-rtc base=localtime \
	-no-shutdown \
	-boot strict=on \
	-k en-us \
	-device pcie-root-port,id=pcierp0,multifunction=on \
	-device pcie-pci-bridge,id=pcibus0,bus=pcierp0 \
	-device qemu-xhci,id=usbhub1 \
	-device usb-kbd,bus=usbhub1.0 \
	-device usb-tablet,bus=usbhub1.0 \
    -netdev tap,id=hostnet0,vhost=on,script=./nat_up.py,downscript=./nat_down.py \
    -device virtio-net-pci,netdev=hostnet0,id=net0,mac=52:54:00:1b:fa:b2 \
	-drive file=$1,format=qcow2,if=none,id=disk0,cache=none \
	-device virtio-blk,drive=disk0,bootindex=1 \
	-device virtio-gpu-pci \
	-vnc 0.0.0.0:0 \
	-serial stdio \
	-sandbox off \
	-msg timestamp=on
