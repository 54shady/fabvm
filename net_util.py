#!/usr/bin/env python
# coding=utf-8

from subprocess import *


def run_command(cmd, stdin=None, stdout=PIPE, stderr=None):
    try:
        p = Popen(cmd, shell=True,
                  stdout=stdout, stdin=stdin, stderr=stderr,
                  executable="/bin/bash")
        out, err = p.communicate()
        return out
    except KeyboardInterrupt:
        print 'Stop'


def run_cmdlist(cmd_list):
    for cmd in cmd_list:
        run_command(cmd)
