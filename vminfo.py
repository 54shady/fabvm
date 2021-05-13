#!/usr/bin/env python
# coding=utf-8

from subprocess import PIPE, Popen
import sys


def run_command(cmd, stdin=None, stdout=PIPE, stderr=None):
    try:
        p = Popen(cmd, shell=True,
                  stdout=stdout, stdin=stdin, stderr=stderr,
                  executable="/bin/bash")
        out, err = p.communicate()
        return out
    except KeyboardInterrupt:
        print('Stop')


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
    return run_command(cmd).decode().split(',')[0][len('-vnc'):].strip()


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
            return (vm, mac, ip, vncp)


def main():
    print(queryinfo(sys.argv[1]))


if __name__ == '__main__':
    main()
