#!/usr/bin/env python
# coding=utf-8

import threading
import time
import random
import paramiko
import argparse


def remote_test_routine(index, lock, args):
    ipaddr = "172.28.109.%d" % (100 + index)
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(hostname=ipaddr, username=args.user, password="0")
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print("NoValidConnectionsError : " + ipaddr)
    else:
        # assume the display device is 0
        cmd = "DISPLAY=:0 %s" % args.command
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stderr.read() if args.stderr else stdout.read().decode()
        lres[index] = result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Remote Test")

    # default one thread
    parser.add_argument("-t", "--thread", type=int, default=1,
                        help="numbers of threads")

    parser.add_argument("--line", type=int,
                        help="filter specify the line")

    # the actual command for remote machine
    parser.add_argument("-c", "--command", type=str, required=True,
                        help='''Test command, -c 'ls -l' ''')

    parser.add_argument("--user", type=str, default="root",
                        help="login user name")

    # for mpv test only
    parser.add_argument("--mpv", help="For mpv frame drop test only",
                        action="store_true")

    # for systemd base distro startup time measure
    parser.add_argument("--systemd", help="Systemd Base Distro Startup Time",
                        action="store_true")

    # printout stderr instead of stdout
    parser.add_argument("--stderr",
                        help="Read process command result from stderr",
                        action="store_true")

    mutex = threading.Lock()

    # input args
    iargs = parser.parse_args()

    # insert each thread result into a list
    lres = []
    for i in range(0, iargs.thread + 1):
        lres.append(0)

    lthreads = []
    for i in range(iargs.thread):
        t = threading.Thread(target=remote_test_routine,
                             args=(i+1, mutex, iargs))
        lthreads.append(t)
        t.start()

    for t in lthreads:
        t.join()

    df = 0
    for i in range(1, iargs.thread + 1):
        if iargs.mpv:
            # for mpv drop frame test, only print the last record
            r = lres[i].splitlines()[len(lres[i].splitlines()) - 1]
            try:
                df += int(r.decode().split(' ')[-1])
            except ValueError:
                pass
            print("%02d" % i, r.decode().split(' ')[-1], df)
        elif iargs.systemd:
            # for linux(systemd) boot time aa.bb second
            if len(lres[i].split(' ')) == 15: # less then 60s
                record = "%2d %s" % (i, lres[i].split(' ')[-1][:-4])
            else: # more then 60s
                if lres[i].split(' ')[-2] == '1min':
                    minute = 60.0
                    tmp = float(lres[i].split(' ')[-1][:-4])
                    if tmp >= 60.0: # this means it is micro second
                        second = 0
                    else:
                        second = tmp
                    time = minute + second
                    record = "%02d %2f" % (i, time)
            print(record)
        else:
            if iargs.line:
                print(lres[i].splitlines()[iargs.line])
            else:
                for j in range(0, len(lres[i].splitlines())):
                    print("line%d" % j, "%2d" % i, lres[i].splitlines()[j])

    # calcute the average drop frames
    print(df / iargs.thread) if iargs.mpv else ""
