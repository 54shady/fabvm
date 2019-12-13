#!/bin/bash

# create disk image
# qemu-img create -f qcow2 disk.img 15G
# dd if=/dev/zero of=disk.img bs=512 count=10000000

# install from iso
# ./install_vm.sh -hda disk.img -name "vm name" -cdrom /path/to/iso/os.iso

function print_usage()
{
	echo "Usage"
	echo "./install_vm.sh -hda disk.img -name "vm name" -cdrom /path/to/iso/os.iso"
}

if [ $# -lt 6 ]
then
	print_usage
	exit
fi

# normal boot
exec qemu-system-x86_64 \
	-enable-kvm \
	-cpu host \
	-smp $(nproc) \
	-m 4096 \
	-boot d \
	$@
