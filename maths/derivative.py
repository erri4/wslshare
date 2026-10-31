from math import isqrt

def arithmetic(n: int):
    if n in (0, 1): return 0
    if n in (2, 3): return 1
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return arithmetic(n // i) * i + (n // i) * arithmetic(i)
    return 1
