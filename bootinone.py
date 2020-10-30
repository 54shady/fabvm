#!/usr/bin/env python
# coding=utf-8

import argparse
from subprocess import Popen, PIPE


def run_command(cmd, stdin=None, stdout=PIPE, stderr=None):
    """ run shell command """
    try:
        p = Popen(cmd, shell=True,
                  stdout=stdout, stdin=stdin, stderr=stderr,
                  executable="/bin/bash")
        out, err = p.communicate()
        return out
    except KeyboardInterrupt:
        print('Stop')


parser = argparse.ArgumentParser(description="LaunchQemu")
parser.add_argument("-n", "--name", type=str,
                    default="demo",
                    help="guest name")

parser.add_argument("-c", "--cpu", type=str,
                    default="host",
                    help="qemu-system-x86_64 -cpu help")

parser.add_argument("-m", "--mem", type=str,
                    default="2048",
                    help="mem size")

parser.add_argument("-s", "--smp", type=str,
                    default="1",
                    help="smp size")

parser.add_argument("-d", "--disk", type=str,
                    default="./demo.qcow2",
                    help="disk image")

parser.add_argument("--up", type=str,
                    default="./bridge_up.sh",
                    help="up script")

parser.add_argument("--do", type=str,
                    default="./bridge_down.sh",
                    help="down script")

parser.add_argument("--remove", type=str,
                    help="remove config: --remove nic")

args = parser.parse_args()
mac1 = run_command("openssl rand -base64 8 | md5sum | cut -c1-2")
mac2 = run_command("openssl rand -base64 8 | md5sum | cut -c1-2")

qemu = '/usr/bin/qemu-system-x86_64'
name = '-name guest=%s,debug-threads=on' % args.name
machine = '-machine pc,accel=kvm,usb=off,dump-guest-core=off'
cpu = '-cpu %s,hv_time,hv_relaxed,hv_vapic,hv_spinlocks=0x1fff' % args.cpu
m = '-m %s' % args.mem
rt = '-realtime mlock=off'
smp = '-smp %s,sockets=1,cores=1,threads=1' % args.smp
nuc = '-no-user-config'
nd = '-nodefaults'
rtc = '-rtc base=localtime,driftfix=slew'
gb = '-global kvm-pit.lost_tick_policy=delay'
gb += ' -global PIIX4_PM.disable_s3=1'
gb += ' -global PIIX4_PM.disable_s4=1'
nhpet = '-no-hpet'
nsd = '-no-shutdown'
boot = '-boot strict=on'
dev = '-device piix3-usb-uhci,id=usb'
drv = '-drive file=%s,format=qcow2,if=none,id=drive-ide0-0-0' % args.disk
dev += ' -device ide-hd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=1'
nic = '''-netdev tap,id=hostnet0,vhost=on,script=%s,downscript=%s \
-device virtio-net-pci,netdev=hostnet0,id=net0,mac=52:54:00:1b:%s:%s''' % (
    args.up, args.do, mac1[0:2], mac2[0:2])
dev += ' -device usb-tablet,id=input0,bus=usb.0,port=1'
vnc = '-vnc 0.0.0.0:0'
dev += ' -device qxl-vga,id=video0,ram_size=67108864,vram_size=67108864,vram64_size_mb=0,vgamem_mb=16'
msg = '-msg timestamp=on'

# map for remove
d = {"nic": nic}

# launch qemu with command
lcmdline = [qemu, name, machine, cpu, m, rt, smp, nuc, nd,
            rtc, gb, nhpet, nsd, boot, dev, drv, nic, vnc, msg]

# maybe remove some config
if args.remove:
    lcmdline.remove(d[args.remove])

scmdline = ' '.join(lcmdline)
run_command(scmdline)
