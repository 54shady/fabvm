# usage ./boot-nat.sh

# need console=ttyS0 in grub command
# -serial stdio

# auto login
# sshpass -p 0 ssh root@`awk '{ if ($4 == "52:54:00:12:34:27") print $1 }' /proc/net/arp`

# auto get ip address accroding to the mac address
# grep `virsh dumpxml vmname | grep 'mac address' | cut -b 21-37` /proc/net/arp  | awk '{ print $1 }'

# disk 2
#-drive file=./data.qcow2,format=qcow2,if=none,id=scsidisk1,cache=writeback \
#-device scsi-hd,bus=scsi0.0,channel=0,scsi-id=1,lun=2,drive=scsidisk1,bootindex=3,write-cache=on \

sudo qemu-system-x86_64 \
	-enable-kvm -cpu host \
	-m 2048 -smp 2 \
	-netdev tap,id=nd0,ifname=tap0,script=./nat_up.py,downscript=./nat_down.py \
	-device e1000,netdev=nd0,mac=52:54:00:12:34:27 \
	-boot menu=on \
	-vnc 0.0.0.0:0 \
	-device virtio-scsi-pci,id=scsi0 \
	-drive file=./gentoo.qcow2,format=qcow2,if=none,id=scsidisk0,cache=writeback \
	-device scsi-hd,bus=scsi0.0,channel=0,scsi-id=0,lun=2,drive=scsidisk0,bootindex=1,write-cache=on \
	-drive file=/tmp/gentoo.iso,format=raw,if=none,id=cdrom,readonly=on \
	-device ide-cd,drive=cdrom,bootindex=2 \
	-monitor stdio
