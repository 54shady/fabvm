#!/usr/bin/env python
# coding=utf-8

from runshellcmd import run_command
import argparse


def getallpid():
    return run_command('pgrep qemu').decode().split()


def pid2name(pid):
    # cat /proc/<pid>/cmdline  | tr '\0' '\n' | ag guest=
    # qemu -name guest=vmname ...
    cmd = '''cat /proc/%s/cmdline | tr '\\0' '\\n' | ag guest=''' % pid
    vmname = run_command(cmd)
    return vmname


def pid2vnc(pid):
    cmd = ''' cat /proc/%s/cmdline | tr '\\0' '\\n' | grep vnc -A1 ''' % pid
    return run_command(cmd).decode().split(',')[0][len('-vnc'):].strip().split(':')[1]


def pid2mac(pid):
    cmd = '''cat /proc/%s/cmdline | tr '\\0' '\\n' | ag mac= ''' % pid
    for i in run_command(cmd).decode().split(','):
        if str(i).startswith('mac='):
            return str(i)[len('mac='):].strip()


def mac2ip(mac):
    cmd = '''grep %s /proc/net/arp | awk '{ print $1 }' ''' % mac
    return run_command(cmd).decode().strip()


def queryinfo(vm):
    for pid in getallpid():
        vmname = pid2name(pid)
        vmname = (vmname.decode().split(',')[0])[len('guest='):]
        if vmname.strip() == vm:
            mac = pid2mac(pid)
            ip = mac2ip(mac)
            vncp = pid2vnc(pid)
            return (vm, pid, mac, ip, vncp)
    print("No %s found!!!" % vm)
    return None


def main():
    parser = argparse.ArgumentParser(description="Getvm Info")

    parser.add_argument("-p", "--pid", help="Get pid by vm name",
                        action="store_true")

    parser.add_argument("-m", "--mac", help="Get mac by vm name",
                        action="store_true")

    parser.add_argument("-v", "--vnc", help="Get vnc by vm name",
                        action="store_true")

    parser.add_argument("-i", "--ip", help="Get ip by vm name",
                        action="store_true")

    parser.add_argument("-n", "--name", help="vm name", required=True,
                        type=str)
    # input args
    iargs = parser.parse_args()

    res = queryinfo(iargs.name)
    if res is not None:
        if iargs.pid:
            _, x, _, _, _ = res
            print(x)
        elif iargs.mac:
            _, _, x, _, _ = res
            print(x)
        elif iargs.vnc:
            _, _, _, _, x = res
            print(x)
        elif iargs.ip:
            _, _, _, x, _ = res
            print(x)
        else:  # defaul print all info
            print(res)


if __name__ == '__main__':
    main()
