#!/usr/bin/env python
# coding=utf-8

import sys
from net_util import *


def main(tap, br, gw, network, dhcprange, mask="255.255.255.0"):
    cmds = [
        "iptables -t nat -D POSTROUTING -s %s/%s -j MASQUERADE" % (
            network, mask),
        "iptables -t filter -D INPUT -i %s -p tcp -m tcp --dport 67 -j ACCEPT" % br,
        "iptables -t filter -D INPUT -i %s -p udp -m udp --dport 67 -j ACCEPT" % br,
        "iptables -t filter -D INPUT -i %s -p tcp -m tcp --dport 53 -j ACCEPT" % br,
        "iptables -t filter -D INPUT -i %s -p udp -m udp --dport 53 -j ACCEPT" % br,
        "iptables -t filter -D FORWARD -i %s -o %s -j ACCEPT" % (br, br),
        "iptables -t filter -D FORWARD -s %s/%s -i %s -j ACCEPT" % (
            network, mask, br),
        "iptables -t filter -D FORWARD -d %s/%s -o %s -m state --state RELATED,ESTABLISHED -j ACCEPT" % (
            network, mask, br),
        "iptables -t filter -D FORWARD -o %s -j REJECT --reject-with icmp-port-unreachable" % br,
        "iptables -t filter -D FORWARD -i %s -j REJECT --reject-with icmp-port-unreachable" % br,
        "ifconfig %s down" % tap,
        "brctl delif %s %s" % (br, tap),
    ]
    run_cmdlist(cmds)

    cmds = [
        "ifconfig %s down" % br,
        "brctl delbr %s" % br
    ]
    run_cmdlist(cmds)

    nr_br = run_command('brctl show | grep natbr | wc -l')
    if int(nr_br) == 0:
        run_command('pkill dnsmasq')
    else:
        pid = get_pid('dnsmasq')
        with open('/proc/%s/cmdline' % pid[0]) as f:
            ret = f.read().replace('\0', ' ')
        lret = list(ret.strip('\n').split(' '))
        run_command('pkill dnsmasq')
        lret.remove("--interface=%s" % br)
        lret.remove("--listen-address=%s" % gw)
        lret.remove("--dhcp-range=%s" % dhcprange)
        run_command(' '.join(lret))


def find_vir_br(tap):
    ''' findout which bridge the tap device on '''
    ret = run_command('brctl show | grep %s' % tap)
    lret = list(ret.strip('\n').split('\n'))
    for line in lret:
        lline = list(line.split('\t'))
        if len(lline) == 6:
            return lline[0]


def find_vir_aa(br):
    ''' findout the bridge IP aa.bb.cc.dd '''
    ret = run_command('ip -4 -br ad')
    sret = str(ret)
    lret = sret.strip('\n').split('\n')
    for i in range(len(lret)):
        ifname = lret[i].split()[0]
        aa = lret[i].split()[2].split('/')[0].split('.')[0]
        if ifname == br:
            return aa


if __name__ == '__main__':
    br = find_vir_br(sys.argv[1])
    aa = find_vir_aa(br)
    gw = "%s.168.53.1" % aa
    network = "%s.168.53.0" % aa
    dhcprange = "%s.168.53.100,%s.168.53.254" % (aa, aa)
    main(sys.argv[1], br, gw, network, dhcprange)
