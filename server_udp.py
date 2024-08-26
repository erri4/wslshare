#!/usr/bin/env python3
 
import socket
import subprocess

src_addr = ('127.0.0.1', 1337)
 
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(src_addr)
    print('Server is up')
    while True:
        msg, addr = s.recvfrom(1024)
        if msg == b'exit':
            break
        output = ''
        try:
            output = subprocess.check_output(msg, shell=True)
            print(f'command: {msg.decode()}\n\n output: {output.decode()}')
        except subprocess.CalledProcessError:
            print(f'command {msg.decode()} is not found')
            output = f'/bin/sh: 1: {msg.decode()}: not found\ncommand {msg.decode()} is not found\n\n'.encode()
        except:
            print('something else went wrong')
            output = b'something else went wrong'
        finally:
            s.sendto(output, addr)

    s.close()
    print('Server is down')
 
if __name__ == '__main__':
    main()