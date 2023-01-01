import pygame
from utilities import import_frames


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()

        self.type = type

        self.active = False

        self.frames = import_frames(f"./assets/images/stones/{type}", scale=0.75)
        self.animation_index = 0

        self.image = pygame.image.load(f"./assets/images/stones/{type}.png").convert()
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def animate(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]


class StonesUI:
    def __init__(self):

        height = 24

        self.surface = pygame.Surface((64, height))
        self.rect = self.surface.get_rect(topleft=(576, 0))

        y = (height - 18) / 2

        self.stones = []
        self.stones.append(Stone((2, y), 'life'))
        self.stones.append(Stone((22, y), 'death'))
        self.stones.append(Stone((42, y), 'curse'))

    def update(self):
        for stone in self.stones:
            if stone.active:
                stone.animate()
            self.surface.blit(stone.image, stone.rect)
        pygame.display.get_surface().blit(self.surface, self.rect)
        self.surface.fill('black')
