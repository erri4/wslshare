import requests
import json
import threading
import base64
import os


SERVER_IP = 'http://127.0.0.1:5000'

cd: str = ''
lastest = None
terminate = False
proceed = True
send_t: threading.Thread = None


def recv():
    global cd, lastest, proceed
    resp = requests.post(SERVER_IP + '/client/recv', timeout=10).text
    cd = 'PS ' + json.loads(resp)['output'] + '>'
    while not terminate:
        try:
            resp = requests.post(SERVER_IP + '/client/recv', timeout=10).text
            cd = 'PS ' + json.loads(resp)['cwd'] + '>'
            lastest = json.loads(resp)['output'] if json.loads(resp)['output'] is not None else '\033[31m' + str(json.loads(resp)['error']) + '\033[0m'
        except requests.exceptions.ReadTimeout:
            continue


def send():
    global lastest, terminate, proceed
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
                requests.post(SERVER_IP + '/client/send', json=json.dumps({
                    'command': 'upload',
                    'filename': filename,
                    'filedata': file_data
                }))
            except Exception as e:
                print(f"\033[31mUpload failed: {e}\033[0m")
                proceed = True
                continue

            proceed = False
            continue
        
        requests.post(SERVER_IP + '/client/send', json=json.dumps({'command': cmd}))
        proceed = False
    terminate = True


def main():
    global send_t, terminate
    requests.post(SERVER_IP + '/client/send', json=json.dumps({'command': 'cd'})).text
    recv_t = threading.Thread(target=recv)
    recv_t.start()
    while not terminate:
        send_t = threading.Thread(target=send)
        send_t.start()
        send_t.join()


if __name__ == '__main__':
    main()