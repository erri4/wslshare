from math import isclose
import pyxel

X_SIZE = 128
Y_SIZE = 128

GRAVITY = 0.1

SQ_SIZE = 8

GROUND_LEVEL = Y_SIZE - SQ_SIZE
WALL_RIGHT = X_SIZE - SQ_SIZE
WALL_LEFT = 0

HARMFUL = [(1, 0)]

WALLS = [(0, 1)]

WINNING = [(2, 2), (2, 1), (1, 1), (1, 2)]

TOP = 1j
LEFT = -1
BOTTOM = -1j
RIGHT = 1
NOT_TOUCHING = 0

class App:
    double_jump: bool = True
    keyup_released: bool = True
    hitbox: bool = False
    won: bool = False

    def __init__(self, hitbox: bool = False):
        pyxel.init(X_SIZE, Y_SIZE, title="Test")
        pyxel.load('./map.pyxres')
        
        self.x = WALL_LEFT
        self.y = GROUND_LEVEL
        self.vy = 0
        self.vx = 0
        self.ax = 0
        self.double_jump = True
        self.keyup_released = True
        self.won = False
        self.hitbox = hitbox
        
        pyxel.run(self.update, self.draw)

    def is_touching_solid(self):
        if self.y >= GROUND_LEVEL: return BOTTOM
        if isclose(self.y, GROUND_LEVEL, abs_tol=1e-5): return BOTTOM
        if self.x <= WALL_LEFT: return LEFT
        if isclose(self.x, WALL_LEFT, abs_tol=1e-5): return LEFT
        if self.get_tile(self.x, self.y) in WALLS: return LEFT
        if self.x >= WALL_RIGHT: return RIGHT
        if isclose(self.x, WALL_RIGHT, abs_tol=1e-5): return RIGHT
        if self.get_tile(self.x + SQ_SIZE, self.y) in WALLS: return RIGHT
        if self.get_tile(self.x, self.y + SQ_SIZE) in WALLS or self.get_tile(self.x + SQ_SIZE, self.y + SQ_SIZE) in WALLS: return BOTTOM
        return NOT_TOUCHING

    def get_tile(self, x: int, y: int, tilemap_index: int = 0):
        if self.won:
            x += 128
        tile_x = x // 8
        tile_y = y // 8
        return pyxel.tilemaps[tilemap_index].pget(tile_x, tile_y)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if self.get_tile(self.x, self.y) in HARMFUL or self.get_tile(self.x + SQ_SIZE, self.y) in HARMFUL or self.get_tile(self.x, self.y + SQ_SIZE) in HARMFUL or self.get_tile(self.x + SQ_SIZE, self.y + SQ_SIZE) in HARMFUL:
            self.x = WALL_LEFT
            self.y = GROUND_LEVEL

        if self.get_tile(self.x, self.y) in WINNING or self.get_tile(self.x + SQ_SIZE, self.y) in WINNING or self.get_tile(self.x, self.y + SQ_SIZE) in WINNING or self.get_tile(self.x + SQ_SIZE, self.y + SQ_SIZE) in WINNING:
            self.x = WALL_LEFT + SQ_SIZE
            self.y = GROUND_LEVEL
            self.won = True

        print(self.is_touching_solid())
        dx, dy = pyxel.tilemaps[0].collide(self.x, self.y, SQ_SIZE, SQ_SIZE, -self.vx, -self.vy, WALLS)
        self.x += dx
        self.y += dy
        self.vx += self.ax
        if isclose(self.vx, 0, abs_tol=1e-5):
            self.vx = 0
            self.ax = 0
        if self.ax >= 0 and self.vx > 0:
            self.ax = 0
            self.vx = 0
        if self.ax <= 0 and self.vx < 0:
            self.ax = 0
            self.vx = 0

        
        solid = self.is_touching_solid()
        if solid:
            self.double_jump = True
        if solid != BOTTOM:
            self.vy -= GRAVITY
        if solid == BOTTOM:
            self.vy = 0
        if self.x >= WALL_RIGHT:
            self.x = WALL_RIGHT
        if self.x <= WALL_LEFT:
            self.x = WALL_LEFT


        if pyxel.btn(pyxel.KEY_LEFT) and solid != LEFT and (not self.x <= WALL_LEFT):
            self.vx = 1
            #if self.ax <= 0: self.ax = -0.1
        if pyxel.btn(pyxel.KEY_RIGHT) and solid != RIGHT and (not self.x >= WALL_RIGHT):
            self.vx = -1
            #if self.ax >= 0: self.ax = 0.1
        if pyxel.btn(pyxel.KEY_UP) and solid and self.keyup_released:
            self.vy = 2
            self.keyup_released = False
            self.vx = 2 * solid.real
            self.ax = -0.05 * self.vx
        if pyxel.btn(pyxel.KEY_UP) and self.double_jump and self.keyup_released:
            self.vy = 2
            self.double_jump = False
            self.keyup_released = False
        if pyxel.btn(pyxel.KEY_DOWN) and self.y < GROUND_LEVEL:
            self.vy -= 1
        if pyxel.btnr(pyxel.KEY_UP):
            self.keyup_released = True

    def draw(self):
        pyxel.cls(0)
        if not self.won: pyxel.bltm(0, 0, 0, 0, 0, X_SIZE, Y_SIZE)
        else: pyxel.bltm(0, 0, 0, 128, 0, X_SIZE, Y_SIZE)
        pyxel.rect(self.x, self.y, SQ_SIZE, SQ_SIZE, 11)
        if self.hitbox:
            pyxel.circ(self.x, self.y, 0.5, 8)
            pyxel.circ(self.x + SQ_SIZE, self.y, 0.5, 8)
            pyxel.circ(self.x, self.y + SQ_SIZE, 0.5, 8)
            pyxel.circ(self.x + SQ_SIZE, self.y + SQ_SIZE, 0.5, 8)

if __name__ == '__main__':
    App()