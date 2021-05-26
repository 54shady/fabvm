#!/usr/bin/env python
# coding=utf-8

from runshellcmd import run_command
import argparse


def activepin(vm, start):
    # 4core vm
    vcpu = (x for x in range(4))
    pcpu = (x for x in range(start, start + 4))
    vp = [x for x in zip(vcpu, pcpu)]
    for v, p in vp:
        cmd = 'virsh vcpupin %s %d %d' % (vm, v, p)
        run_command(cmd)


def deactivepin(vm):
    for v in range(4):
        cmd = 'virsh vcpupin %s %d 0-127' % (vm, v)
        run_command(cmd)


def main():
    parser = argparse.ArgumentParser(description="vcpu pin script")
    parser.add_argument("-n", "--name", type=str,
                        default="demo-1", help="vm name")
    parser.add_argument(
        "--pin", help="pin to physical core", action="store_true")
    parser.add_argument("--start", type=int, default=5, help="Pcore Start")
    parser.add_argument("--depin", help="unpin to physical core",
                        action="store_true")
    iargs = parser.parse_args()
    vm = iargs.name
    pstart = iargs.start
    if iargs.pin:
        activepin(vm, pstart)
    if iargs.depin:
        deactivepin(vm)


if __name__ == '__main__':
    main()
