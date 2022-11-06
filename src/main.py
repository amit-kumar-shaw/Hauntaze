import pygame, sys
from settings import *
from level import Level
from music import GameSound
import os

os.chdir('..')

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hauntaze')
clock = pygame.time.Clock()
sound = GameSound()
sound.playbackgroundmusic()
level = Level()

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)
    level.run()

    # drawing logic
    pygame.display.update()
    clock.tick(60)