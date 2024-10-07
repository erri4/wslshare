import subprocess

def get_gw():
    ipconfig = subprocess.run(['ipconfig'], shell=True, capture_output=True)
    ipconfig = str(ipconfig.stdout.decode())

    substr = 'Default Gateway . . . . . . . . . : '
    find = ipconfig.find(substr)
    start = find + len(substr)
    end = start + len('fff.fff.fff.fff')
    r1 = ipconfig[start:end].strip().split('.')
    li = r1[-1]
    n = False
    while not n:
        n = isnumber(li)
        if n:
            break
        li = li[:len(li) - 2].strip()
    r1[-1] = li
    return '.'.join(r1)


def get_ip():
    ipconfig = subprocess.run(['ipconfig'], shell=True, capture_output=True)
    ipconfig = str(ipconfig.stdout.decode())

    substr = 'IPv4 Address. . . . . . . . . . . : '
    find = ipconfig.find(substr)
    start = find + len(substr)
    end = start + len('fff.fff.fff.fff')
    r1 = ipconfig[start:end].strip().split('.')
    li = r1[-1]
    n = False
    while not n:
        n = isnumber(li)
        if n:
            break
        li = li[:len(li) - 2].strip()
    r1[-1] = li
    return '.'.join(r1)
        

def isnumber(value):
    if type(value) == int:
        return bool(1)
    if type(value) != str:
        return bool(0)
    if value == '':
        return bool(0)
    rt = list(value)
    if rt[0] == "-" and not value == "-":
        for i in range(1, len(rt)):
            if not rt[i] == "0" and not rt[i] == "1" and not rt[i] == "2" and not rt[i] == "3" and not rt[i] == "4" and not \
                    rt[
                        i] == "5" and not \
                    rt[i] == "6" and not rt[i] == "7" and not rt[i] == "8" and not rt[i] == "9":
                return bool(0)
    else:
        for i in range(0, len(rt)):
            if not rt[i] == "0" and not rt[i] == "1" and not rt[i] == "2" and not rt[i] == "3" and not rt[i] == "4" and not \
                    rt[
                        i] == "5" and not \
                    rt[i] == "6" and not rt[i] == "7" and not rt[i] == "8" and not rt[i] == "9":
                return bool(0)
    return bool(1)
