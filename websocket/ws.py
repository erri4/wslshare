from websocket_server import WebsocketServer
import json
from User import User
import message_handler
from helper_funcs import get_rooms, getcliby, users, rooms


def new_client(client, server):
    cl = User(client)
    users.append(cl)


def client_left(client, server):
    c = getcliby('client', client)
    obj = users[c]
    if obj.room != None:
        room = obj.room
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == room:
                r = i
        rm = rooms[r].remove_participant(users[c])
        users[c].room = None
        if rm == False:
            rooms[r].sysmsg(f'{obj.name} have left the room', server)
            rooms[r].move(server)
            rooms[r].sendall(rooms[r].get_usernames(), server, 'rm_ppl')
        else:
            del rooms[r]
        for cl in users:
            if cl.room == None:
                cl.send(server, list(get_rooms()), 'rooms')
    del users[c]
    print(f'client left: {obj.name}')


def message_received(client, server, msg):
    msg = json.loads(msg)
    header = msg[0]
    msg = msg[1]
    message_handler.message_handler(client, server, msg, header)

def start_server(ip):
    server = WebsocketServer(host=f'{ip}', port=5001)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    
    print(f'Server listening on {ip}:5001')
    server.run_forever(threaded=True)
