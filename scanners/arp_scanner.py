import time
from scapy.all import Ether, srp, ARP
from collections import namedtuple
from functions import get_gw, isnumber

Ans = namedtuple('Answer', 'ip mac')


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
        if i.lower() == 'default gateway' or i.lower() == 'default gw':
            i = get_gw()
            print(f'default gateway is {i}')
            val_ip = True
            il = i.split('.')
            i = '.'.join([il[0], il[1], il[2]])
        il = i.split('.')
        if len(il) == 3:
            if isnumber(il[0]) and isnumber(il[1]) and isnumber(il[2]):
                val_ip = True
            else:
                print(f'{i} is not a valid ip')
        else:
            print(f'{i} is not a valid ip')
    all_ans = []
    print("starting")
    time.sleep(3)
    for crnt_ip in range(225):
        print(f'starting for {crnt_ip}')
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
