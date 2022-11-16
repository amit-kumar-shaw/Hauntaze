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
level = Level(multiplayer=True)
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
        # display fps
        font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        fps_msg = font.render(f'FPS: {float("{:.2f}".format(clock.get_fps()))}', False, 'white')
        msg_rect = fps_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        screen.blit(fps_msg, msg_rect)
    else:
        menu.update()


    # drawing logic
    pygame.display.update()
    clock.tick(FPS)