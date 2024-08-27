#! /usr/bin/env python3
import json
import socket
import select

from protocol import server_addr, pro_rd_msg, pro_wr_msg

def main():
    print("server started")
    server = socket.socket()
    server.bind(server_addr)
    server.listen(5)

    clients = [server]
    clients_name = [[server, server_addr]]
    finished = False

    while not finished:
        rdables, _, _ = select.select(clients, [], [], 0.1)
        for rdable in rdables:
            if rdable == server:
                conn, addr = server.accept()
                clients.append(conn)
                clients_name.append([conn, None])
            else:
                msg = pro_rd_msg(rdable)
                cl_addr = ""
                for client in clients_name:
                    if client[0] == rdable:
                        cl_addr = client[1]
                if cl_addr == None:
                    clients_name.remove([rdable, None])
                    clients_name.append([rdable, msg.decode()])
                    for client in clients:
                        if client != conn and client != server:
                            pro_wr_msg(client, json.dumps(f'\033[96m *{msg.decode()} have joined the room* \033[00m').encode())
                    print(f'new client: {msg.decode()}')
                else:
                    if msg == b'' or msg == b'exit':
                        #dead client
                        rdable.shutdown(socket.SHUT_RDWR)
                        rdable.close()
                        clients.remove(rdable)
                        cl = ''
                        for client in clients_name:
                            if client[0] == rdable:
                                cl = client[1]
                                clients_name.remove(client)
                        for client in clients:
                            if client != rdable and client != server:
                                pro_wr_msg(client, json.dumps(f'\033[96m *{cl} have left the room* \033[00m').encode())
                        if cl == 'admin':
                            finished = True
                    if cl_addr == 'admin':
                        if  msg == b'/close':
                            finished = True
                        if msg.decode().split(' ')[0] == '/kick':
                            kc = msg.decode().split(' ')[1]
                            for client in clients_name:
                                if client[1] == kc:
                                    cl = client[0]
                                    clients_name.remove(client)
                            cl.shutdown(socket.SHUT_RDWR)
                            cl.close()
                            clients.remove(cl)
                            for client in clients:
                                if client != cl and client != server:
                                    pro_wr_msg(client, json.dumps(f'\033[96m *{kc} has left the room* \033[00m').encode())
                        else:
                            for client in clients_name:
                                if client[0] == rdable:
                                    msg = json.dumps([msg.decode(), client[1]])
                            for client in clients_name:
                                if client[0] != rdable and client[0] != server and client[1] != None:
                                    pro_wr_msg(client[0], msg.encode())
                    elif msg != b'exit':
                        for client in clients_name:
                            if client[0] == rdable:
                                msg = json.dumps([msg.decode(), client[1]])
                        for client in clients_name:
                            if client[0] != rdable and client[0] != server and client[1] != None:
                                pro_wr_msg(client[0], msg.encode())

    server.shutdown(socket.SHUT_RDWR)
    server.close()
    print("server shutdown")

if __name__ == '__main__':
    main()