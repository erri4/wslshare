import math

RawVector = tuple[int, int, int] | tuple[int, int]

class Vector:
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], tuple):
                if len(args[0]) in (2, 3):
                    self.point = args[0]
                else:
                    raise DimensionError("Vector must be 2D or 3D")
            if isinstance(args[0], Vector):
                self.point = args[0].point
        elif len(args) == 2:
            if isinstance(args[0], int) and isinstance(args[1], int):
                self.point = args
        elif len(args) == 3:
            if isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], int):
                self.point = args
        else:
            raise DimensionError("Vector must be 2D or 3D")

    @classmethod
    def nullVector(cls, dim: int):
        if dim not in (2, 3): raise DimensionError("Vector must be 2D or 3D")
        return (0, 0, 0) if dim == 3 else (0, 0)
    
    @classmethod
    def twoPoints(cls, start: "Vector | RawVector", end: "Vector | RawVector"):
        return cls(Vector(start) - Vector(end))
    
    def __add__(self, other: "Vector | RawVector"):
        if isinstance(other, Vector):
            if self.dim == other.dim:
                return Vector((self.x + other.x, self.y + self.y)) if self.dim == 2 else Vector((self.x + other.x, self.y + other.y, self[2] + other[2]))
            else: raise DimensionError("Cannot add vectors: vectors has to be the same dimensions")
        if isinstance(other, tuple):
            if all([isinstance(x, int) for x in other]):
                if len(other) == self.dim:
                    return Vector((self.x + other[0], self.y + other[1])) if self.dim == 2 else Vector((self.x + other[0], self.y + other[1], self[2] + other[2]))
                else: raise DimensionError("Cannot add vectors: vectors has to be the same dimensions")
                
    def __radd__(self, other: RawVector):
        if isinstance(other, tuple):
            if all([isinstance(x, int) for x in other]):
                if len(other) == self.dim:
                    return Vector((self.x + other[0], self.y + other[1])) if self.dim == 2 else Vector((self.x + other[0], self.y + other[1], self[2] + other[2]))
                else: raise DimensionError("Cannot add vectors: vectors has to be the same dimensions")

    def __mul__(self, other: "Vector | RawVector | int"):
        if isinstance(other, int):
            return Vector(tuple([x * other for x in self.point]))
        if isinstance(other, float):
            if int(other) == other: other = int(other)
            return Vector(tuple([x * other for x in self.point]))
        if isinstance(other, Vector):
            if self.dim == other.dim:
                return self.x * other.x + self.y * other.y + (0 if self.dim == 2 else (self.z * other.z))
            raise DimensionError("Cannot dot product vectors: vectors has to be the same dimensions")
        if isinstance(other, tuple):
            if all([isinstance(x, int) for x in other]):
                if len(other) == self.dim:
                    return self.x * other[0] + self.y * other[1] + (0 if self.dim == 2 else (self.z * other[2]))
                raise DimensionError("Cannot dot product vectors: vectors has to be the same dimensions")

    def __rmul__(self, other: "RawVector | int"):
        return self * other

    def __matmul__(self, other: "Vector | RawVector"):
        if isinstance(other, Vector):
            if self.dim == other.dim:
                if self.dim == 2: return self.x * other.y - self.y * other.x
                return Vector((Vector(self.y, self.z)@Vector(other.y, other.z), -(Vector(self.x, self.z)@Vector(other.x, other.z)), Vector(self.x, self.y)@Vector(other.x, other.y)))
            raise DimensionError("Cannot cross product vectors: vectors has to be the same dimensions")
        if isinstance(other, tuple):
            if all([isinstance(x, int) for x in other]):
                if len(other) == self.dim:
                    if self.dim == 2: return self.x * other[1] - self.y * other[0]
                    return Vector((Vector(self.y, self.z)@Vector(other[1], other[2]), -(Vector(self.x, self.z)@Vector(other[0], other[2])), Vector(self.x, self.y)@Vector(other[0], other[1])))
                raise DimensionError("Cannot cross product vectors: vectors has to be the same dimensions")
    
    def __rmatmul__(self, other: "RawVector"):
        return Vector(other) @ self

    def angle(self, other: "Vector | RawVector"):
        if isinstance(other, Vector):
            if self.dim == other.dim:
                return math.acos(abs(self * other) / (abs(self) * abs(other)))
            raise DimensionError("Cannot find angle between vectors: vectors has to be the same dimensions")
        if isinstance(other, tuple):
            if all([isinstance(x, int) for x in other]):
                if len(other) == self.dim:
                    return math.acos(abs(self * other) / (abs(self) * math.sqrt(other[0] ** 2 + other[1] ** 2 + (0 if self.dim == 2 else other[2]) ** 2)))
                raise DimensionError("Cannot find angle between vectors: vectors has to be the same dimensions")
            
    def projection(self, other: "Vector | RawVector"):
        return ((self * Vector(other)) / (abs(Vector(other)) ** 2)) * Vector(other)

    def __floordiv__(self, other: "Vector | RawVector"):
        return self.projection(other)
    
    def __truediv__(self, other: int):
        return self * (1 / other)

    def __getitem__(self, key: int):
        return self.point[key]
    
    @property
    def dim(self):
        return len(self.point)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]
    
    @property
    def z(self):
        if self.dim < 3: raise DimensionError("Vector does not have z value")
        return self[2]
    
    @property
    def norm(self):
        return abs(self)
    
    @property
    def theta(self):
        if self.dim == 3: raise DimensionError("3D vector does not have an angle")
        return math.atan2(self.y, self.x)
    
    @x.setter
    def x(self, value: int):
        if self.dim == 3:
            self.point = (value, self[1], self[2])
        else:
            self.point = (value, self[1])

    @y.setter
    def y(self, value: int):
        if self.dim == 3:
            self.point = (self[0], value, self[2])
        else:
            self.point = (self[0], value)

    @z.setter
    def z(self, value: int):
        if self.dim < 3: raise DimensionError("Vector does not have z value")
        self.point = (self[0], self[1], value)
    
    @z.deleter
    def z(self):
        if self.dim < 3: raise DimensionError("Vector does not have z value")
        self.point = (self[0], self[1])

    @norm.setter
    def norm(self, value: int):
        self.point = (~self * value).point

    @theta.setter
    def theta(self, value: int):
        if self.dim == 3: raise DimensionError("3D vector does not have an angle")
        norm = self.norm
        self.point = (norm * math.cos(value), norm * math.sin(value))

    def __abs__(self):
        if self.dim == 2: norm = math.sqrt(self.x ** 2 + self.y ** 2)
        else: norm = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        if norm == int(norm): return int(norm)
        return norm

    def __xor__(self, other: "Vector | RawVector"):
        return self.angle(other)

    def __neg__(self):
        return self * -1
    
    def __pos__(self):
        return Vector(self)
    
    def __invert__(self) -> "Vector":
        return self / abs(self)

    def __str__(self):
        return str(self.point)


class DimensionError(Exception): pass

def readVector() -> Vector:
    vec = tuple([int(x) for x in input().split()])
    return Vector(vec)
