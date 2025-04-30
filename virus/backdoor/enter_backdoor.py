import socket
import json
import os

relay_addr = ('127.0.0.1', 9000)

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
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(relay_addr)
    conn.sendall(b"client\n")
    print("[+] Connected to relay.")

    cwd = os.getcwd()

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
        print("[-] Disconnected from relay.")

if __name__ == '__main__':
    main()
