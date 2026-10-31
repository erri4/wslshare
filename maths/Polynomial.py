from Rational import Rational
from itertools import dropwhile
from Function import x, Real

def coeff(n: Real, points: list[tuple[Real, Real]]) -> Real:
    a_n = None
    for pt in points:
        if pt[0] == n:
            a_n = pt[1]
    prod = 1
    for pt in points:
        if pt[0] != n:
            prod *= (n - pt[0])
    return Rational(a_n, prod)

def vietta(roots: list[Real], leading_coeff: Real = 1):
    coeffs: list[int | float] = [1]
    for r in roots:
        new_coeffs = [0] * (len(coeffs) + 1)
        for i in range(len(coeffs)):
            new_coeffs[i] += coeffs[i]
            new_coeffs[i + 1] -= r * coeffs[i]
        coeffs = new_coeffs

    coeffs = [leading_coeff * c for c in coeffs]
    coeffs.reverse()
    return coeffs

def term(n: Real, points: list[tuple[Real, Real]]) -> list[Real]:
    roots: list[Real] = []
    for pt in points:
        if pt[0] != n:
            roots.append(pt[0])
    return vietta(roots, coeff(n, points))

def sup(n: int) -> str:
    if n <= 1: return ''
    sup = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    return str(n).translate(sup)

def coeffrepr(co: Real, i: Real):
    if co == 0: return ''
    if i == 0: return ('+' if co > 0 else '') + repr(co)
    if co == 1: return '+x' + sup(i)
    return ('+' if co > 0 else '') + repr(co) + 'x' + sup(i)

def from_points(points: list[tuple[Real, Real]]):
    coeffs: list[Real] = list([0]*len(points))
    for pt in points:
        trm = term(pt[0], points)
        for i in range(len(trm)):
            coeffs[i] += trm[i]
    return list(reversed(list(dropwhile(lambda x: x == 0, reversed(coeffs)))))

def from_list(coeffs: list[Real]):
    res = 0
    for i in range(len(coeffs)):
        res += coeffs[i] * (x^i)
    return res
        
def flt(num: str) -> int | float:
    if '.' in num:
        return float(num)
    return int(num)

def main():
    points: list[tuple[Real, Real]] = []
    print('Points: (x y, seperated by space or comma)')
    inp = input()
    while inp:
        if ',' in inp:
            _x, _y = inp.split(',')
        else:
            _x, _y = inp.split()
        if '/' in _x:
            _x = _x.split('/')
            _x = Rational(flt(_x[0].strip()), flt(_x[1].strip()))
        else:
            _x = flt(_x.strip())
        if '/' in _y:
            _y = _y.split('/')
            _y = Rational(flt(_y[0].strip()), flt(_y[1].strip()))
        else:
            _y = flt(_y.strip())
        points.append((_x, _y))
        inp = input()
    polynomial = from_points(points)
    pol = polynomial.copy()
    res = coeffrepr(pol[-1], len(pol) - 1)
    if res[0] == '+': res = res[1:]
    for i in range(len(pol) - 2, -1, -1):
        if pol[i]:
            res += coeffrepr(pol[i], i)
    print(res)
    polynomial = from_list(polynomial)
    evaluateQ = input('Want to evaluate? (y/n)')
    if evaluateQ and evaluateQ[0].lower() == 'y':
        where = input('Where? ')
        if where and where[0].lower() != 'q':
            if '/' in where:
                where = where.split('/')
                where = Rational(flt(where[0].strip()), flt(where[1].strip()))
            else:
                where = flt(where.strip())
            print(polynomial(where))
            where = input('Where? ')
            while where and where[0].lower() != 'q':
                if '/' in where:
                    where = where.split('/')
                    where = Rational(flt(where[0].strip()), flt(where[1].strip()))
                else:
                    where = flt(where.strip())
                print(polynomial(where))
                where = input('Where? ')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: pass