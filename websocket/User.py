import json
    

class User:
    def __init__(self, client):
        self.client = client
        self.id = 0
        self.name = None
        self.room = None
        self.x = 0
        self.y = 0
        self.friends = []


    def move(self, x, y):
        self.x = x
        self.y = y


    def set_name_color(self, name, color):
        self.name = name
        self.color = color

    
    def send(self, server, msg, header):
        if header == None:
            header = 'msg'
        server.send_message(self.client, json.dumps([header, msg]))
