import subprocess
import math
from random import randint
import socket


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
    return socket.gethostbyname(socket.gethostname())
        

def isnumber(value):
    if type(value) == int:
        return True
    if type(value) != str:
        return False
    if value == '':
        return False
    rt = list(value)
    if rt[0] == "-" and not value == "-":
        for i in range(1, len(rt)):
            if not rt[i] == "0" and not rt[i] == "1" and not rt[i] == "2" and not rt[i] == "3" and not rt[i] == "4" and not \
                    rt[
                        i] == "5" and not \
                    rt[i] == "6" and not rt[i] == "7" and not rt[i] == "8" and not rt[i] == "9":
                return False
    else:
        for i in range(0, len(rt)):
            if not rt[i] == "0" and not rt[i] == "1" and not rt[i] == "2" and not rt[i] == "3" and not rt[i] == "4" and not \
                    rt[
                        i] == "5" and not \
                    rt[i] == "6" and not rt[i] == "7" and not rt[i] == "8" and not rt[i] == "9":
                return False
    return True


def is_zero(value, s=""):
    rt = value.split(s)
    rt = "".join(rt)
    rt = replace_text(rt, "-", "1")
    if isnumber(rt):
        if not int(rt) == 0:
            return False
    return True


def is_even(ns):
    n = int(ns)
    g = list(str(n))
    r = []
    if int(g[-1]) % 2 == 0:
        r.insert(0, True)
        if n == 2:
            r.insert(1, True)
        else:
            r.insert(1, False)
    else:
        r = [False, False]
    return r


def is_prime(nh):
    n = abs(int(nh))
    g = list(str(n))
    if g[-1] == "5":
        return False
    if is_even(n)[1]:
        return True
    if is_even(n)[0]:
        return False
    h = round(math.sqrt(n))
    for u in range(5, h, 2):
        if n % u == 0:
            return False
    return True


def reverse_list(r):
    vvc = []
    if type(r) == list:
        for uy in range(len(r) - 1, -1, -1):
            vvc.insert(len(vvc), r[uy])
    return vvc


def reverse_string(r):
    vvc = ""
    for uy in range(len(r) - 1, -1, -1):
        vvc += r[uy]
    return vvc


def process_text(x, y):
    t = 0
    oo = 0
    x_arr = list(x)
    y_arr = list(y)
    result = []
    while t < len(x_arr) - len(y_arr) + 1:
        while x_arr[t + oo] == y_arr[oo]:
            oo += 1
            if oo == len(y_arr):
                result.insert(len(result), str(t))
                t += oo
                oo *= 0
            if t == len(x_arr):
                break
        t += 1
        oo *= 0
        if t == len(x_arr):
            break
    if len(result) == 0:
        return None
    else:
        return result


def replace_text(x, y, z):
    x_arr = list(x)
    y_arr = list(y)
    t = 0
    of = reverse_list(process_text(x, y))
    oo = 0
    while t < len(of):
        x_arr[int(of[t])] = z
        while oo < len(y_arr) - 1:
            del x_arr[int(of[t]) + 1]
            oo += 1
        t += 1
        oo = 0
    return "".join(x_arr)


def num_sum(x):
    s = x.split(" ")
    p = 0
    del s[-1]
    for f in range(0, len(s)):
        p += int(s[f])
    return p


def num_string(y):
    er = y.split(" ")
    r = "+"
    g = ""
    del er[-1]
    tt = str(r.join(er))
    t = replace_text(tt, "+-", "-")
    t += "="
    return g.join(t)


def sam(z, w):
    u = ""
    t = u.join(str(z)) + str(w)
    return t


def random_string(x, y, z=""):
    x_arr = list(x)
    p = []
    v = []
    t = 0
    i = ""
    h = ", "
    if y == "true":
        while t < len(x_arr):
            ran = randint(0, len(x_arr))
            p.insert(ran, x_arr[t])
            v.insert(len(v), str(ran))
            t += 1
        return i.join(p), h.join(v)
    elif y == "false":
        tz = z.split(", ")
        zz = reverse_list(tz)
        while t < len(zz):
            if int(zz[t]) < len(x_arr):
                p.insert(len(p), x_arr[int(zz[t])])
                del x_arr[int(zz[t])]
            else:
                p.insert(len(p), x_arr[-1])
                del x_arr[-1]
            t += 1
        return i.join(reverse_list(p)), ""


def list_key(x, y, z):
    x_arr = list(x)
    y_arr = list(y)
    t = 0
    r = ""
    if not len(x_arr) == len(y_arr):
        if len(y_arr) < len(x_arr):
            while len(y_arr) < len(x_arr):
                y_arr.insert(len(y_arr), str(y))
                e = r.join(y_arr)
                y_arr = list(e)
        while len(y_arr) > len(x_arr):
            del y_arr[-1]
    if z == "true":
        while t < len(x_arr):
            y_arr[t] = ord(y_arr[t])
            x_arr[t] = ord(x_arr[t])
            x_arr[t] = int(x_arr[t]) + int(y_arr[t])
            x_arr[t] = chr(x_arr[t])
            t += 1
        return r.join(x_arr)
    else:
        while t < len(x_arr):
            y_arr[t] = ord(y_arr[t])
            x_arr[t] = ord(x_arr[t])
            x_arr[t] = int(x_arr[t]) - int(y_arr[t])
            x_arr[t] = chr(x_arr[t])
            t += 1
        return r.join(x_arr)
