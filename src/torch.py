import pygame
from utilities import import_frames


class Torch(pygame.sprite.Sprite):
    """player torch"""
    def __init__(self, pos):
        super().__init__()

        self.frames = import_frames("./assets/images/player/torch", scale=0.5)
        self.torch_index = 0

        self.image = self.frames[self.torch_index]
        self.rect = self.image.get_rect(midtop=pos)

    def animate(self):
        """update torch frames"""

        self.torch_index += 0.1
        if self.torch_index >= len(self.frames):
            self.torch_index = 0
        self.image = self.frames[int(self.torch_index)]

    def scale(self, scale):
        """scale torch frames"""
        self.frames = import_frames("./assets/images/player/torch", scale=scale)

    def reset(self):
        """scale torch frames to normal size"""
        self.frames = import_frames("./assets/images/player/torch", scale=0.5)