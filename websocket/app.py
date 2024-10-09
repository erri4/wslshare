from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from ws import start_server
import sys
sys.path.insert(1, '/Users/Reef/Documents/WSLShare')
from func import get_ip


def refresh():

    with open('names.json', 'w') as file:
        json.dump([], file)

            
    with open('static/ip.txt', 'w') as file:
        file.write(f'{get_ip()}')

ip = ''
with open('static/ip.txt', encoding='utf8') as file_object:
    ip = file_object.read()

app = Flask(__name__)


@app.route('/server', methods=['GET', 'POST'])
def ajax():
    if request.method == "POST":
        with open('names.json', 'r') as file:
            names = json.load(file)
        name = request.form['name']
        if name in names:
            return jsonify(False)
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


def runapp(ip):
    app.run(host=f'{ip}', port=5000)

if __name__ == '__main__':
    refresh()
    start_server(ip)
    runapp(ip)

