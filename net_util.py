#!/usr/bin/env python
# coding=utf-8

from subprocess import *


av = ['192', '193', '194']

def run_command(cmd, stdin=None, stdout=PIPE, stderr=None):
    try:
        p = Popen(cmd, shell=True,
                  stdout=stdout, stdin=stdin, stderr=stderr,
                  executable="/bin/bash")
        out, err = p.communicate()
        return out
    except KeyboardInterrupt:
        print('Stop')


def run_cmdlist(cmd_list):
    for cmd in cmd_list:
        run_command(cmd)


def get_netcard(dnat, lbr):
    used = []
    ret = run_command('ip -4 -br ad')
    sret = str(ret)
    lret = sret.strip('\n').split('\n')
    for i in range(len(lret)):
        ifname = lret[i].split()[0]
        aa = lret[i].split()[2].split('/')[0].split('.')[0]
        if dnat and ifname != 'lo':
            used.append(aa)
        if not dnat and ifname not in lbr and ifname != 'lo':
            used.append(aa)
    return (list(set(av).difference(set(used))))[0]


def get_pid(name):
    return map(int, check_output(["pidof", name]).split())
