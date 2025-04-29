import json
import socket
import subprocess
import os

host = '127.0.0.1'
port = 1337

def recv_msg(conn):
    length = int.from_bytes(conn.recv(4), byteorder='big')
    data = b''
    while len(data) < length:
        more = conn.recv(length - len(data))
        if not more:
            raise ConnectionError("Client disconnected")
        data += more
    return json.loads(data.decode())

def send_msg(conn, msg):
    data = json.dumps(msg).encode()
    length = len(data).to_bytes(4, byteorder='big')
    conn.sendall(length + data)

def handle_client(conn, addr):
    print(f"[+] Connected to {addr}")
    current_dir = os.getcwd()

    try:
        while True:
            msg = recv_msg(conn)
            if msg == 'exit':
                break

            if msg.startswith('cd'):
                parts = msg.split(maxsplit=1)
                if len(parts) == 2:
                    new_path = os.path.abspath(os.path.join(current_dir, parts[1]))
                    if os.path.isdir(new_path):
                        current_dir = new_path
                        send_msg(conn, {"cwd": current_dir})
                    else:
                        send_msg(conn, {"output": f"cd : Cannot find path '{new_path}' because it does not exist."})
                else:
                    send_msg(conn, {"cwd": current_dir})
                continue

            try:
                result = subprocess.run(msg, shell=True, capture_output=True, cwd=current_dir)
                output = result.stdout.decode()
                error = result.stderr.decode()

                if error:
                    send_msg(conn, {"output": error})
                else:
                    send_msg(conn, {"output": output})

            except Exception as e:
                send_msg(conn, {'output': f"Server error: {str(e)}"})

    except Exception as e:
        print(f"[!] Client error: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected from {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"[*] Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == '__main__':
    main()
