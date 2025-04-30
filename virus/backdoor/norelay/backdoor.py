import json
import socket
import subprocess
import os

def recv_msg(conn):
    length_bytes = conn.recv(4)
    if not length_bytes:
        raise ConnectionError("Disconnected")
    length = int.from_bytes(length_bytes, byteorder='big')
    data = b''
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Disconnected during receive")
        data += chunk
    return json.loads(data.decode())

def send_msg(conn, msg):
    encoded = json.dumps(msg).encode()
    length = len(encoded).to_bytes(4, byteorder='big')
    conn.sendall(length + encoded)

def handle_upload(conn, header, current_dir):
    filename = os.path.basename(header['filename'])
    filesize = header['size']
    full_path = os.path.join(current_dir, filename)

    with open(full_path, 'wb') as f:
        remaining = filesize
        while remaining > 0:
            chunk = conn.recv(min(4096, remaining))
            if not chunk:
                raise ConnectionError("Upload interrupted")
            f.write(chunk)
            remaining -= len(chunk)

    send_msg(conn, {"output": f"File '{filename}' uploaded successfully."})

def handle_client(conn):
    conn.sendall(b"HELLO_SERVER\n")
    current_dir = os.getcwd()

    while True:
        try:
            msg = recv_msg(conn)

            if isinstance(msg, dict) and msg.get("action") == "upload":
                handle_upload(conn, msg, current_dir)
                continue

            if msg == "exit":
                print("[*] Client disconnected.")
                break

            if msg.startswith("cd"):
                parts = msg.split(maxsplit=1)
                if len(parts) == 2:
                    new_path = os.path.abspath(os.path.join(current_dir, parts[1]))
                    if os.path.isdir(new_path):
                        current_dir = new_path
                        send_msg(conn, {"cwd": current_dir})
                    else:
                        send_msg(conn, {"output": f"cd: path '{new_path}' not found."})
                else:
                    send_msg(conn, {"cwd": current_dir})
                continue

            result = subprocess.run(msg, shell=True, capture_output=True, cwd=current_dir)
            output = result.stdout.decode()
            error = result.stderr.decode()

            send_msg(conn, {"output": error or output})
        except Exception as e:
            send_msg(conn, {"output": f"Server error: {str(e)}"})
            break

def main():
    host = '0.0.0.0'
    port = 9000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        print(f"[*] Server listening on {host}:{port}...")

        while True:
            conn, addr = s.accept()
            print(f"[+] Connection from {addr}")
            handle_client(conn)
            conn.close()
            print("[*] Waiting for next connection...\n")

if __name__ == '__main__':
    main()
