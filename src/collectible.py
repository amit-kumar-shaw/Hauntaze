import pygame
import random
from utilities import import_frames


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type):
        super().__init__(groups)
        self.type = type
        self.frames = []
        if type == 'coin':
            self.frames = import_frames("./assets/images/coin", scale=0.5)
        elif type == 'torch':
            self.frames = import_frames("./assets/images/big_torch", scale=0.8)

        self.animation_index = random.choice([0, 1, 2, 3])

        self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
