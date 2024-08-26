from scapy.all import *
from collections import namedtuple


TCPport = namedtuple('TCPport', 'port')


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
    while ports_to_scan == []:
        i = input('ports:')
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
        rs = tcp_scan('192.168.68.1', port)
        if rs != []:
            for r in rs:
                all_rs.append(f'port {r.port} is open')
        else:
            all_rs.append(f'port {port} is closed')
    for res in all_rs:
        print(res)


if __name__ == '__main__':
    main()
