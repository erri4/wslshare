VIRUS_HASH = 'THIS IS A PLACE HOLDER'
from os import system
from hashlib import sha256
from psutil import NoSuchProcess, AccessDenied, ZombieProcess, process_iter
from threading import Thread


def findthevirus():
    def get_file_hash(filepath):
        try:
            with open(filepath, "rb") as f:
                hasher = sha256()
                while chunk := f.read(4096):
                    hasher.update(chunk)
                return hasher.hexdigest()
        except Exception:
            return None

    hash_to_process = {}

    for process in process_iter(['pid', 'name', 'exe']):
        try:
            exe_path = process.info['exe']
            if exe_path:
                file_hash = get_file_hash(exe_path)
                if file_hash:
                    process_name = process.info['name'].replace('.exe', '')
                    if file_hash in hash_to_process:
                        hash_to_process[file_hash].add(process_name)
                    else:
                        hash_to_process[file_hash] = {process_name}
        except (NoSuchProcess, AccessDenied, ZombieProcess):
            pass

    for file_hash, process_names in hash_to_process.items():
        if file_hash == VIRUS_HASH:
            return list(process_names)
    return []

def kill_v(v):
    system(f'taskkill /f /im {v}.exe')

if __name__ == '__main__':
    print('Starting to look for the virus...')

    virus_processes = findthevirus()
    print(f'Virus found under the names {virus_processes}. Killing it...')

    for vname in virus_processes:
        t1 = Thread(target=kill_v, args=(vname,))
        t1.start()
        t1.join()