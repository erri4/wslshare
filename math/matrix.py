RawMatrix = list[list[int]]

class Matrix:
    mat: RawMatrix

    def __init__(self, mat: "RawMatrix | Matrix"):
        if isinstance(mat, Matrix):
            self.mat = [row[:] for row in mat.mat]
            return
        mx = max(len(row) for row in mat)

        for row in mat:
            row += [0] * (mx - len(row))
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if round(mat[i][j]) == mat[i][j]:
                    mat[i][j] = round(mat[i][j])
        self.mat = mat

    @classmethod
    def Id(cls, n: int):
        mat = [[0]*n]*n
        mat = [row[:] for row in mat]
        for i in range(n):
            mat[i][i] = 1
        return cls(mat)
    
    @property
    def col(self):
        if self.row == 0: return 0
        return len(self[0])
    
    @property
    def row(self):
        return len(self.mat)

    def __add__(self, other: "Matrix"):
        if not isinstance(other, Matrix): raise TypeError
        if other.row != self.row or other.col != self.col: raise MatrixDimensionsError("Cannot add matrices: matrices has to be the same dimensions")
        mat: list[list[int]] = []
        for i in range(self.row):
            mat.append([])
            for j in range(self.col):
                mat[i].append(self[i][j] + other[i][j])
        return Matrix(mat)
    
    def __sub__(self, other: "Matrix"):
        if not isinstance(other, Matrix): raise TypeError
        if other.row != self.row or other.col != self.col: raise MatrixDimensionsError("Cannot substruct matrices: matrices has to be the same dimensions")
        mat: list[list[int]] = []
        for i in range(self.row):
            mat.append([])
            for j in range(self.col):
                mat[i].append(self[i][j] - other[i][j])
        return Matrix(mat)
    
    def __mul__(self, other: "Matrix | int"):
        if isinstance(other, int):
            return Matrix([[(x * other) for x in row] for row in self.mat])
        if isinstance(other, Matrix):
            if other.row != self.col: raise MatrixDimensionsError("Cannot multiply matrices: first matrix has to have the same columns as rows of the second matrix")
            mat = [[0] * other.col for _ in range(self.row)]

            for i in range(self.row):
                for j in range(other.col):
                    mat[i][j] = sum(self[i][k] * other[k][j] for k in range(self.col))
            return Matrix(mat)
        raise TypeError
    
    def __rmul__(self, other: int):
        if not isinstance(other, int): raise TypeError
        return self * other
    
    def __eq__(self, other: "Matrix | RawMatrix"):
        if isinstance(other, Matrix):
            return self.mat == other.mat
        return self.mat == other
    
    def __getitem__(self, key: int):
        if isinstance(key, tuple):
            r,c = key
            return self.mat[r][c]
        return self.mat[key]

    def __str__(self):
        '⌊⌋⌈⌉|'
        if self.row == 1: return f'[{' '.join([str(x) for x in self.mat[0]])}]'
        res = '⌈'
        res += ' '.join([str(x) for x in self.mat[0]]) + '⌉\n'
        for i in range(1, self.row - 1):
            res += '|' + ' '.join([str(x) for x in self.mat[i]]) + '|\n'
        res += '⌊' + ' '.join([str(x) for x in self.mat[-1]]) + '⌋'
        return res
    
    def det(self) -> int:
        if self.row != self.col:
            raise MatrixDimensionsError("Cannot find determinant: matrix must be a square")

        n = self.row
        mat = [row[:] for row in self.mat]
        det = 1
        swaps = 0

        for i in range(n):

            if mat[i][i] == 0:
                for r in range(i+1, n):
                    if mat[r][i] != 0:
                        mat[i], mat[r] = mat[r], mat[i]
                        swaps += 1
                        break
                else:
                    return 0

            pivot = mat[i][i]

            for r in range(i+1, n):
                factor = mat[r][i] / pivot
                for c in range(i, n):
                    mat[r][c] -= factor * mat[i][c]

        for i in range(n):
            det *= mat[i][i]

        if swaps % 2:
            det = -det

        return round(det) if det == round(det) else det
    
    def __invert__(self):
        if self.row != self.col: raise MatrixDimensionsError("Cannot find inverse: matrix must be a square")
        aug = [row[:] + [1 if i == j else 0 for j in range(self.row)] for i,row in enumerate(self.mat)]

        for i in range(self.row):
            if aug[i][i] == 0:
                for r in range(i+1, self.row):
                    if aug[r][i] != 0:
                        aug[i], aug[r] = aug[r], aug[i]
                        break
                else:
                    raise MatrixDimensionsError("Matrix not invertible: determinant is 0")

            pivot = aug[i][i]

            for j in range(2*self.row):
                aug[i][j] /= pivot
                if round(aug[i][j])*pivot == aug[i][j]*pivot:
                    aug[i][j] = round(aug[i][j])

            for r in range(self.row):
                if r != i:
                    factor = aug[r][i]
                    for c in range(2*self.row):
                        aug[r][c] -= factor * aug[i][c]

        mat = [row[self.row:] for row in aug]
        return Matrix(mat)
    
    def __pow__(self, n: int):
        if self.row != self.col: raise MatrixDimensionsError("Cannot raise to power: matrix must be a square")
        A = self
        if n < 0:
            A = ~self
            n = -n
        binb = [bool(int(x)) for x in list(bin(n)[2:])]
        binb.reverse()
        c = Matrix.Id(self.row)
        binc = []
        for j in range(len(binb)):
            if j == 0:
                binc.append(A)
            else:
                binc.append(binc[j - 1] * binc[j - 1])
        for j in range(len(binc)):
            if binb[j]:
                c *= binc[j]
        return c

    def __neg__(self):
        return self * -1
    
    def __pos__(self):
        return Matrix(self)
    
    def T(self):
        return Matrix(list(map(list, zip(*self.mat))))
    
    def __abs__(self):
        return self.det()
    
class MatrixDimensionsError(Exception): pass

def readMatrix() -> Matrix:
    mat = []
    while True:
        try:
            row = [int(x) for x in input().split()]
            if row == []: break
            mat.append(row)
        except ValueError:
            break

    return Matrix(mat)
