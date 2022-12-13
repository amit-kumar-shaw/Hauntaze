import pygame
from settings import *
from utilities import import_frames


class Torch(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.frames = import_frames("./assets/images/player/torch", scale=0.5)
        self.torch_index = 0

        self.image = self.frames[self.torch_index]

        self.rect = self.image.get_rect(midtop=pos)


    def animate(self):

        self.torch_index += 0.1
        if self.torch_index >= len(self.frames): self.torch_index = 0
        self.image = self.frames[int(self.torch_index)]

    def scale(self, scale):
        self.frames = import_frames("./assets/images/player/torch", scale=scale)

    def reset(self):
        self.frames = import_frames("./assets/images/player/torch", scale=0.5)