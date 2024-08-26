import json
import socket
import subprocess

src_addr = ('127.0.0.1', 1337)


def rd_msg(soc):
    msg, addr = soc.recvfrom(1024)
    msg = msg.decode()
    return {'msg': msg, 'addr': addr}
    

def wr_msg(soc, msg, add):
    soc.sendto(msg.encode(), add)


def cmd_split(cmd):
    splt = cmd.split(' ')
    if splt == [cmd]:
        return splt
    l = []
    for i in range(1, len(splt)):
        l.append(splt[i])
    str2 = ''.join(l)
    str1 = splt[0]
    return [str1, str2]


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(src_addr)
    print('Server is up')
    while True:
        msg_addr = rd_msg(s)
        msg = msg_addr['msg']
        addr = msg_addr['addr']
        splt_cmd = cmd_split(msg)
        if msg == 'exit()':
            break
        output = b''
        err = b''
        try:
            output = subprocess.run(splt_cmd, shell=True, capture_output=True)
            err = str(output.stderr.decode()).encode()
            output = str(output.stdout.decode()).encode()
            print(f'command: {msg}\n\n output: {output.decode()}')
            if err != b'':
                print(f'err: {err.decode()}')
        except subprocess.CalledProcessError:
            print(f'command {msg} is not found')
            output = f'/bin/sh: 1: {msg}: not found\ncommand {msg} is not found\n\n'.encode()
        except:
            print('something else went wrong')
            output = b'something else went wrong'
        finally:
            if err != b'':
                msg = json.dumps(["err: '", err.decode(), "'"])
                wr_msg(s, msg, addr)
            else:
                wr_msg(s, json.dumps(output.decode()), addr)

    s.close()
    print('Server is down')
 
if __name__ == '__main__':
    main()