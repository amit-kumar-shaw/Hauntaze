import pygame
import sys
# import postprocessing
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game


# pygame initialization
pygame.init()

# initialize controllers
pygame.joystick.init()

# get available joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not bool(joysticks):
    joysticks = None

flags = pygame.SCALED | pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption('Hauntaze')

clock = pygame.time.Clock()

# initialize the game
game = Game(joysticks)

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # run the game
    game.run()

    pygame.display.update()
    clock.tick(FPS)
