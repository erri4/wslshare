from Rational import Rational
from itertools import dropwhile

Number: tuple = (int, Rational, float)
type Num = int | Rational | float

class Polynomial:
    coeffs: list[Num]

    def __init__(self, coeffs: list[Num]):
        while coeffs and coeffs[-1] == 0:
            coeffs.pop()
        self.coeffs = coeffs

    @classmethod
    def pol0(cls):
        return cls.poln(0)

    @classmethod
    def pol1(cls):
        return cls.poln(1)

    @classmethod
    def poln(cls, n: Num):
        return cls([n])

    @classmethod
    def Id(cls):
        return cls([0, 1])

    @staticmethod
    def coeff(n: Num, points: list[tuple[Num, Num]]) -> Num:
        a_n = None
        for pt in points:
            if pt[0] == n:
                a_n = pt[1]
        prod = 1
        for pt in points:
            if pt[0] != n:
                prod *= (n - pt[0])
        return Rational(a_n, prod)

    @staticmethod
    def vietta(roots: list[Num], leading_coeff: Num = 1):
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

    @staticmethod
    def term(n: Num, points: list[tuple[Num, Num]]) -> list[Num]:
        roots: list[Num] = []
        for pt in points:
            if pt[0] != n:
                roots.append(pt[0])
        return Polynomial.vietta(roots, Polynomial.coeff(n, points))

    @classmethod
    def from_points(cls, points: list[tuple[Num, Num]]):
        coeffs: list[Num] = list([0]*len(points))
        for pt in points:
            trm = Polynomial.term(pt[0], points)
            for i in range(len(trm)):
                coeffs[i] += trm[i]
        return cls(list(reversed(list(dropwhile(lambda x: x == 0, reversed(coeffs))))))

    @staticmethod
    def sup(n: int) -> str:
        if n <= 1: return ''
        sup = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
        return str(n).translate(sup)

    @staticmethod
    def coeffrepr(co: Num, i: Num):
        if co == 0: return ''
        if i == 0: return ('+' if co > 0 else '') + repr(co)
        if co == 1: return '+x' + Polynomial.sup(i)
        return ('+' if co > 0 else '') + repr(co) + 'x' + Polynomial.sup(i)

    @property
    def deg(self):
        if not self.coeffs: return -float('inf')
        return len(self.coeffs) - 1

    def __getitem__(self, key: int):
        if key < len(self.coeffs): return self.coeffs[key]
        return 0

    def __call__(self, x: Num) -> "Num | Polynomial":
        y: Num = 0
        for i in range(len(self.coeffs)):
            y += (self.coeffs[i]*pow(x, i))
        return y

    def __str__(self):
        return str(self.coeffs)

    def __len__(self):
        return len(self.coeffs)

    def __iter__(self):
        yield from self.coeffs

    def __eq__(self, other: "Polynomial | Num"):
        if type(other) in Number:
            return self.deg <= 0 and self[0] == other
        return self.coeffs == other.coeffs

    def __ge__(self, other: "Polynomial | Num"):
        if type(other) in Number: return self.deg >= 0
        return self.deg >= other.deg

    def __le__(self, other: "Polynomial | Num"):
        if type(other) in Number: return self.deg <= 0
        return self.deg <= other.deg

    def __gt__(self, other: "Polynomial | Num"):
        if type(other) in Number: return self.deg > 0
        return self.deg > other.deg

    def __lt__(self, other: "Polynomial | Num"):
        if type(other) in Number: return self.deg < 0
        return self.deg < other.deg

    def __repr__(self):
        pol = self.coeffs.copy()
        res = Polynomial.coeffrepr(pol[-1], len(pol) - 1)
        if res[0] == '+': res = res[1:]
        for i in range(len(pol) - 2, -1, -1):
            if pol[i]:
                res += Polynomial.coeffrepr(pol[i], i)
        return res

    def __add__(self, other: "Polynomial | Num"):
        if type(other) in Number:
            new = self.coeffs.copy()
            new[0] += other
            return Polynomial(new)
        new = [0] * (max(self.deg, other.deg) + 1)
        for i in range(len(new)):
            new[i] = self[i] + other[i]
        return Polynomial(new)

    def __radd__(self, other: "Polynomial | Num"):
        if type(other) in Number:
            new = self.coeffs.copy()
            new[0] += other
            return Polynomial(new)
        new = [0] * (max(self.deg, other.deg) + 1)
        for i in range(len(new)):
            new[i] = self[i] + other[i]
        return Polynomial(new)

    def __sub__(self, other: "Polynomial | Num"):
        if type(other) in Number:
            new = self.coeffs.copy()
            new[0] -= other
            return Polynomial(new)
        new = [0] * (max(self.deg, other.deg) + 1)
        for i in range(len(new)):
            new[i] = self[i] - other[i]
        return Polynomial(new)

    def __rsub__(self, other: "Polynomial | Num"):
        if type(other) in Number:
            new = [-c for c in self.coeffs.copy()]
            new[0] += other
            return Polynomial(new)
        new = [0] * (max(self.deg, other.deg) + 1)
        for i in range(len(new)):
            new[i] = other[i] - self[i]
        return Polynomial(new)

    def __mul__(self, other: "Polynomial | Num"):
        if type(other) in Number:
            new = [(c * other) for c in self.coeffs.copy()]
            return Polynomial(new)
        if not self or not other:
            return Polynomial.pol0()
        
        result = [0] * (self.deg + other.deg + 1)
        
        for i, a in enumerate(self):
            for j, b in enumerate(other):
                result[i + j] += a * b  
        return Polynomial(result)

    def __rmul__(self, other: "Polynomial | Num"):
        if type(other) in Number:
            new = [(c * other) for c in self.coeffs.copy()]
            return Polynomial(new)
        if not self or not other:
            return Polynomial.pol0()
        
        result = [0] * (self.deg + other.deg + 1)
        
        for i, a in enumerate(self):
            for j, b in enumerate(other):
                result[i + j] += a * b  
        return Polynomial(result)

    def __matmul__(self, other: "Polynomial | Num"):
        return self(other)

    def __rmatmul__(self, other: "Polynomial | Num"):
        if type(other) in Number: return other
        return other(self)

    def __divmod__(self, other: "Polynomial | Num"):
        if not other or other == 0: raise ZeroDivisionError("Division by the zero polynomial.")
        if type(other) in Number:
            new = self.coeffs.copy()
            for i in range(len(new)): new[i] /= other
            return Polynomial(new), Polynomial.pol0()
        
        if self.deg < other.deg:
            return [0], self
        
        A = self.coeffs.copy()
        B = other.coeffs.copy()
        
        quotient = [0] * (self.deg - other.deg + 1)
        
        while len(A) >= len(B) and any(A):
            deg_diff = (len(A) - 1) - other.deg
            factor = A[-1] / B[-1]
            
            quotient[deg_diff] = factor
            
            for i, b_coeff in enumerate(B):
                A[deg_diff + i] -= factor * b_coeff
                
            while A and ((A[-1] < 1e-12 and type(A[-1]) is float) or A[-1] == 0):
                A.pop()
        return Polynomial(quotient), Polynomial(A)

    def __mod__(self, other: "Polynomial | Num"):
        return divmod(self, other)[1]

    def __floordiv__(self, other: "Polynomial | Num"):
        return divmod(self, other)[0]

    def __pow__(self, other: int):
        c = Polynomial.pol1()
        binb = [int(c) for c in bin(other)[2:]]
        binb.reverse()
        binc: list[Polynomial] = []
        for i in range(len(binb)):
            if i == 0: binc.append(self)
            else: binc.append(binc[i - 1] * binc[i - 1])

        for i in range(len(binc)):
            if binb[i]: c *= binc[i]
        return c

    def __xor__(self, other: int):
        return self ** other # for things like p = x^8 +123 + 5 +6 * x

    def derivative(self, order: int = 1) -> "Polynomial":
        if order == 0: return self
        if order < 0: return self.integral(-order)
        if order == 1:
            if self.deg <= 0: return Polynomial.pol0()
            new = [0] * (self.deg)
            for i in range(len(new)):
                new[i] = self[i + 1] * (i + 1)
            return Polynomial(new)
        return self.derivative(order - 1).derivative()

    def integral(self, order: int = 1) -> "Polynomial":
        if order == 0: return self
        if order < 0: return self.derivative(-order)
        if order == 1:
            if self.deg < 0: return Polynomial.pol0()
            new = [0] * (self.deg + 2)
            for i in range(self.deg + 1):
                try:
                    new[i + 1] = Rational(self[i], i + 1)
                except TypeError:
                    new[i + 1] = self[i] / (i + 1)
            return Polynomial(new)
        return self.integral(order - 1).integral()

x = Polynomial.Id()

def flt(num: str) -> int | float:
    if '.' in num:
        return float(num)
    return int(num)

def main():
    points: list[tuple[Num, Num]] = []
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
    polynomial = Polynomial.from_points(points)
    print(polynomial)
    evaluateQ = input('Want to evaluate? (y/n)')
    if evaluateQ and evaluateQ[0] == 'y':
        where = input('Where?')
        if '/' in where:
            where = where.split('/')
            where = Rational(flt(where[0].strip()), flt(where[1].strip()))
        else:
            where = flt(where.strip())
        print(polynomial(where))
        where = input()
        while where:
            if '/' in where:
                where = where.split('/')
                where = Rational(flt(where[0].strip()), flt(where[1].strip()))
            else:
                where = flt(where.strip())
            print(polynomial(where))
            where = input()


if __name__ == '__main__':
    main()