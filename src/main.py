import random

import pygame, sys
from settings import *
from level import Level
from menu import Menu
import os

os.chdir('..')

# Pygame setup
pygame.init()
flags = pygame.SCALED | pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption('Hauntaze')
clock = pygame.time.Clock()
start = False
level = Level()
menu = Menu()

while True:
    # event loop
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_RETURN]:
            start = True

    screen.fill(BG_COLOR)
    if start:
        level.run()
    else:
        menu.update()

    # drawing logic
    pygame.display.update()
    clock.tick(FPS)