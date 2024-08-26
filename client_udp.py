#! /usr/bin/env python3

import socket

src_addr = ('127.0.0.1', 7331)  
server_addr = ('127.0.0.1', 1337)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(src_addr)
    s.sendto(b'pwd', server_addr)
    pwd, addr = s.recvfrom(1024)
    s.sendto(b'whoami', server_addr)
    username, addr = s.recvfrom(1024)
    s.sendto(b'hostname', server_addr)
    hostname, addr = s.recvfrom(1024)
    while True:
        i = input(f'\033[92m{username.decode().strip()}@{hostname.decode().strip()}\033[00m:\033[94m{pwd.decode().strip()}\033[00m$')
        s.sendto(i.encode(), server_addr)
        if i == 'exit':
            break
        msg, addr = s.recvfrom(1024)
        print(f'{msg.decode()}')

    s.close()

if __name__ == '__main__':
    main()