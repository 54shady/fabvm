#!/usr/bin/env python
# coding=utf-8

import argparse
from os import system


def nodeIdx():
    '''
    generate a number from [0-3] in order
    01230123
    '''
    i = 0
    a = 0
    while True:
        i += 1
        yield a
        a = i % 4


def clusterIdx():
    '''
    generate number 000011112222...77770000
    '''
    i = 0
    a = 0
    while True:
        i += 1
        for j in range(4):
            yield a
        a = i % 8


def clusterIdx2():
    '''
    012301230123
    '''
    i = 0
    a = 0
    while True:
        i += 1
        yield a
        a = i % 4


def clusterIdx3():
    '''
    45674567
    '''
    i = 0
    a = 4
    while True:
        i += 1
        yield a
        a = 4 + (i % 4)


def processIdx():
    '''
    generate 01230123
    '''
    i = 0
    a = 0
    while True:
        i += 1
        yield a
        a = i % 4


def processIdx2():
    i = 0
    a = 0
    while True:
        i += 1
        for j in range(16):
            yield a
        a = i % 4


def test():
    g = processIdx2()
    for i in range(20):
        print(next(g))

def domain():
    divofs = args.number / 4
    for vm in range(args.number):
        if vm < divofs:
            for vcpu in range(4):
                print("virsh vcpupin demo-%d %d 0-31" % (vm + 1, vcpu))
                system("virsh vcpupin demo-%d %d 0-31" % (vm + 1, vcpu))
            if args.numatune:
                print(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 0))
                system(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 0))
        elif divofs <= vm < divofs * 2:
            for vcpu in range(4):
                print("virsh vcpupin demo-%d %d 32-63" % (vm + 1, vcpu))
                system("virsh vcpupin demo-%d %d 32-63" % (vm + 1, vcpu))
            if args.numatune:
                print(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 1))
                system(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 1))
        elif divofs * 2 <= vm < divofs * 3:
            for vcpu in range(4):
                print("virsh vcpupin demo-%d %d 64-95" % (vm + 1, vcpu))
                system("virsh vcpupin demo-%d %d 64-95" % (vm + 1, vcpu))
            if args.numatune:
                print(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 2))
                system(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 2))
        elif divofs * 3 <= vm < divofs * 4:
            for vcpu in range(4):
                print("virsh vcpupin demo-%d %d 96-127" % (vm + 1, vcpu))
                system("virsh vcpupin demo-%d %d 96-127" % (vm + 1, vcpu))
            if args.numatune:
                print(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 3))
                system(
                    "virsh numatune demo-%d --mode strict --nodeset %d --config"
                    % (vm + 1, 3))
        else:
            print("None")


def deploy(args):
    if args.strategy == "dmean":
        mean()
    elif args.strategy == "dcross":
        cross()
    elif args.strategy == "dtest":
        test()
    elif args.strategy == "domain":
        domain()
    elif args.strategy == "dnull":
        for vm in range(args.number):
            for vcpu in range(4):
                print("virsh vcpupin demo-%d %d 0-127" % (vm + 1, vcpu))
                system("virsh vcpupin demo-%d %d 0-127" % (vm + 1, vcpu))
    else:
        for vm in range(args.number):
            for vcpu in range(4):
                print("virsh vcpupin demo-%d %d 0-127" % (vm + 1, vcpu))
                system("virsh vcpupin demo-%d %d 0-127" % (vm + 1, vcpu))


def cross():
    gnIdx = nodeIdx()
    gcIdx2 = clusterIdx2()
    gcIdx3 = clusterIdx3()
    gpIdx = processIdx2()
    cnt = 1

    for vm in range(args.number):
        nidx = next(gnIdx)
        if args.numatune:
            print(
                "virsh numatune demo-%d --mode strict --nodeset %d --config"
                % (vm + 1, nidx))
            system(
                "virsh numatune demo-%d --mode strict --nodeset %d --config"
                % (vm + 1, nidx))
        for vcpu in range(4):
            cidx = next(gcIdx2)
            pidx = next(gpIdx)
            if cnt > 64:
                cidx = next(gcIdx3)
            cnt += 1
            #print("n:%d, c:%d, p:%d" % (nidx, cidx, pidx))
            cpuIdx = nidx * 32 + cidx * 4 + pidx
            print("virsh vcpupin demo-%d %d %d" % (vm + 1, vcpu, cpuIdx))
            system("virsh vcpupin demo-%d %d %d" % (vm + 1, vcpu, cpuIdx))
        print("\n")


def mean():
    # init node and cluster
    cpu = []
    node1 = []
    node2 = []
    node3 = []
    node4 = []

    for i in range(8):
        node1.append([])
        node2.append([])
        node3.append([])
        node4.append([])

    cpu.append(node1)
    cpu.append(node2)
    cpu.append(node3)
    cpu.append(node4)

    gnIdx = nodeIdx()
    gcIdx = clusterIdx()

    for i in range(args.number):
        nidx = next(gnIdx)
        cidx = next(gcIdx)
        #print("deploy %d ==> node %d cluster %d" % (i, nidx, cidx))
        if args.numatune:
            print("virsh numatune demo-%d --mode strict --nodeset %d --config"
                  % (i + 1, nidx))
            system(
                "virsh numatune demo-%d --mode strict --nodeset %d --config"
                % (i + 1, nidx))
        cpu[nidx][cidx].append(i)

    for i in range(4):  # node
        for j in range(8):  # cluster
            for v in range(len(cpu[i][j])):
                for k in range(4):  # cores per cluster
                    cpuidx = i * 32 + j * 4 + k
                    print("virsh vcpupin demo-%d %d %d" %
                          (cpu[i][j][v] + 1, k, cpuidx))
                    system("virsh vcpupin demo-%d %d %d" %
                           (cpu[i][j][v] + 1, k, cpuidx))
            print('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AutoDeployVCPU")
    parser.add_argument("--strategy", type=str,
                        default="dmean",
                        choices=["dmean", "dnull",
                                 "dcross", "dtest", "domain"],
                        help="vcpu pin strategy")
    parser.add_argument("-n", "--number", type=int, default=40,
                        help="Numbers of VMS")

    parser.add_argument("--numatune", help="Numa bind to local node",
                        action="store_true")

    args = parser.parse_args()
    deploy(args)
