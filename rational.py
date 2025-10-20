from typing import TypeAlias

Number: TypeAlias = "Rational | int | float"


def gcd(a: int, b: int) -> int:
    if b > a:
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a


class Rational:
    # class things

    def __new__(cls, p: int, q: int): # p/q
        if q == 0:
            raise ZeroDivisionError("division by zero")
        gdcpq = gcd(p, q)
        p /= gdcpq
        q /= gdcpq
        if q == 1:
            return int(p)
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, p: int, q: int):
        if q == 0:
            raise ZeroDivisionError("division by zero")
        gdcpq = gcd(p, q)
        p /= gdcpq
        q /= gdcpq
        self.p = int(p)
        self.q = int(q)

    @classmethod
    def from_float(cls, num: float | int):
        mul = 1
        while num*mul != int(num*mul):
            mul *= 10
        return Rational(int(num*mul), mul)

    def to_float(self):
        return self.p / self.q


    def __repr__(self):
        return f'{self.p}/{self.q}'

    def __str__(self):
        return f'{self.p}/{self.q}'
    
    # math operators
    
    def __add__(self, other: Number): 
        if type(other) is Rational:
            return Rational(self.p*other.q + other.p*self.q, self.q*other.q)
        if type(other) is int:
            return Rational(self.p + self.q*other, self.q)
        return self + Rational.from_float(other)

        
    def __sub__(self, other: Number):
        if type(other) is Rational:
            return self + (-other)
        return Rational.from_float(self.to_float() - other)
        
    
    def __mul__(self, other: Number):
        if type(other) is Rational:
            return Rational(self.p*other.p, self.q*other.q)
        if type(other) == int:
            return Rational(self.p*other, self.q)
        return self * Rational.from_float(other)
    

    def __pow__(self, other: Number):
        if type(other) is int:
            return Rational(self.p ** other, self.q ** other)
        if type(other) is Rational:
            return Rational.from_float((self.p ** other.to_float()) / (self.q ** other.to_float()))
        return self ** Rational.from_float(other)

    def __truediv__(self, other: Number):
        if other == 0:
            raise ZeroDivisionError("division by zero")
        if type(other) is Rational:
            return Rational(self.p*other.q, self.q*other.p)
        if type(other) == int:
            return Rational(self.p, self.q*other)
        return self / Rational.from_float(other)
    # right hand operators

    def __rtruediv__(self, other: Number):
        if type(other) is Rational:
            return Rational(other.p*self.q, other.q*self.p)
        if type(other) == int:
            return Rational(other * self.q, self.p)
        return Rational.from_float(other) / self
    
    def __radd__(self, other: Number): 
        if type(other) is Rational:
            return Rational(self.p*other.q + other.p*self.q, self.q*other.q)
        if type(other) is int:
            return Rational(self.p + self.q*other, self.q)
        return self + Rational.from_float(other)

        
    def __rsub__(self, other: Number):
        if type(other) is Rational:
            return -self + other
        return Rational.from_float(self.to_float() - other)
        
    
    def __rmul__(self, other: Number):
        if type(other) is Rational:
            return Rational(self.p*other.p, self.q*other.q)
        if type(other) == int:
            return Rational(self.p*other, self.q)
        return self * Rational.from_float(other)
    

    def __rpow__(self, other: Number):
        if type(other) is Rational:
            return Rational.from_float((other.p ** self.to_float()) / (other.q ** self.to_float()))
        return Rational.from_float(other ** self.to_float())

    # comparators

    def __eq__(self, other: Number):
        if type(other) is Rational:
            return self.p == other.p and self.q == other.q
        if type(other) == int:
            return self.q == 0 and self.p == other
        return self == Rational.from_float(other)
    
    def __le__(self, other: Number):
        if type(other) is Rational:
            return self.to_float() <= other.to_float()
        return self.to_float() <= other
    
    def __lt__(self, other: Number):
        if type(other) is Rational:
            return self.to_float() < other.to_float()
        return self.to_float() < other
    
    def __ne__(self, other: Number):
        if type(other) is Rational:
            return self.to_float() != other.to_float()
        return self.to_float() != other
    
    def __gt__(self, other: Number):
        if type(other) is Rational:
            return self.to_float() > other.to_float()
        return self.to_float() > other
    
    def __ge__(self, other: Number):
        if type(other) is Rational:
            return self.to_float() >= other.to_float()
        return self.to_float() >= other

    # unary operators

    def __invert__(self):
        return 1 / self
    
    def __neg__(self):
        return Rational(-self.p, self.q)
    
    def __pos__(self):
        return Rational(+self.p, self.q)
    
    def __abs__(self):
        return Rational(abs(self.p), abs(self.q))
    
    def __round__(self, n: int):
        return round(self.to_float(), n)
