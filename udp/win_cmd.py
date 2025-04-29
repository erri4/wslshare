import json
import socket
import subprocess
import os

src_addr = ('127.0.0.1', 1337)

def rd_msg(soc):
    msg, addr = soc.recvfrom(1024)
    msg = msg.decode()
    return {'msg': msg, 'addr': addr}

def wr_msg(soc, msg, addr):
    soc.sendto(msg.encode(), addr)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(src_addr)
    print('Server is up')

    current_dir = os.getcwd()

    while True:
        msg_addr = rd_msg(s)
        msg: str = msg_addr['msg']
        addr = msg_addr['addr']

        if msg == 'exit':
            break

        if msg.startswith('cd'):
            parts = msg.split(maxsplit=1)
            if len(parts) == 2:
                new_path = os.path.abspath(os.path.join(current_dir, parts[1]))
                if os.path.isdir(new_path):
                    current_dir = new_path
                    wr_msg(s, json.dumps({"cwd": current_dir}), addr)
                else:
                    wr_msg(s, json.dumps({"output": f"cd : Cannot find path '{new_path}' because it does not exist."}), addr)
            else:
                wr_msg(s, json.dumps({"cwd": current_dir}), addr)
            continue

        try:
            result = subprocess.run(msg, shell=True, capture_output=True, cwd=current_dir)
            output = result.stdout.decode()
            error = result.stderr.decode()

            if error:
                wr_msg(s, json.dumps({"output": error}), addr)
            else:
                wr_msg(s, json.dumps({"output": output}), addr)

        except Exception as e:
            wr_msg(s, json.dumps({'output': f"Server error: {str(e)}"}), addr)

    s.close()
    print('Server is down')

if __name__ == '__main__':
    main()