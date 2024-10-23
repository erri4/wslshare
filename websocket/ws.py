from websocket_server import WebsocketServer
import json


users = []
rooms = []


class user:
    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.name = None
        self.room = None
        self.x = 0
        self.y = 0
        self.xp = 0


    def move(self, x, y):
        self.x = x
        self.y = y


    def set_name_color(self, name, color):
        self.name = name
        self.color = color


    def set_room(self, rm):
        self.room = rm


def send(msg, cl, server, header = 'msg'):
    if header == None:
        header = 'msg'
    server.send_message(cl, json.dumps([header, msg]))

    

class rom:
    def __init__(self, name, creator):
        self.name = name
        self.participants = [creator]
    

    def add_participant(self, participant):
        self.participants.append(participant)
        

    def remove_participant(self, participant):
        for part in self.participants:
            if part == participant:
                self.participants.remove(participant)
        if self.participants == []:
            return True
        else:
            return False
    

    def sendmsg(self, msg, frm, server):
        reply = [frm.name, msg, [frm.color[0], frm.color[1], frm.color[2]]]
        self.sendall(reply, server)
    

    def sysmsg(self, msg, server):
        self.sendall(msg, server, 'sys')


    def sendall(self, msg, server, header = 'msg'):
        for cl in self.participants:
            send(msg, cl.client, server, header)


    def get_pos(self):
        r = {}
        for cl in self.participants:
            r[cl.name] = [cl.x, cl.y]
        return r
    

    def move(self, server):
        play = []
        poss = self.get_pos()
        for player in list(poss.keys()):
            for cli in self.participants:
                if cli.name == player:
                    cl_color = cli.color
            play.append([player, [poss[f'{player}'][0], poss[f'{player}'][1]], [cl_color[0], cl_color[1], cl_color[2]]])
        self.sendall(play, server, 'move')
    

    def get_usernames(self):
        r = []
        for cl in self.participants:
            r.append(cl.name)
        return r


def get_cli_obj(client):
    for i in range(len(users)):
        if users[i].client == client:
            return i
    return False


def get_rooms():
    r = []
    for rm in rooms:
        r.append(rm.name)
    return r


def new_client(client, server):
    cl = user(client, client['id'])
    users.append(cl)


def client_left(client, server):
    c = get_cli_obj(client)
    obj = users[c]
    if obj.room != None:
        room = obj.room
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == room:
                r = i
        rm = rooms[r].remove_participant(users[c])
        users[c].set_room(None)
        if rm == False:
            rooms[r].sysmsg(f'{obj.name} have left the room', server)
            rooms[r].move(server)
            rooms[r].sendall(rooms[r].get_usernames(), server, 'rm_ppl')
        else:
            del rooms[r]
        for cl in users:
                if cl.room == None:
                    send(list(get_rooms()), cl.client, server, 'rooms')
    if obj.name != None:
        with open('names.json', 'r') as file:
            names = json.load(file)
        names.remove(users[c].name)
        with open('names.json', 'w') as file:
            json.dump(names, file)
    del users[c]
    print(f'client left: {obj.name}')


def message_received(client, server, msg):
    c = get_cli_obj(client)
    obj = users[c]
    msg = json.loads(msg)
    header = msg[0]
    msg = msg[1]
    if header == 'name':
        users[c].set_name_color(msg[0], msg[1])
        send('name', client, server, 'success')
        send(msg[0], client, server, 'name')
        send(list(get_rooms()), client, server, 'rooms')
        print(f'new client: {msg[0]}')
    elif header == 'create':
        if msg == None:
            msg = f"{obj.name}'s room"
        ex = False
        for rm in rooms:
            if rm.name == msg:
                ex = True
        if ex == False:
            r = rom(msg, obj)
            rooms.append(r)
            users[c].set_room(r)
            send('room', client, server, 'success')
            users[c].set_room(f'{msg}')
            send(msg, client, server, 'rm_name')
            send([obj.name], client, server, 'rm_ppl')
            for cl in users:
                if cl.room == None:
                    send(list(get_rooms()), cl.client, server, 'rooms')
            r.move(server)
            print(f'{obj.name} created room: {msg}')
        else:
            send('room already exist', client, server, 'fail')
    elif header == 'join':
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == msg:
                r = i
        rooms[r].sysmsg(f'{obj.name} have joined the room', server)
        rooms[r].add_participant(users[c])
        rooms[r].move(server)
        send(msg, client, server, 'rm_name')
        send('room', client, server, 'success')
        users[c].set_room(f'{msg}')
        rooms[r].sendall(rooms[r].get_usernames(), server, 'rm_ppl')
        print(f'{obj.name} joined room: {msg}')
    elif header == 'leave':
        room = obj.room
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == room:
                r = i
        rm = rooms[r].remove_participant(users[c])
        users[c].set_room(None)
        if rm == False:
            rooms[r].sysmsg(f'{obj.name} have left the room', server)
            rooms[r].move(server)
            rooms[r].sendall(rooms[r].get_usernames(), server, 'rm_ppl')
        else:
            del rooms[r]
        for cl in users:
                if cl.room == None:
                    send(list(get_rooms()), cl.client, server, 'rooms')
        send('', client, server, 'rm_name')
        send('', client, server, 'rm_ppl')
        print(f'{obj.name} left room: {rooms[r].name}')
    elif header == 'msg':
        room = obj.room
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == room:
                r = i
        rooms[r].sendmsg(msg, users[c], server)
        print(f'{obj.name} send: {msg} in room: {rooms[r].name}')
    elif header == 'move':
        room = obj.room
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == room:
                r = i
        users[c].move(msg[0], msg[1])
        rooms[r].move(server)
    elif header == 'eat':
        room = obj.room
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == room:
                r = i
        for part in rooms[r].participants:
            if msg[0] < int(part.x) + 29 and msg[0] > int(part.x) - 29:
                    if msg[1] < int(part.y) + 29 and msg[1] > int(part.y) - 29:
                        if part.client != client:
                            p = get_cli_obj(part.client)
                            users[c].xp += 10
                            users[p].move(0, 0)
                            send('', part.client, server, 'uate')
                            send(users[c].xp, users[c].client, server, 'xp')
                            rep = [[obj.name, part.name], [[obj.color[0], obj.color[1], obj.color[2]], [part.color[0], part.color[1], part.color[2]]]]
                            rooms[r].sendall(rep, server, 'ate')
                            print(f'{obj.name} ate {part.name}')
        rooms[r].move(server)


def start_server(ip):
    server = WebsocketServer(host=f'{ip}', port=5001)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    
    print(f'Server listening on {ip}:5001')
    server.run_forever(threaded=True)