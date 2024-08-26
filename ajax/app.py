import asyncio
import websockets
async def handler(websocket, path):
    print(path)
    data = await websocket.recv()
    print(f'msg: {data}, src: {path}')
    reply = f"Data recieved as:  {data}!"
    await websocket.send(reply)

start_server = websockets.serve(handler, "127.0.0.1", 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#############################################################
'''from flask import Flask, jsonify, render_template, request, redirect, url_for
import socket
import select
from protocol import server_addr, pro_rd_msg, pro_wr_msg

app = Flask(__name__)


server = socket.socket()
server.bind(server_addr)
server.listen(5)
rd = [server]

while True:
        rdables, _, _ = select.select(rd, [], [], 0.1)
        for rdable in rdables:
            if rdable == server:
                conn, addr = server.accept()
                print('connected!')
                rd.append(conn)
                pro_wr_msg(conn, b'hi!')
            else:
                msg = pro_rd_msg(rdable)
                if msg != b'':
                    print(msg.decode())'''
###################################################
'''@app.route('/server', methods=['GET', 'POST'])
def ajax():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        output = firstname + ' ' + lastname
        if firstname and lastname:
            return jsonify({'output': 'Your Name is ' + output + ', right?'})
        return jsonify({'error': 'Missing data!'})
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<custom_page>')
def custom_page_func(custom_page):
    return render_template('page_not_found.html', custom_page=custom_page), 404'''
