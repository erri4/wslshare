import subprocess
from scapy.all import *
from collections import namedtuple

Ans = namedtuple('Answer', 'ip mac')


def get_gw():
    ipconfig = subprocess.run(['ipconfig'], shell=True, capture_output=True)
    ipconfig = str(ipconfig.stdout.decode())

    substr = 'Default Gateway . . . . . . . . . : '
    i = 0
    r1 = []
    r2 = []
    while i < len(ipconfig) - len(substr):
        find = ipconfig.find(substr, i)
        if find != -1:
            r1.append(find)
            i = find + 1
        else:
            i += 1

    for f in r1:
        start = f + len(substr)
        end = start + 11
        r2.append(ipconfig[start:end])

    for d in r2:
        ls = d.split('.')
        if len(ls) >= 3:
            rls = [ls[0], ls[1], ls[2]]
            return '.'.join(rls)


def isnumber(value):
    if type(value) == int:
        return bool(1)
    if type(value) != str:
        return bool(0)
    if value == '':
        return bool(0)
    rt = list(value)
    if rt[0] == "-" and not value == "-":
        for i in range(1, len(rt)):
            if not rt[i] == "0" and not rt[i] == "1" and not rt[i] == "2" and not rt[i] == "3" and not rt[i] == "4" and not \
                    rt[
                        i] == "5" and not \
                    rt[i] == "6" and not rt[i] == "7" and not rt[i] == "8" and not rt[i] == "9":
                return bool(0)
    else:
        for i in range(0, len(rt)):
            if not rt[i] == "0" and not rt[i] == "1" and not rt[i] == "2" and not rt[i] == "3" and not rt[i] == "4" and not \
                    rt[
                        i] == "5" and not \
                    rt[i] == "6" and not rt[i] == "7" and not rt[i] == "8" and not rt[i] == "9":
                return bool(0)
    return bool(1)


def arp_scan(ip):
    req = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip)
    ans, _ = srp(req, timeout=0.5, retry=1)
    r = []
    for _, packet in ans:
        r.append(Ans(packet.psrc, packet.hwsrc))
    return r

def main():
    val_ip = False
    while not val_ip:
        i = input('ip:')
        il = i.split('.')
        if len(il) == 3:
            if isnumber(il[0]) and isnumber(il[1]) and isnumber(il[2]):
                val_ip = True
            else:
                print(f'{i} is not a valid ip')
        elif i.lower() == 'default gateway' or i.lower() == 'default gy':
            i = get_gw()
            print(f'default gateway is {i}')
            val_ip = True
        else:
            print(f'{i} is not a valid ip')
    all_ans = []
    print("starting")
    for crnt_ip in range(225):
        arp = arp_scan(f'{i}.{crnt_ip}')
        if arp != []:
            all_ans.append(arp)
    print('scan finished')
    for answer in all_ans:
        if answer != []:
            for packet in answer:
                print(f'ip: {packet.ip}, mac: {packet.mac}')
    if all_ans == []:
        print('There is no devices connected on this ip.')


if __name__ == '__main__':
    main()
