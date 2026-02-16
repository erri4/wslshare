import math
primes = [2, 3]

def isprime(num: int):
    if math.sqrt(num) == int(math.sqrt(num)): return False
    for i in range(3, math.ceil(math.sqrt(num)), 2):
        if num % i == 0:
            return False
    return True

mx = 100000
found = []
for i in range(0, mx, 2):
    for j in primes:
        if isprime(i + j):
            primes.append(j + i)
            found.append(i)
            break

print(len(found) == mx / 2)