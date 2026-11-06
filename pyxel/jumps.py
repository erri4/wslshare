from math import isclose
import pyxel

GROUND_LEVEL = 100
GRAVITY = 0.1
WALL_LEFT = 0
WALL_RIGHT = 152

class App:
    double_jump: bool = True
    keyup_released: bool = True

    def __init__(self):
        pyxel.init(160, 120, title="Test")
        
        self.x = 76
        self.y = GROUND_LEVEL
        self.vy = 0
        self.vx = 0
        self.ax = 0
        self.double_jump = True
        self.keyup_released = True
        
        pyxel.run(self.update, self.draw)

    def is_touching_solid(self):
        sgn = 0
        sgn -= self.x <= WALL_LEFT
        sgn += self.x >= WALL_RIGHT
        if self.y >= GROUND_LEVEL: sgn = 0
        return (self.y >= GROUND_LEVEL or self.x <= WALL_LEFT or self.x >= WALL_RIGHT, sgn)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.y -= self.vy
        self.x -= self.vx
        self.vx += self.ax
        if isclose(self.vx, 0, abs_tol=1e-9):
            self.vx = 0
            self.ax = 0
        if self.ax >= 0 and self.vx > 0:
            self.ax = 0
            self.vx = 0
        if self.ax <= 0 and self.vx < 0:
            self.ax = 0
            self.vx = 0
        solid = self.is_touching_solid()
        if not (solid[0] and solid[1] == 0):
            self.vy -= GRAVITY
        else:
            match solid[1]:
                case 0:
                    self.y = GROUND_LEVEL
                    self.double_jump = True
                    self.vy = 0
                case 1:
                    self.x = WALL_RIGHT
                    self.double_jump = True
                case -1:
                    self.x = WALL_LEFT
                    self.double_jump = True
        if self.x >= WALL_RIGHT:
            self.x = WALL_RIGHT
            self.double_jump = True
        if self.x <= WALL_LEFT:
            self.x = WALL_LEFT
            self.double_jump = True
        if pyxel.btn(pyxel.KEY_LEFT) and solid[1] != -1 and (not self.x <= WALL_LEFT):
            self.vx = 2
            if self.ax <= 0: self.ax = -0.1
        if pyxel.btn(pyxel.KEY_RIGHT) and solid[1] != 1 and (not self.x >= WALL_RIGHT):
            self.vx = -2
            if self.ax >= 0: self.ax = 0.1
        if pyxel.btn(pyxel.KEY_UP) and solid[0] and self.keyup_released:
            self.vy = 2
            self.keyup_released = False
            self.vx = 2 * solid[1]
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
        pyxel.rect(self.x, self.y, 8, 8, 11)

App()