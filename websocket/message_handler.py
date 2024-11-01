from helper_funcs import pool, getcliby, get_rooms, login, addname, users, rooms
from Room import Room


def message_handler(client, server, msg, header):
    global users
    global rooms
    c = getcliby('client', client)
    obj = users[c]
    if header == 'login':
        l = login(msg[0], msg[2])
        if l == True:
            users[c].set_name_color(msg[0], msg[1])
            users[c].send(server, 'name', 'success')
            users[c].send(server, msg[0], 'name')
            users[c].send(server, list(get_rooms()), 'rooms')
            print(f'new client: {msg[0]}')
            sql = f"select id, xp from users where username='{obj.name}'"
            with pool.select(sql) as s:
                xp = s.sqlres[0]['xp']
                users[c].send(server, xp, 'xp')
                users[c].id = s.sqlres[0]['id']
            sql = f"select * from friends where friend={obj.id}"
            with pool.select(sql) as s:
                for row in s.sqlres:
                    id = row['f_of']
                    sql = f"select username from users where id={id}"
                    with pool.select(sql) as se:
                        users[c].friends.append(se.sqlres[0]['username'])
            users[c].send(server, users[c].friends, 'friend')
        else:
            users[c].send(server, l, 'fail')
    if header == 'reg':
        if addname(msg[0], msg[2]):
            users[c].set_name_color(msg[0], msg[1])
            users[c].send(server, 'name', 'success')
            users[c].send(server, msg[0], 'name')
            users[c].send(server, list(get_rooms()), 'rooms')
            print(f'new client: {msg[0]}')
            sql = f"select id, xp from users where username='{obj.name}'"
            with pool.select(sql) as s:
                xp = s.sqlres[0]['xp']
                users[c].send(server, xp, 'xp')
                users[c].id = s.sqlres[0]['id']
        else:
            users[c].send(server, 'username already exists', 'fail')
    elif header == 'create':
        if msg == None:
            msg = f"{obj.name}'s room"
        ex = False
        for rm in rooms:
            if rm.name == msg:
                ex = True
        if ex == False:
            r = Room(msg, obj)
            rooms.append(r)
            users[c].send(server, 'room', 'success')
            users[c].room = f'{msg}'
            users[c].send(server, msg, 'rm_name')
            users[c].send(server, [obj.name], 'rm_ppl')
            for cl in users:
                if cl.room == None:
                    cl.send(server, list(get_rooms()), 'rooms')
            r.move(server)
            print(f'{obj.name} created room: {msg}')
        else:
            users[c].send(server, 'room already exists', 'fail')
    elif header == 'join':
        r = None
        for i in range(len(rooms)):
            if rooms[i].name == msg:
                r = i
        rooms[r].sysmsg(f'{obj.name} have joined the room', server)
        rooms[r].add_participant(users[c])
        rooms[r].move(server)
        users[c].send(server, msg, 'rm_name')
        users[c].send(server, 'room', 'success')
        users[c].room = f'{msg}'
        rooms[r].sendall(rooms[r].get_usernames(), server, 'rm_ppl')
        print(f'{obj.name} joined room: {msg}')
    elif header == 'leave':
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
        users[c].send(server, '', 'rm_name')
        users[c].send(server, '', 'rm_ppl')
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
                            p = getcliby('client', part.client)
                            sql = f"select xp from users where username='{obj.name}'"
                            with pool.select(sql) as s:
                                xp = s.sqlres[0]['xp']
                                xp += 10
                                sql = f"update users set xp={xp} where username='{obj.name}'"
                                pool.runsql(sql)
                            users[p].move(0, 0)
                            part.send(server, '', 'uate')
                            users[c].send(server, xp, 'xp')
                            rep = [[obj.name, part.name], [[obj.color[0], obj.color[1], obj.color[2]], [part.color[0], part.color[1], part.color[2]]]]
                            rooms[r].sendall(rep, server, 'ate')
                            print(f'{obj.name} ate {part.name}')
        rooms[r].move(server)
    elif header == 'del':
        sql = f"delete from friends where friend='{obj.id}' or f_of='{obj.id}'"
        pool.runsql(sql)
        sql = f"delete from users where username='{obj.name}'"
        pool.runsql(sql)
    elif header == 'changep':
        sql = f"update users set pass='{msg}' where username='{obj.name}'"
        pool.runsql(sql)
    elif header == 'addf':
        sql = f"select id from users where username='{msg}'"
        with pool.select(sql) as se:
            if se.rowcount == 1:
                sql = f"select * from friends where friend={obj.id} and f_of={users[getcliby('name', msg)].id}"
                with pool.select(sql) as s:
                    if s.rowcount == 0:
                        sql = f"insert into friends values ({obj.id}, {users[getcliby('name', msg)].id})"
                        pool.runsql(sql)
                        sql = f"select * from friends where friend={obj.id}"
                        with pool.select(sql) as s:
                            for row in s.sqlres:
                                id = row['f_of']
                                sql = f"select username from users where id={id}"
                                with pool.select(sql) as se:
                                    users[c].friends.append(se.sqlres[0]['username'])
                        users[c].send(server, users[c].friends, 'friend')
    elif header == 'remf':
        sql = f"select id from users where username='{msg}'"
        with pool.select(sql) as se:
            if se.rowcount == 1:
                sql = f"select * from friends where friend={obj.id} and f_of={se.sqlres[0]['id']}"
                with pool.select(sql) as s:
                    if s.rowcount > 0:
                        sql = f"delete from friends where friend={obj.id} and f_of={se.sqlres[0]['id']}"
                        pool.runsql(sql)
                        sql = f"select * from friends where friend={obj.id}"
                        with pool.select(sql) as s:
                            for row in s.sqlres:
                                id = row['f_of']
                                sql = f"select username from users where id={id}"
                                with pool.select(sql) as se:
                                    users[c].friends.append(se.sqlres[0]['username'])
                        users[c].send(server, users[c].friends, 'friend')
