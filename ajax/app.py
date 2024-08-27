'''import asyncio
import websockets
async def handler(websocket, path):
    print(path)
    data = await websocket.recv()
    print(f'msg: {data}, src: {path}')
    reply = f"Data recieved as:  {data}!"
    await websocket.send(reply)

start_server = websockets.serve(handler, "127.0.0.1", 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()'''
###################################################
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/server', methods=['GET', 'POST'])
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
    return render_template('page_not_found.html', custom_page=custom_page), 404
