from scapy.all import *
from collections import namedtuple
from pypackage.functions import isnumber


TCPport = namedtuple('TCPport', 'port')


def tcp_scan(ip, port):
    try:
        syn = IP(dst=ip) / TCP(dport=port, flags='S')
    except socket.gaierror:
        raise Exception(f'couldn\'t resolve {ip}')
    ans, _ = sr(syn, timeout=0.5, retry=1)
    r = []
    for _, packet in ans:
        if packet[TCP].flags == 'SA':
            r.append(TCPport(packet[TCP].sport))
    return r


def main():
    ports_to_scan = []
    ip = input('ip: ')
    while ports_to_scan == []:
        i = input('ports: ')
        ls1 = i.split(', ')
        for port in ls1:
            if isnumber(port) == True:
                ports_to_scan.append(int(port))
        if ports_to_scan == []:
            ls2 = i.split(',')
            for port in ls2:
                if isnumber(port) == True:
                    ports_to_scan.append(int(port))
            if ports_to_scan == []:
                print('give at least one valid port number')
    all_rs = []
    for port in ports_to_scan:
        rs = tcp_scan(ip, port)
        if rs != []:
            for r in rs:
                all_rs.append(f'port {r.port} is open')
        else:
            all_rs.append(f'port {port} is closed')
    for res in all_rs:
        print(res)


if __name__ == '__main__':
    main()
