import socket
import json

server_addr = ('127.0.0.1', 1337)

def send_msg(soc, msg):
    data = json.dumps(msg).encode()
    length = len(data).to_bytes(4, byteorder='big')
    soc.sendall(length + data)

def recv_msg(soc):
    length = int.from_bytes(soc.recv(4), byteorder='big')
    data = b''
    while len(data) < length:
        more = soc.recv(length - len(data))
        if not more:
            raise ConnectionError("Server disconnected")
        data += more
    return json.loads(data.decode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_addr)
        send_msg(s, 'cd')
        path_loc = recv_msg(s).get('cwd', '')

        while True:
            i = input(f'PS {path_loc.strip()}>')
            send_msg(s, i)
            if i == 'exit':
                break
            msg = recv_msg(s)
            if 'output' in msg:
                print(msg['output'].strip())
            elif 'cwd' in msg:
                path_loc = msg['cwd']

if __name__ == '__main__':
    main()
