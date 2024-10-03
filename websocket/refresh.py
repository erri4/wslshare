import subprocess
import json

with open('websocket/names.json', 'w') as file:
    json.dump([], file)

def get_ip():
    ipconfig = subprocess.run(['ipconfig'], shell=True, capture_output=True)
    ipconfig = str(ipconfig.stdout.decode())

    substr = 'IPv4 Address. . . . . . . . . . . : 192.168.68'

    find = ipconfig.find(substr)
    start = find + 47
    end = start + 3
    return f'192.168.68.{ipconfig[start:end].strip()}'


    
        
with open('websocket/static/ip.txt', 'w') as file:
    file.write(f'{get_ip()}')