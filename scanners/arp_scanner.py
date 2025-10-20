import time
from scapy.layers.l2 import Ether, ARP, srp
from collections import namedtuple
import subprocess
import re

NUMBER_RE = re.compile(r"^[+-]?\d+(\.\d+)?$")

Ans = namedtuple('Answer', 'ip mac')
def isnumber(data: str | int | float):
    if type(data) is str:
        return bool(re.match(NUMBER_RE, data))
    return isinstance(data, (int, float))
def get_gw():
    """
    get the default gateway.
    """
    ipconfig = subprocess.run(['ipconfig'], shell=True, capture_output=True)
    ipconfig = str(ipconfig.stdout.decode())

    substr = 'Default Gateway . . . . . . . . . : '
    find = ipconfig.find(substr)
    start = find + len(substr)
    end = start + len('fff.fff.fff.fff')
    r1 = ipconfig[start:end].strip().split('.')
    li = r1[-1]
    n = False
    while not n:
        n = isnumber(li)
        if n:
            break
        li = li[:len(li) - 2].strip()
    r1[-1] = li
    return '.'.join(r1)


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
        print(f'starting for {i}.{crnt_ip}')
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
