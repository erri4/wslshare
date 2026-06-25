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

## fibonacci

class Qsqrt5:
    a: int
    b: int

    def __init__(self, a: int, b: int = 0):
        self.a = a
        self.b = b
    
    def __mul__(self, other: "Qsqrt5"):
        return Qsqrt5(self.a * other.a + 5 * self.b * other.b, self.a * other.b + self.b * other.a)

    def __repr__(self):
        if self.a and self.b:
            return f'{repr(self.a)} + sqrt5 * {repr(self.b)}'
        if self.b:
            return f'sqrt5 * {repr(self.b)}'
        return repr(self.a)

    def __eq__(self, other: "Qsqrt5"):
        return self.a == other.a and self.b == other.b

    def __sub__(self, other: "Qsqrt5"):
        return Qsqrt5(self.a - other.a, self.b - other.b)

def fastpow(a: Qsqrt5 | int, n: int):
    b = [int(c) for c in bin(n)[2:]]
    b.reverse()
    powsa = [a]
    for i in range(1, len(b)):
        powsa.append(powsa[i - 1] * powsa[i - 1])
    res = type(a)(1)
    for i in range(len(powsa)):
        if b[i]:
            res *= powsa[i]
    return res

def fibonacci(n: int):
    phi = Qsqrt5(1, 1)
    psi = Qsqrt5(1, -1)
    return (fastpow(phi, n) - fastpow(psi, n)).b // fastpow(2, n)

if __name__ == '__main__':
    print(fibonacci(100))
