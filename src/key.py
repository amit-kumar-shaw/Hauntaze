import pygame
from utilities import import_frames

class Key(pygame.sprite.Sprite):
    """Each level Key"""
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.frames = import_frames("./assets/images/key", scale=0.75)
        self.animation_index = 0

        self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):
        """update key frames"""

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
