from matrix import Matrix, MatrixDimensionsError
from vector import Vector, DimensionError
from rational import Rational
from typing import Callable
import re
import math
import os

def det(mat: Matrix):
    return mat.det()

def ang(v1: Vector, v2: Vector | None = None):
    if v2 is None:
        return v1.theta
    return v1.angle(v2)

def norm(v1: Vector):
    return ~v1

def dim(x: Matrix | Vector):
    if isinstance(x, Vector):
        return x.dim
    if isinstance(x, Matrix):
        return Vector(x.col, x.row)

env: dict[str, Vector | Matrix | Rational | int | float, Callable] = {"det": det, "Det": det, "ang": ang, "norm": norm, "dim": dim, "sin": math.sin, "arcsin": math.asin, "cos": math.cos, "arccos": math.acos, "tan": math.tan, "arctan": math.atan, "sqrt": math.sqrt, "e": math.e, "pi": math.pi, "Vector": Vector, "Matrix": Matrix, "Rational": Rational, "Id": Matrix.Id}

def smrtsplt(s: str):
    args = []
    start = 0
    depth = 0
    
    for i, c in enumerate(s):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c == ',' and depth == 0:
            args.append(s[start:i].strip())
            start = i + 1

    args.append(s[start:].strip())
    return args


def readVector(env: dict | None = None) -> Vector:
    if env is None:
        vec = tuple([int(x.strip()) for x in input().split()])
    else:
        vec = tuple([eval(pythonize(x.strip()), env) for x in input().split()])
    return Vector(vec)

def readRational(env: dict | None = None) -> Rational:
    if env is None:
        p, q = [int(x.strip()) for x in input().split('/')]
    else:
        p, q = [eval(pythonize(x.strip()), env) for x in input().split('/')]
    return Rational(p, q)

def readMatrix(env: dict | None = None) -> Matrix:
    mat = []
    while True:
        try:
            if env is None:
                row = [int(x) for x in input().split()]
            else:
                row = [eval(pythonize(x), env) for x in input().split()]
            if row == []: break
            mat.append(row)
        except ValueError:
            break

    return Matrix(mat)

def pythonize(expr: str):
    expr = expr.replace('x', '@').replace('^T', '.T()').replace('^', '**').replace('\\/', '//').replace('/\\', '//')
    pattern = re.compile(r'(?<![A-Za-z0-9_])\(([^,()]+),\s*([^,()]+)(?:,\s*([^,()]+))?\)')
    def repl(m: re.Match[str]):
        items = [g.strip() for g in m.groups() if g]
        return f"Vector({', '.join(items)})"
    expr = pattern.sub(repl, expr)
    absu = re.findall(r"\|(.*?)\|", expr)
    for s in absu:
        expr = expr.replace(f'|{s}|', f'abs({s})')
    return expr

while True:
    expr = input()
    if expr == 'clear':
        os.system("cls")
        continue
    if expr == 'exit': break
    try:
        if len(expr.split('=')) == 2:
            name = expr.split('=')[0].strip()
            if name == 'x': raise SyntaxError("x is a saved name")
            value = expr.split('=')[1].strip()
            if value[0] == '(' and value[-1] == ')' and ',' in value:
                value = Vector(tuple([eval(pythonize(x.strip()), env) for x in value[1:-1].split(',')]))
            elif '/' in value:
                p, q = [int(x.strip()) for x in value.split('/')]
                value = Rational(p, q)
            elif value == 'Rational': value = readRational()
            elif value == 'Vector': value = readVector(env)
            elif value == 'Matrix': value = readMatrix()
            else: value = eval(pythonize(value), env)
            env[name] = value
        elif expr != '':
            expr = pythonize(expr)
            print(eval(expr, env))
    except (MatrixDimensionsError, DimensionError, ZeroDivisionError, ArithmeticError) as e:
        print(f'\033[91m{e}\033[0m')
