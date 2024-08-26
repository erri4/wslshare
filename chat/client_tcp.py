#! /usr/bin/env python3

import json
import sys
import socket
import select

from protocol import server_addr, pro_rd_msg, pro_wr_msg

def main():

    client = socket.socket()
    client.connect(server_addr)

    to_rd = [client, sys.stdin]
    finished = False
    print('name:')
    s = '\n'
    while not finished:
        rdables, _, _ = select.select(to_rd, [], [], 0.1)
        for rdable in rdables:
            if rdable == client:
                from_server = pro_rd_msg(client)
                if from_server == b'':
                    finished = True
                else:
                    from_server = from_server.decode()
                    from_server = json.loads(from_server)
                    if type(from_server) == list:
                        print(f'{from_server[1]}: {from_server[0]}')
                    else:
                        print(f'{from_server}')
            else:
                msg = rdable.readline().strip()
                if s:
                    print(s)
                    s = False
                if msg != '':
                    pro_wr_msg(client, msg.encode())
                if msg == b'exit':
                    finished = True
        
    client.shutdown(socket.SHUT_RDWR)
    client.close()

if __name__ == '__main__':
    main()