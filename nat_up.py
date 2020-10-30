#!/usr/bin/env python
# coding=utf-8

import sys
from net_util import *
import os


def check_bridge(br):
    cmd = "brctl show | grep ^%s " % br
    bret = run_command(cmd)
    sret = str(bret)
    lret = sret.strip('\n').split('\t')
    return lret[0] == br


def create_bridge(br, gw, mask="255.255.255.0"):
    cmds = [
        "brctl addbr %s" % br,
        "brctl stp %s off" % br,
        "brctl setfd %s 0" % br,
        "ifconfig %s %s netmask %s up" % (br, gw, mask)
    ]
    run_cmdlist(cmds)


def enable_ip_forward():
    cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
    run_command(cmd)


def add_filter_rules(br, network, mask="255.255.255.0"):
    cmds = [
        "iptables -t nat -A POSTROUTING -s %s/%s -j MASQUERADE" % (
            network, mask),
        "iptables -t filter -A INPUT -i %s -p tcp -m tcp --dport 67 -j ACCEPT" % br,
        "iptables -t filter -A INPUT -i %s -p udp -m udp --dport 67 -j ACCEPT" % br,
        "iptables -t filter -A INPUT -i %s -p tcp -m tcp --dport 53 -j ACCEPT" % br,
        "iptables -t filter -A INPUT -i %s -p udp -m udp --dport 53 -j ACCEPT" % br,
        "iptables -t filter -A FORWARD -i %s -o %s -j ACCEPT" % (br, br),
        "iptables -t filter -A FORWARD -s %s/%s -i %s -j ACCEPT" % (
            network, mask, br),
        "iptables -t filter -A FORWARD -d %s/%s -o %s -m state --state RELATED,ESTABLISHED -j ACCEPT" % (
            network, mask, br),
        "iptables -t filter -A FORWARD -o %s -j REJECT --reject-with icmp-port-unreachable" % br,
        "iptables -t filter -A FORWARD -i %s -j REJECT --reject-with icmp-port-unreachable" % br
    ]
    run_cmdlist(cmds)


def start_dnsmasq(br, gw, dhcprange, dual_nat=False):
    ''' only need one dnsmasq '''
    if dual_nat:
        # backup old dnsmasq args
        pid = get_pid('dnsmasq')
        with open('/proc/%s/cmdline' % pid[0]) as f:
            ret = f.read().replace('\0', ' ')
        lret = list(ret.strip('\n').split(' '))

        # kill old dnsmasq
        run_command('pkill dnsmasq')

        # rebuild cmdlline
        lret.append("--interface=%s" % br)
        lret.append("--listen-address=%s" % gw)
        lret.append("--dhcp-range=%s" % dhcprange)

        # relaunch dnsmasq
        run_command(' '.join(lret))
    else:
        cmd = "dnsmasq \
            --strict-order \
            --except-interface=lo \
            --interface=%s \
            --listen-address=%s \
            --bind-interfaces \
            --dhcp-range=%s \
            --pid-file=/var/run/qemu-dnsmasq-nat.pid \
            --dhcp-leasefile=/var/run/qemu-dnsmasq-nat.leases \
            --dhcp-no-override" % (br, gw, dhcprange)
        run_command(cmd)


def config_tap(tap, br):
    cmds = [
        "ifconfig %s 0.0.0.0 up" % tap,
        "brctl addif %s %s" % (br, tap)
    ]
    run_cmdlist(cmds)


def main():
    lbr = []
    br = "natbr%s" % sys.argv[1][-1]
    nr_br = run_command('brctl show | grep natbr | wc -l')
    lret = list(nr_br.strip('\n').split('\n'))
    for line in lret:
        lline = list(line.split('\t'))
        lbr.append(lline[0])

    dual_nat = False
    if int(nr_br) >= 1:
        dual_nat = True

    ret = check_bridge(br)

    aa = get_netcard(dual_nat, lbr)
    gw = "%s.168.53.1" % aa
    network = "%s.168.53.0" % aa
    dhcprange = "%s.168.53.100,%s.168.53.254" % (aa, aa)

    create_bridge(br, gw)
    enable_ip_forward()
    add_filter_rules(br, network)
    start_dnsmasq(br, gw, dhcprange, dual_nat)
    config_tap(sys.argv[1], br)


if __name__ == '__main__':
    main()
