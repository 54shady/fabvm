#!/usr/bin/env python
# coding=utf-8

import subprocess
import sys


def run_command(cmd, stdin=None, stdout=subprocess.PIPE, stderr=None):
    """ run shell command """
    try:
        p = subprocess.Popen(cmd, shell=True,
                             stdout=stdout, stdin=stdin, stderr=stderr,
                             executable="/bin/bash")
        out, err = p.communicate()
        return out
    except KeyboardInterrupt:
        print('Stop')


def main(resultfile):
    # predefine the line number stub for specify file
    d = {
        'execl': 'line98',
        'dhrystone': 'line96',
        'fc256': 'line100',
        'pipecs': 'line103',
        'pipetp': 'line102',
        'spawn': 'line104',
        'syscall': 'line107',
        'whetstone': 'line97',
        'is': 'line109'
    }

    '''
    the intermediate file will be name as below:
    lineN-KEY-Nvm-k4q2.dat
    line98-execl-20vm-k4q2.dat
    '''
    for k in d:
        sfile = resultfile
        tempfile = '%s-%s-%s-k4q2.dat' % (d[k], k, resultfile.split('-')[0])
        cmd = 'cp %s %s' % (sfile, tempfile)
        run_command(cmd)

        # delete the line we don't care
        cmd = '''sed -i '/%s/!d' %s''' % (d[k], tempfile)
        run_command(cmd)

        # calculate the average value of last column
        cmd = '''awk '{ sum += $NF } END { print sum / NR }' %s''' % tempfile
        r = run_command(cmd)
        cmd = '''sed -i "s/%s/%s/" %s''' % (d[k], r.strip(), tempfile)
        run_command(cmd)

        # dropout the linestub for plt script, final data file name
        tfile = '%s-%s-k4q2.dat' % (k, resultfile.split('-')[0])
        cmd = 'mv %s %s' % (tempfile, tfile)
        run_command(cmd)


'''
raw test file name:
    20vm-run-k4q2.txt
    30vm-run-k4q2.txt
    40vm-run-k4q2.txt
'''
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage %s [N]vm-aa-bb.txt' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1])
