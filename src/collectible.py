import pygame
import random
from utilities import import_frames


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # t1 = pygame.image.load("./assets/images/coin/1.png").convert_alpha()
        # t2 = pygame.image.load("./assets/images/coin/2.png").convert_alpha()
        # t3 = pygame.image.load("./assets/images/coin/3.png").convert_alpha()
        # t4 = pygame.image.load("./assets/images/coin/4.png").convert_alpha()
        #
        # self.frames = [pygame.transform.rotozoom(t1, 0, 0.5), pygame.transform.rotozoom(t2, 0, 0.5), pygame.transform.rotozoom(t3, 0, 0.5), pygame.transform.rotozoom(t4, 0, 0.5)]

        self.frames = import_frames("./assets/images/coin", scale=0.5)

        self.animation_index = random.choice([0, 1, 2, 3])

        self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]