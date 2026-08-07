from rational import Rational
from math import floor
from string import ascii_uppercase, digits as digs
chars = digs + ascii_uppercase

def main():
    number = input("Number: ")
    base = input("Base: ")
    baseto = input("To base: ")
    base = int(base)
    baseto = int(baseto)
    if base == baseto:
        print(number)
        return
    if '.' not in number:
        n = int(number, base)
        digits = []
        while n > 0:
            digits.append(chars[n % baseto])
            n //= baseto
        digits.reverse()
        print(''.join(digits))
    else:
        num, fraction = number.split('.')
        n = int(num, base)
        frac = Rational(int(fraction, base), base**len(fraction))
        digits = []
        while n > 0:
            digits.append(chars[n % baseto])
            n //= baseto
        digits.reverse()
        if len(digits) == 0:
            digits.append('0')
        print(''.join(digits),end='.')
        fracdigits = []
        seen = {}
        while frac != 0:
            seen[frac] = len(fracdigits)
            fracdigits.append(chars[floor(frac * baseto)])
            frac = frac * baseto - floor(frac * baseto)
            if frac in seen:
                break
        if frac in seen:
            fracdigits.insert(seen[frac], ' ')
            fracdigits.append('...')
        print(''.join(fracdigits))

if __name__ == '__main__':
    main()