from functions import get_gw
import socket
import json
import os
from pathlib import Path

server_port = 9000
handshake_msg = b"HELLO_SERVER\n"
cache_file = Path(".server_ip")


def verify_server(ip):
    try:
        with socket.create_connection((ip, server_port), timeout=2) as sock:
            greeting = sock.recv(64)
            if greeting.strip() == handshake_msg.strip():
                return True
    except:
        pass
    return False


def save_server_ip(ip):
    cache_file.write_text(ip)


def load_cached_ip():
    if cache_file.exists():
        ip = cache_file.read_text().strip()
        if verify_server(ip):
            print(f"[+] Using cached server IP: {ip}")
            return ip
        else:
            print("[-] Cached IP invalid or server not responding.")
    return None


def discover_server_ip():
    print("[*] Scanning local network for server...")
    gw = get_gw()
    base_ip = '.'.join(gw.split('.')[:-1])
    for i in range(1, 255):  # skip .0 (network) and .255 (broadcast)
        subnet = f"{base_ip}.{i}"
        if verify_server(subnet):
            print(f"[+] Server found at {subnet}")
            save_server_ip(subnet)
            return subnet
    raise Exception("[-] No server found on network.")


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


def upload_file(conn, filepath):
    if not os.path.isfile(filepath):
        print("File not found.")
        return

    size = os.path.getsize(filepath)
    filename = os.path.basename(filepath)
    header = {
        "action": "upload",
        "filename": filename,
        "size": size
    }

    send_msg(conn, header)

    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            conn.sendall(chunk)

    resp = recv_msg(conn)
    print(resp.get("output", "[No response]"))


def main():
    server_ip = load_cached_ip()
    if not server_ip:
        server_ip = discover_server_ip()

    conn = socket.create_connection((server_ip, server_port))
    conn.recv(64)  # consume handshake

    send_msg(conn, "cd")
    response = recv_msg(conn)
    cwd = response.get("cwd", os.getcwd())

    try:
        while True:
            command = input(f"PS {cwd}> ").strip()

            if command.startswith("upload "):
                filepath = command[7:].strip()
                upload_file(conn, filepath)
                continue

            send_msg(conn, command)

            if command == "exit":
                break

            response = recv_msg(conn)
            if 'cwd' in response:
                cwd = response['cwd']
            elif 'output' in response:
                print(response['output'].strip())

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        print("[-] Disconnected from server.")


if __name__ == '__main__':
    main()
