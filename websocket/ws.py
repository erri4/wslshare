from websocket_server import WebsocketServer

clients = []
clients_name = []
def new_client(client, server):
    clients.append(client)
    clients_name.append(client['id'], None)
    print(f"New client connected: {client['id']}")


def client_left(client, server):
    cl_name = ''
    for cl in clients_name:
        if cl[0] == client['id']:
            cl_name = cl[1]
    clients_name.remove(client['id'], cl_name)
    clients.remove(client)
    for cl in clients:
        server.send_message(cl, f'{client['id']} have left the room')
    print(f"Client disconnected: {cl_name}")

def message_received(client, server, msg):
    cl_name = ''
    for cl in clients_name:
        if cl[0] == client['id']:
            cl_name = cl[1]
    if cl_name == None:
        clients_name.remove([client['id'], None])
        clients_name.append([client['id'], msg])
        for cl in clients:
            if cl != client:
                server.send_message(cl, f'{cl_name} have joined the room')
    else:
        print(f"{cl_name}: {msg}")
        reply = f"{cl_name}: {msg}"
        for cl in clients:
            if cl != client:
                server.send_message(cl, reply)

def start_server():
    server = WebsocketServer(host='127.0.0.1', port=5001)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    
    print("Server listening on 127.0.0.1:5001")
    server.run_forever()

if __name__ == "__main__":
    start_server()