import socket
import threading
import os

def handle_forward(src: socket.socket, dst: socket.socket, label):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except OSError as e:
        print(f"[!] {label} error: {e}")
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except:
            pass
        src.close()

def main():
    PORT = int(os.environ.get("PORT", 9000))
    relay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    relay.bind(('0.0.0.0', PORT))
    relay.listen(2)
    print(f"[*] Relay is listening on port {PORT}...")

    client_conn = None
    server_conn = None

    def identify_peer(conn: socket.socket):
        role = conn.recv(16).decode().strip().lower()
        return role

    try:
        while True:
            while not (client_conn and server_conn):
                conn, addr = relay.accept()
                role = identify_peer(conn)
                if role == 'client':
                    client_conn = conn
                    print(f"[+] Client connected from {addr}")
                elif role == 'server':
                    server_conn = conn
                    print(f"[+] Server connected from {addr}")
                else:
                    print(f"[!] Unknown role from {addr}, closing.")
                    conn.close()

            # Start forwarding threads
            threading.Thread(target=handle_forward, args=(client_conn, server_conn, "Client→Server"), daemon=True).start()
            threading.Thread(target=handle_forward, args=(server_conn, client_conn, "Server→Client"), daemon=True).start()

            print("[*] Relay is relaying between client and server...")

            while True:
                if client_conn.fileno() == -1:
                    break
            if client_conn.fileno() == -1:
                client_conn = None
                continue
    except KeyboardInterrupt:
        print("[*] Relay shutting down.")
    finally:
        relay.close()

if __name__ == '__main__':
    main()
