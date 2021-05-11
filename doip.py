#!/usr/bin/env python
# coding=utf-8

from subprocess import PIPE, Popen

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


def libvirt_getip(doname):
    cmd = 'virsh domifaddr %s' % doname
    ret = run_command(cmd)
    ip = ret.decode().split()[-1]
    return ip[:-3]
