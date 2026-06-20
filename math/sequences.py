dpt = [1]
dpy = [0]

def t(n: int):
    if n == 0:
        return 1
    if len(dpt) <= n: dpt.extend([-1] * (n - len(dpt) + 1))
    if dpt[n] >= 0: return dpt[n]
    t_n = int(str(t(n - 1)) + str(y(n))) // y(n)
    dpt[n] = t_n
    return t_n

def y(n: int):
    if n == 0:
        return 0
    if len(dpy) <= n: dpy.extend([-1] * (n - len(dpy) + 1))
    if dpy[n] >= 0: return dpy[n]
    y_n = y(n - 1) + 1
    while int(str(t(n - 1)) + str(y_n)) % y_n:
        y_n += 1
    dpy[n] = y_n
    return y_n

def mexseq():
    sm = 0
    for i in range(166):
        print(i, t(i), y(i))
        sm += 1/t(i)
    print(sm)

if __name__ == '__main__':
    mexseq()
