import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./assets/images/wall3.png").convert_alpha()
        # self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(topleft=pos)
