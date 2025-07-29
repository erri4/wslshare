from flask import Flask, Response, request

app = Flask(__name__)

server_queue = []
client_queue = []

@app.route('/server/send', methods=['POST'])
def serversend():
    data = request.get_json()
    client_queue.append(data)
    if server_queue:
        server_queue.pop()
    return ''

@app.route('/server/recv', methods=['POST'])
def serverrecv():
    if not server_queue:
        return Response(status=204)
    return server_queue[-1]

@app.route('/client/send', methods=['POST'])
def clientsend():
    data = request.get_json()
    server_queue.append(data)
    return ''

@app.route('/client/recv', methods=['POST'])
def clientrecv():
    if not client_queue:
        return Response(status=204)
    return client_queue.pop()

@app.route('/bye', methods=['POST'])
def bye():
    global server_queue, client_queue
    server_queue = []
    client_queue = []
    return ''
