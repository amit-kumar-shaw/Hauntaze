import pygame
from random import choice
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, wall):
        super().__init__(groups)

        wall1 = pygame.image.load("./assets/images/tiles/tile_1.png").convert_alpha()
        wall2 = pygame.image.load("./assets/images/tiles/tile_2.png").convert_alpha()
        wall3 = pygame.image.load("./assets/images/tiles/tile_3.png").convert_alpha()
        wall4 = pygame.image.load("./assets/images/tiles/tile_4.png").convert_alpha()
        wall5 = pygame.image.load("./assets/images/tiles/tile_5.png").convert_alpha()
        wall6 = pygame.image.load("./assets/images/tiles/tile_6.png").convert_alpha()
        floor1 = pygame.image.load("./assets/images/tiles/floor_1.png").convert_alpha()
        floor2 = pygame.image.load("./assets/images/tiles/floor_2.png").convert_alpha()
        floor3 = pygame.image.load("./assets/images/tiles/floor_3.png").convert_alpha()
        floor4 = pygame.image.load("./assets/images/tiles/floor_4.png").convert_alpha()

        if wall:
            self.image = choice([wall1, wall2, wall3, wall4, wall5, wall6])
        else:
            self.image = choice([floor1, floor1, floor1, floor1, floor1, floor1, floor2, floor3, floor4])

        self.rect = self.image.get_rect(topleft=pos)
