from flask import Flask, request
import json

app = Flask(__name__)

command = str
output = str

server_queue: list[command] = []
client_queue: list[dict[command, output]] = []

@app.route('/server/send', methods=['POST'])
def serversend():
    data = json.dumps(request.get_json())
    client_queue.append(data)
    server_queue.pop()
    return ''


@app.route('/server/recv', methods=['POST'])
def serverrecv():
    while server_queue == []:
        pass
    return server_queue[-1]


@app.route('/client/send', methods=['POST'])
def clientsend():
    data = json.loads(request.get_json())['command']
    server_queue.append(data)
    return ''


@app.route('/client/recv', methods=['POST'])
def clientrecv():
    while client_queue == []:
        pass
    return client_queue.pop()


@app.route('/bye', methods=['POST'])
def bye():
    global server_queue, client_queue
    server_queue = []
    client_queue = []
