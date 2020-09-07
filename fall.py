import psutil

av = ['192', '193', '194']

def get_netcard():
    used = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if k != 'natbr0':
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    ipsub = item[1].split('.')[0]
                    used.append(ipsub)

    return (list(set(av).difference(set(used))))[0]
