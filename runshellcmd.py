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
