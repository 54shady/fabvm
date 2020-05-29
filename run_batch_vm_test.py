#!/usr/bin/env python
# coding=utf-8

import threading
import time
import random
import paramiko
import argparse

def remote_test_routine(arg, lock, cmd):
    ipaddr = "172.28.107.%d" % (130 + arg)
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(hostname=ipaddr, username="root",password="0")
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print("NoValidConnectionsError : " + ipaddr)
    else:
        stdin,stdout,stderr=s.exec_command(cmd)
        result = stdout.read().decode()
        lres[arg] = result


if __name__ == '__main__':
    # insert each thread result into a list
    lres = []

    # default max thread maybe 50?
    for i in range(0, 50):
        lres.append(0)

    parser = argparse.ArgumentParser(description="Run Remote Test")

    # default one thread
    parser.add_argument("-t", "--thread", type=int,default=1,
                        help="numbers of threads")

    # the actual command for remote machine
    parser.add_argument("-c", "--command", type=str,required=True,
                        help='''Test command, -c 'ls -l' ''')

    mutex = threading.Lock()

    args = parser.parse_args()
    lthreads = []
    for i in range(args.thread):
        t = threading.Thread(target=remote_test_routine,
                args=(i+1, mutex, args.command))
        lthreads.append(t)
        t.start()

    for t in lthreads:
        t.join()

    print("===lrest start===")
    for i in range(0, len(lres)):
        if lres[i] != 0:
            for j in range(0, len(lres[i].splitlines())):
                print("line%d" % j, "%2d" % i, lres[i].splitlines()[j])
    print("===lrest end===")
