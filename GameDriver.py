# Created on 23 September 2019

from pygame.locals import *
from pygame.mouse import get_pos
from pygame.draw import rect
from square import Square
from random import randint


class GameDriver:
    def __init__(self, dim, width):
        self.w = width
        self.dim = dim
        self.squares = []
        self.moving = False
        self.pos = (-1, -1)
        self.v = (0, 0)
        self.rect = Rect(0, 0, 0, 0)
        self.time = 0
        self.duration = 200

        for y in range(dim[1]):
            row = []
            for x in range(dim[0]):
                if y == dim[1] - 1 and x == dim[0] - 1:
                    row.append(Square(-1, width))
                else:
                    row.append(Square((y * dim[0]) + (x + 1), width))
            self.squares.append(row)
        self.shuffle()

    def shuffle(self):
        x, y = self.dim[0] - 1, self.dim[1] - 1
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        while self.numCorrect() > 1:
            dx, dy = directions[randint(0, 3)]
            x1, y1 = x + dx, y + dy
            while not (0 <= x1 < self.dim[0] and 0 <= y1 < self.dim[1]):
                dx, dy = directions[randint(0, 3)]
                x1, y1 = x + dx, y + dy
            self.squares[y][x], self.squares[y1][x1] = self.squares[y1][x1], self.squares[y][x]
            x, y = x1, y1

    def numCorrect(self):
        result = 0
        for y, row in enumerate(self.squares):
            for x, s in enumerate(row):
                if (y * self.dim[0]) + x + 1 == s.val or s.val == -1:
                    result += 1
        return result

    def drawBoard(self, display):
        display.fill((0, 0, 0))
        for y, row in enumerate(self.squares):
            for x, square in enumerate(row):
                display.blit(square.surface, (x * self.w, y * self.w))

    def drawSquare(self, display, pos):
        rect(display, (0, 0, 0), (pos[0] * self.w, pos[1] * self.w, self.w, self.w))
        display.blit(self.squares[pos[1]][pos[0]].surface, (pos[0] * self.w, pos[1] * self.w))

    def moveSquare(self, display, dt):
        self.time = min(self.duration, self.time + dt)
        delta = int(self.w * self.time / self.duration)
        rect(display, (0, 0, 0), self.rect)
        r = self.rect.move(delta * self.v[0], delta * self.v[1])
        display.blit(self.squares[self.pos[1]][self.pos[0]].surface, r)
        if self.time == self.duration:
            x, y = self.pos
            x1, y1 = x + self.v[0], y + self.v[1]
            self.squares[y][x], self.squares[y1][x1] = self.squares[y1][x1], self.squares[y][x]
            self.pos = (-1, -1)
            self.moving = False
            if self.numCorrect() == self.dim[0] * self.dim[1]:
                return True
        return False

    def run(self, display, events, dt):
        if self.moving:
            return self.moveSquare(display, dt)
        else:
            for e in events:
                if e.type == MOUSEBUTTONUP:
                    pos = get_pos()
                    x, y = int(pos[0] / self.w), int(pos[1] / self.w)
                    val = self.squares[y][x].val
                    if val != -1:
                        if (x, y) == self.pos:
                            space = self.getAdjacentSpace((x, y))
                            if space != None:
                                self.time = 0
                                self.v = (space[0] - x, space[1] - y)
                                self.rect = Rect(x * self.w, y * self.w, self.w, self.w)
                                self.moving = True
                        else:
                            self.drawSquare(display, self.pos)
                            rect(display, (0, 255, 0), (x * self.w, y * self.w, self.w, self.w), 1)
                            self.pos = (x, y)
        return False

    def getAdjacentSpace(self, pos):
        for p in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x = pos[0] + p[0]
            y = pos[1] + p[1]
            if 0 <= x < self.dim[0] and 0 <= y < self.dim[1] and self.squares[y][x].val == -1:
                return (x, y)
