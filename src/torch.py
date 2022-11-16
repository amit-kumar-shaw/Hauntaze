import pygame
from settings import *


class Torch(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        t1 = pygame.image.load("./assets/images/player/torch/torch_0.png").convert_alpha()
        t2 = pygame.image.load("./assets/images/player/torch/torch_1.png").convert_alpha()
        t3 = pygame.image.load("./assets/images/player/torch/torch_2.png").convert_alpha()
        t4 = pygame.image.load("./assets/images/player/torch/torch_3.png").convert_alpha()
        t5 = pygame.image.load("./assets/images/player/torch/torch_4.png").convert_alpha()
        t6 = pygame.image.load("./assets/images/player/torch/torch_5.png").convert_alpha()

        self.torch = [pygame.transform.rotozoom(t1, 0, 0.5), pygame.transform.rotozoom(t2, 0, 0.5),
                      pygame.transform.rotozoom(t3, 0, 0.5), pygame.transform.rotozoom(t4, 0, 0.5),
                      pygame.transform.rotozoom(t5, 0, 0.5), pygame.transform.rotozoom(t6, 0, 0.5)]
        self.torch_index = 0

        self.image = self.torch[self.torch_index]

        self.rect = self.image.get_rect(midtop=pos)

    def animate(self):

        self.torch_index += 0.1
        if self.torch_index >= len(self.torch): self.torch_index = 0
        self.image = self.torch[int(self.torch_index)]