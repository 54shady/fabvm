#!/usr/bin/env python
# coding=utf-8

import threading
import time
import random
import paramiko
import argparse

def start_routine_d(arg):
    ipaddr = "172.28.107.11%d" % arg
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=ipaddr, username="root",password="0")
    order = '/root/lmbench3/bin/arm-linux/stream'
    stdin,stdout,stderr=s.exec_command(order)
    result = stderr.read()
    print("===Testing %s Start===" % ipaddr)
    for i in range(0, len(result.splitlines())):
        print(result.splitlines()[i])
    print("===Testing %s End===\n" % ipaddr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Remote Test")
    parser.add_argument("-t", "--thread", type=int,
                        help="numbers of threads")

    args = parser.parse_args()
    for i in range(args.thread):
        t = threading.Thread(target=start_routine_d, args=(i+1,))
        t.start()
