from Rational import Rational
from abc import ABC, abstractmethod
from typing import Callable
from operator import add, sub, truediv, call, mul # pow
from math import e as _e, pi as _pi, sin as _sin, cos as _cos, log, floor, ceil # round, abs
from util import sqrt

commutative = (add, mul)

type Real = int | float | Rational | Function
_round = round

class IntegrationError(Exception): pass
class DifferentiationError(Exception): pass

class Function(ABC):
    @abstractmethod
    def __call__(self, x: "Function") -> Real: raise NotImplementedError("You are using the base `Function` type. Check your code for logic arrors")
    
    @abstractmethod
    def __eq__(self, other: "Function"): raise NotImplementedError("You are using the base `Function` type. Check your code for logic arrors")

    @abstractmethod
    def __repr__(self): raise NotImplementedError("You are using the base `Function` type. Check your code for logic arrors")
    
    @abstractmethod
    def _derivative(self) -> "Function": raise NotImplementedError("You are using the base `Function` type. Check your code for logic arrors")

    @abstractmethod
    def _integral(self) -> "Function": raise NotImplementedError("You are using the base `Function` type. Check your code for logic arrors")
    
    def __add__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(self, other, add)
    
    def __radd__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(other, self, add)
    
    def __sub__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(self, other, sub)
    
    def __rsub__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(other, self, sub)
    
    def __mul__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(self, other, mul)
    
    def __rmul__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(other, self, mul)
    
    def __matmul__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(self, other, call)
    
    def __rmatmul__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(other, self, call)
    
    def __floordiv__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return floor(FuncionOPTree(self, other, truediv))
    
    def __truediv__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(self, other, truediv)
    
    def __pow__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(self, other, pow)
    
    def __xor__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return self ** other
    
    def __rfloordiv__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return floor(FuncionOPTree(other, self, truediv))
    
    def __rtruediv__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(other, self, truediv)
    
    def __rpow__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return FuncionOPTree(other, self, pow)
    
    def __rxor__(self, other: "Function") -> "Function":
        if not isinstance(other, (Function, int, float, Rational)): return NotImplemented
        return other ** self
    
    def __abs__(self) -> "Function":
        tmp = Unary(abs)
        tmp.deriv = tmp / x
        tmp.integ = (tmp / x) * x.integral()
        return tmp@self
    
    def __floor__(self) -> "Function":
        return Unary(floor, derivative=ConstantFunction(0))@self
    
    def __ceil__(self) -> "Function":
        return Unary(ceil, derivative=ConstantFunction(0))@self
    
    def __neg__(self) -> "Function":
        return (-x)@self
    
    def __pos__(self) -> "Function":
        return x@self
    
    def __round__(self, ndigits: int | None = None):
        def round(x):
            return _round(x, ndigits)
        return Unary(round)@self

    def derivative(self, order: int = 1) -> "Function":
        range(order)
        if order == 0: return +self
        if order == 1: return self._derivative()
        if order < 0: return self.integral(-order)
        return self.derivative(order - 1).derivative()

    def integral(self, order: int = 1) -> "Function":
            range(order)
            if order == 0: return +self
            if order == 1: return self._integral()
            if order < 0: return self.derivative(-order)
            return self.integral(order - 1).integral()
    
    def __str__(self):
        return repr(self)

class Identity(Function):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __call__(self, x):
        return x

    def __eq__(self, other):
        return other is self._instance

    def __repr__(self):
        return 'x'

    def __neg__(self):
        return NegIdentity()

    def _derivative(self):
        return ConstantFunction(1)

    def _integral(self):
        return (self ** 2) / 2

class NegIdentity(Function):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __call__(self, x):
        return -x

    def __eq__(self, other):
        return other is self._instance

    def __repr__(self):
        return '(-x)'

    def _derivative(self):
        return ConstantFunction(-1)

    def _integral(self):
        return -(self ** 2) / 2

x = Identity()

class ConstantFunction(Function):
    value: Real

    def __init__(self, value: Real):
        self.value = value

    def __eq__(self, other: Real):
        if isinstance(other, Function):
            if isinstance(other, ConstantFunction):
                return self.value == other.value
            return False
        return self.value == other

    def __call__(self, x):
        return self.value

    def _derivative(self):
        return ConstantFunction(0)

    def _integral(self):
        return x * self

    def __repr__(self):
        return repr(self.value)

class FuncionOPTree(Function):
    left: Function
    right: Function
    op: Callable[[Real, Real], Real]

    def __new__(cls, left: Function, right: Function, op: Callable[[Real], Real]):
        if not isinstance(left, Function):
            left = ConstantFunction(left)
        if not isinstance(right, Function):
            right = ConstantFunction(right)

        if isinstance(left, ConstantFunction) and isinstance(right, ConstantFunction):
            return ConstantFunction(op(left.value, right.value))
        if isinstance(right, ConstantFunction) and op is call:
            return ConstantFunction(op(left, right.value))
        if (left == ConstantFunction(0) and op is add) or (left == ConstantFunction(1) and op is mul):
            return right
        if (right == ConstantFunction(0) and op is add) or (right == ConstantFunction(1) and (op is mul or op is pow or op is truediv)):
            return left
        if right == ConstantFunction(0) and op is pow:
            return ConstantFunction(1)
        if left in (ConstantFunction(0), ConstantFunction(1)) and op is pow:
            return left
        if ConstantFunction(0) in (left, right) and op is mul:
            return ConstantFunction(0)
        return super().__new__(cls)

    def __init__(self, left: Function, right: Function, op: Callable[[Real], Real]):
        if self is left or self is right: return
        if not isinstance(left, Function):
            left = ConstantFunction(left)
        if not isinstance(right, Function):
            right = ConstantFunction(right)
        if op is pow:
            if isinstance(right, ConstantFunction) and right.value % 2 == 0:
                if isinstance(left, FuncionOPTree) and left.op is call and left.left is (-x):
                    left = left.right
                if left is (-x):
                    left = x
        self.left = left
        self.right = right
        self.op = op

    def __call__(self, x):
        if self.op is not call:
            return self.op(self.left(x), self.right(x))
        else:
            return self.op(self.left, self.right(x))

    def __eq__(self, other):
        if isinstance(other, FuncionOPTree):
            if self.op in commutative:
                if self.left == other.right and self.right == other.left:
                    return True
            return self.left == other.left and self.right == other.right
        return False

    def __repr__(self):
        match self.op.__name__:
            case 'add':
                rpr = repr(self.left) + '+' + repr(self.right)
            case 'sub':
                rpr = repr(self.left) + '-' + repr(self.right)
            case 'mul':
                rpr = repr(self.left) + '*' + repr(self.right)
            case 'call':
                return repr(self.left).replace('x', repr(self.right))
            case 'pow':
                rpr = repr(self.left) + '^' + repr(self.right)
            case 'truediv':
                rpr = repr(self.left) + '/' + repr(self.right)
            case _: rpr = self.op.__name__ + f'({repr(self.left)}, {repr(self.right)})'
        return f'({rpr})'

    def _derivative(self):
        match self.op.__name__:
            case 'add':
                return self.left.derivative() + self.right.derivative()
            case 'sub':
                return self.left.derivative() - self.right.derivative()
            case 'mul':
                return self.left * self.right.derivative() + self.left.derivative() * self.right
            case 'call':
                return (self.left.derivative()@self.right) * self.right.derivative()
            case 'pow':
                return self * (self.right.derivative() * (ln@self.left) + self.right * (self.left.derivative() / self.left))
            case 'truediv':
                return (self.left.derivative() * self.right - self.left * self.right.derivative()) / (self.right ** 2)
            case _: raise DifferentiationError('Non differentiable function')

    def _integral(self):
        match self.op.__name__:
            case 'add':
                return self.left.integral() + self.right.integral()
            case 'sub':
                return self.left.integral() - self.right.integral()
            case 'mul':
                if isinstance(self.left, ConstantFunction):
                    return self.left * self.right.integral()
                if isinstance(self.right, ConstantFunction):
                    return self.right * self.left.integral()
                raise IntegrationError('Non integrable function')
            case 'pow':
                if isinstance(self.right, ConstantFunction) and self.left is x:
                    return (x ^ (self.right + 1)) / (self.right + 1)
                if isinstance(self.left, ConstantFunction) and self.right is x:
                    return self / (ln@self.left)
                raise IntegrationError('Non integrable function')
            case _: raise IntegrationError('Non integrable function')

class Unary(Function):
    func: Callable[[Real], Real]
    deriv: Function | None
    integ: Function | None

    def __init__(self, func: Callable[[Real], Real], derivative: Function | None = None, integral: Function | None = None):
        self.func = func
        self.deriv = derivative
        self.integ = integral

    def __eq__(self, other):
        if isinstance(other, Function):
            if isinstance(other, Unary):
                return self.func == other.func
        return False

    def __call__(self, x):
        return self.func(x)

    def __repr__(self):
        return self.func.__name__ + '(x)'

    def _integral(self):
        if self.integ is not None: return self.integ
        raise IntegrationError('Non integrable function')

    def _derivative(self):
        if self.deriv is not None: return self.deriv
        raise DifferentiationError('Non differentiable function')

ln = Unary(log, derivative=(1/x))
ln.integ = x * ln - x

sin = Unary(_sin)
cos = Unary(_cos, derivative=-sin, integral=sin)
sin.deriv = cos
sin.integ = -cos
tan = sin / cos
cot = cos / sin
e = ConstantFunction(_e)
pi = ConstantFunction(_pi)
exp = e^x

if __name__ == '__main__':
    print(exp.derivative())