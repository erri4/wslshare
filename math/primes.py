import math
from typing import Callable

def sigma(start: int, end: int, f: Callable[[int], int]):
    sum = 0
    for i in range(start, end + 1):
        sum += f(i)
    return sum

def pi(x: int):
    def inner(j: int) -> int:
        return math.floor(math.cos(math.pi * (math.factorial(j - 1) + 1) / j) ** 2)
    r = sigma(1, x, inner)
    return r - 1

def prime(n: int):
    def inner(j: int) -> int:
        return pi(j) + 1
    def outer(i: int) -> int:
        return math.floor((n / inner(i)) ** (1 / n))
    return 1 + sigma(1, 2 ** n, outer)

for i in range(1, 8):
    print(prime(i))