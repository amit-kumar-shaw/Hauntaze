import pygame
from random import choice
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, wall):
        super().__init__(groups)
        wall1 = pygame.image.load("./assets/images/tiles/wall1.png").convert_alpha()
        wall2 = pygame.image.load("./assets/images/tiles/wall2.png").convert_alpha()
        wall3 = pygame.image.load("./assets/images/tiles/wall3.png").convert_alpha()
        floor1 = pygame.image.load("./assets/images/tiles/floor1.png").convert_alpha()
        floor2 = pygame.image.load("./assets/images/tiles/floor2.png").convert_alpha()
        floor3 = pygame.image.load("./assets/images/tiles/floor3.png").convert_alpha()
        # self.image = pygame.image.load("./tiles/wall2.png").convert_alpha()
        if wall:
            self.image = choice([wall1, wall1, wall2])
        else:
            self.image = choice([floor1, floor1, floor1, floor1, floor1, floor1, floor1, floor1, floor1, floor3])
        # self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(topleft=pos)
