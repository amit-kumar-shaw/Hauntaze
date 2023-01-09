# import random

import pygame, sys
# import postprocessing
from settings import *
from game import Game


# Pygame setup
pygame.init()

# initialize controllers
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not bool(joysticks):
    joysticks = None


pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
flags = pygame.SCALED | pygame.DOUBLEBUF #| pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption('Hauntaze')
clock = pygame.time.Clock()

game = Game(joysticks)

while True:
    # event loop
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if keys[pygame.K_RETURN] and (menu.is_player1_ready or menu.is_player2_ready):
        #     start = True

    # screen.fill(BG_COLOR, (0, 0, SCREEN_WIDTH, (ROWS * CELL_SIZE * TILE_HEIGHT)))
    game.run()

    # print(clock.get_fps())

    # drawing logic
    pygame.display.update()
    clock.tick(FPS)
