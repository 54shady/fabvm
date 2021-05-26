#!/usr/bin/env python
# coding=utf-8

from runshellcmd import run_command
import threading
import argparse


def remote_test_routine(index, action):
    cmd = "virsh %s demo-%s" % (action, index)
    if action == "undefine":
        cmd = cmd + " --nvram"
    run_command(cmd)


# the shell command below is in sequential mode
# time for i in `seq 1 60`; do virsh start demo-$i; done

# run python in parallel mode using multi thread instead
# time python burst-virsh.py -n 60 --action=start
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Burst Action For Virsh")

    parser.add_argument("-n", "--number", type=int, default=1,
                        help="Numbers of VMS")

    parser.add_argument("--skip", type=int, default=0,
                        help="Skip the N of previous VMs")

    parser.add_argument("--action", type=str, required=True,
                        choices=["start", "destroy", "undefine", "reset"],
                        help="virsh X")

    # input args
    iargs = parser.parse_args()
    lthreads = []

    for i in range(iargs.skip, iargs.number + iargs.skip):
        t = threading.Thread(target=remote_test_routine,
                             args=(i+1, iargs.action))
        lthreads.append(t)
        t.start()

    for t in lthreads:
        t.join()
