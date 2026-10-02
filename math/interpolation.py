from rational import Rational

def flt(num: str) -> int | float:
    if '.' in num:
        return float(num)
    return int(num)

def coeff(n: int | float | Rational, points: list[tuple[int | float | Rational, int | float | Rational]]) -> int | float | Rational:
    a_n = None
    for pt in points:
        if pt[0] == n:
            a_n = pt[1]
    prod = 1
    for pt in points:
        if pt[0] != n:
            prod *= (n - pt[0])
    return Rational(a_n, prod)

def vietta(roots: list[int | float | Rational], leading_coeff: int | float | Rational = 1):
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

def term(n: int | float | Rational, points: list[tuple[int | float | Rational, int | float | Rational]]) -> list[int | float | Rational]:
    roots: list[int | float | Rational] = []
    for pt in points:
        if pt[0] != n:
            roots.append(pt[0])
    return vietta(roots, coeff(n, points))
    
def sup(n: int) -> str:
    if n <= 1: return ''
    sup = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    return str(n).translate(sup)

def allcoeffs(points: list[tuple[int | float | Rational, int | float | Rational]]) -> list[int | float | Rational]:
    coeffs: list[int | float | Rational] = list([0]*len(points))
    for pt in points:
        trm = term(pt[0], points)
        for i in range(len(trm)):
            coeffs[i] += trm[i]
    return coeffs

def runpoly(x: int | float | Rational, polynomial: list[int | float | Rational]) -> int | float | Rational:
    y: int | float | Rational = 0
    for i in range(len(polynomial)):
        y += (polynomial[i]*pow(x, i))
    return round(y) if round(y) == y else y

def print_polynomial(pol: list[int | float | Rational]) -> None:
    res = repr(pol[-1]) + 'x' + sup(len(pol) - 1)
    for i in range(len(pol) - 2, -1, -1):
        if pol[i]:
            res += ('+' if pol[i] > 0 else '') + repr(pol[i]) + ('x' if i > 0 else '') + sup(i)
    print(res)

def main():
    points: list[tuple[int | float | Rational, int | float | Rational]] = []
    print('Points: (x y, seperated by space or comma)')
    inp = input()
    while inp:
        if ',' in inp:
            x, y = inp.split(',')
        else:
            x, y = inp.split()
        if '/' in x:
            x = x.split('/')
            x = Rational(flt(x[0].strip()), flt(x[1].strip()))
        else:
            x = flt(x.strip())
        if '/' in y:
            y = y.split('/')
            y = Rational(flt(y[0].strip()), flt(y[1].strip()))
        else:
            y = flt(y.strip())
        points.append((x, y))
        inp = input()
    polynomial = allcoeffs(points)
    print_polynomial(polynomial)
    evaluateQ = input('Want to evaluate? (y/n)')
    if evaluateQ and evaluateQ[0] == 'y':
        where = input('Where?')
        if '/' in where:
            where = where.split('/')
            where = Rational(flt(where[0].strip()), flt(where[1].strip()))
        else:
            where = flt(where.strip())
        print(runpoly(where, polynomial))
        where = input()
        while where:
            if '/' in where:
                where = where.split('/')
                where = Rational(flt(where[0].strip()), flt(where[1].strip()))
            else:
                where = flt(where.strip())
            print(runpoly(where, polynomial))
            where = input()


if __name__ == '__main__':
    main()