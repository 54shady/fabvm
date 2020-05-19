#!/usr/bin/env python
# coding=utf-8

import threading
import time
import random
import paramiko
import argparse

def remote_test_routine(arg, lock):
    ipaddr = "172.28.107.%d" % (110 + arg)
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(hostname=ipaddr, username="root",password="0")
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print("NoValidConnectionsError : " + ipaddr)
    else:
        order = '/root/lmbench3/bin/arm-linux/stream'
        stdin,stdout,stderr=s.exec_command(order)
        result = stderr.read()
        lock.acquire()
        print("===Testing %s Start===" % ipaddr)
        for i in range(0, len(result.splitlines())):
            print(result.splitlines()[i])
        print("===Testing %s End===\n" % ipaddr)
        lock.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Remote Test")
    parser.add_argument("-t", "--thread", type=int,
                        help="numbers of threads")

    mutex = threading.Lock()

    args = parser.parse_args()
    for i in range(args.thread):
        t = threading.Thread(target=remote_test_routine, args=(i+1, mutex,))
        t.start()
