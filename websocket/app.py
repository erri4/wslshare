from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from ws import start_server
import threading
import subprocess

def get_ip():
    ipconfig = subprocess.run(['ipconfig'], shell=True, capture_output=True)
    ipconfig = str(ipconfig.stdout.decode())

    substr = 'IPv4 Address. . . . . . . . . . . : 192.168.68'

    find = ipconfig.find(substr)
    if find == -1:
        return '127.0.0.1'
    start = find + 47
    end = start + 3
    return f'192.168.68.{ipconfig[start:end].strip()}'

def refresh():

    with open('names.json', 'w') as file:
        json.dump([], file)

            
    with open('static/ip.txt', 'w') as file:
        file.write(f'{get_ip()}')

app = Flask(__name__)


@app.route('/server', methods=['GET', 'POST'])
def ajax():
    if request.method == "POST":
        with open('names.json', 'r') as file:
            names = json.load(file)
        name = request.form['name']
        if name in names:
            return jsonify(False)
        with open('names.json', 'r') as file:
            names = json.load(file)
        names.append(name)
        with open('names.json', 'w') as file:
            json.dump(names, file)
        return jsonify(True)
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<custom_page>')
def custom_page_func(custom_page):
    return render_template('page_not_found.html', custom_page=custom_page), 404


def runapp():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    refresh()
    t1 = threading.Thread(target=start_server)
    t2 = threading.Thread(target=runapp)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

