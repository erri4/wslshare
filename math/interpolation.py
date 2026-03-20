points: list[tuple[int | float, int | float]] = [(1, 6), (2, 12), (3, 20), (10, 14), (6.93463, 43.91536)]

def coeff(n: int | float) -> int | float:
    a_n = None
    for pt in points:
        if pt[0] == n:
            a_n = pt[1]
    prod = 1
    for pt in points:
        if pt[0] != n:
            prod *= (n - pt[0])
    return round(a_n / prod) if round(a_n / prod) == a_n / prod else a_n / prod

def vietta(roots: list[int | float], leading_coeff: int | float = 1):
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

def term(n: int | float) -> list[int | float]:
    roots: list[int | float] = []
    for pt in points:
        if pt[0] != n:
            roots.append(pt[0])
    return vietta(roots, coeff(n))
    
def sup(n: int):
    sup = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    return str(n).translate(sup)

def all() -> list[int | float]:
    coeffs: list[int | float] = list([0]*len(points))
    for pt in points:
        trm = term(pt[0])
        for i in range(len(trm)):
            coeffs[i] += trm[i]
    for i in range(len(coeffs)):
        coeffs[i] = round(coeffs[i]) if coeffs[i] == round(coeffs[i]) else round(coeffs[i], 7)
    return coeffs

def runpoly(x: int | float, polynomial: list[int | float]) -> int | float:
    y: int | float = 0
    for i in range(len(polynomial)):
        y += (polynomial[i]*pow(x, i))
    return round(y) if round(y) == y else round(y, 7)

def print_polynomial(pol: list[int | float]) -> None:
    res = ''
    pol.reverse()
    for i in range(len(pol) - 2):
        if pol[i] != 0:
            res += f'{pol[i] if pol[i] != 1 else ''}x{sup(len(pol) - i - 1)}+'
    if pol[-2] != 0:
        if pol[-1] != 0:
            res += f'{pol[-2] if pol[-2] != 1 else ''}x+{pol[-1]}'
        else:
            res += f'{pol[-2] if pol[-2] != 1 else ''}x'
    else:
        if pol[-1] != 0:
            res += f'{pol[-1]}'
    print(res)

polynomial = all()
print_polynomial(polynomial)
print(runpoly(2, polynomial))