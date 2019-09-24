# Created on 23 September 2019

import sys
import pygame
from pygame.locals import *
from GameDriver import GameDriver

pygame.init()

dim = (3, 3)
width = 100
w, h = dim[0] * width, dim[1] * width
display = pygame.display.set_mode((w, h))
pygame.display.set_caption("Slider")

driver = GameDriver(dim, width)
driver.drawBoard(display)

won = False
time = pygame.time.get_ticks()
while True:
    events = pygame.event.get()

    if QUIT in [e.type for e in events]:
        pygame.quit()
        sys.exit(0)

    if not won:
        dt = pygame.time.get_ticks() - time
        time = pygame.time.get_ticks()
        won = driver.run(display, events, dt)
        if won:
            surface = pygame.Surface((w, h))
            surface.set_alpha(128)
            display.blit(surface, (0, 0))
            img = pygame.image.load("won.png")
            width = int(min(w, h) / 5)
            img = pygame.transform.scale(img, (width, width))
            display.blit(img, (int((w - width) / 2), int((h - width) / 2)))

    pygame.display.update()
