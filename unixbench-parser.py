#!/usr/bin/env python
# coding=utf-8

from runshellcmd import run_command
import sys
import argparse


def parser_all(resultfile):
    '''
    the resultfile should be like below as example
    10vm-run-k4q2.txt
    which stand for 10 VMS and kernel version 4.x, qemu version 2.x
    '''
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
        # kernel and qemu version
        kq = resultfile.split('-')[2][0:4]

        # number of virtual machines
        nr_vms = resultfile.split('-')[0]

        tempfile = '%s-%s-%s-%s.dat' % (d[k], k, nr_vms, kq)
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
        tfile = '%s-%s-%s.dat' % (k, nr_vms, kq)
        cmd = 'mv %s %s' % (tempfile, tfile)
        run_command(cmd)


def print_usage(prog):
    usage = 'Usage:\n%s 20vm-run-k4q2.txt \n%s pipecs*k4q2.dat' % (prog, prog)
    print(usage)


'''
raw test file name:
    20vm-run-k4q2.txt
    30vm-run-k4q2.txt
    40vm-run-k4q2.txt
'''
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 2:
        parser_all(sys.argv[1])
    elif argc > 2:
        index = sys.argv[1].split('-')
        kqv = index[2][0:4]
        sidefile = 'side-' + index[0] + '-' + kqv + '.dat'
        lrecord = []
        for i in range(1, len(sys.argv)):
            # get first row of first column, which is the mean value
            cmd = '''awk 'NR == 1 { print $1 }' %s''' % sys.argv[i]
            r = run_command(cmd)
            # make one record
            record = '%s %s' % (sys.argv[i].split('-')[1][:-2], r)
            lrecord.append(record)
        with open(sidefile, "w") as f:
            for i in range(0, len(lrecord)):
                f.write("%s" % lrecord[i])
        cmd = '''sed -i "s/STUB/%s/g" side.plt''' % index[0]
        run_command(cmd)
        cmd = '''sed -i "s/KQV/%s/g" side.plt''' % kqv
        run_command(cmd)
        cmd = 'gnuplot side.plt'
        run_command(cmd)

        # roll back the side.plt the way it used to be
        cmd = '''sed -i "s/%s/STUB/g" side.plt''' % index[0]
        run_command(cmd)
        cmd = '''sed -i "s/%s/KQV/g" side.plt''' % kqv
        run_command(cmd)
    else:
        print_usage(sys.argv[0])
