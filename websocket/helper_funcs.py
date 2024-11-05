import database as db


users = []
rooms = []
HOST = 'localhost'
USER = 'root'
PASSWORD = '033850900reefmysql'
DATABASE = 'mysqldb'
PORT = 3300
pool = db.ConnectionPool(HOST, USER, PASSWORD, DATABASE, PORT)


def getcliby(attr: str, con) -> int | bool:
    global users
    for i in range(len(users)):
        if getattr(users[i], attr) == con:
            return i
    return False


def getroomby(attr: str, con) -> int | bool:
    global rooms
    for i in range(len(rooms)):
        if getattr(rooms[i], attr) == con:
            return i
    return False


def get_rooms() -> list:
    global rooms
    r = []
    for rm in rooms:
        r.append(rm.name)
    return r


def login(name: str, p) -> bool | str:
    sql = f"select pass from users where username='{name}'"
    with pool.select(sql) as s:
        if s.rowcount == 1:
            pa = s.sqlres[0]['pass']
            if pa == p:
                return True
            return 'incorrect password'
        return 'user does not exist'


def addname(name: str, passw) -> bool:
    sql = f"select username from users where username='{name}'"
    with pool.select(sql) as s:
        if not s.rowcount > 0:
            sql = f"insert into users (username, pass, xp) values ('{name}', '{passw}', 0)"
            pool.runsql(sql)
            return True
        return False
    

def sendrooms(clobj, server):
    global rooms
    roms = []
    for rm in list(get_rooms()):
        room = getroomby('name', rm)
        finroom = []
        for part in rooms[room].participants:
            if part.name in clobj.friends:
                finroom.append(part.name)
        roms.append([rm, finroom])
    clobj.send(server, roms, 'rooms')
