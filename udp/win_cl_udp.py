#! /usr/bin/env python3

import socket
import json

src_addr = ('127.0.0.1', 7331)  
server_addr = ('127.0.0.1', 1337)


def rd_msg(soc):
    msg, addr = soc.recvfrom(65507)
    msg = json.loads(msg.decode())
    return {'msg': msg, 'addr': addr}
    

def wr_msg(soc, msg):
    soc.sendto(msg.encode(), server_addr)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(src_addr)
    wr_msg(s, 'cd')
    path_loc = rd_msg(s)['msg']['cwd']
    while True:
        i = input(f'PS {path_loc.strip()}>')
        wr_msg(s, i)
        if i == 'exit':
            break
        msg: dict[str, str] = rd_msg(s)['msg']
        if 'output' in msg:
            print(f'{msg['output'].strip()}')
        elif 'cwd' in msg:
            path_loc = msg['cwd']

    s.close()

if __name__ == '__main__':
    main()
