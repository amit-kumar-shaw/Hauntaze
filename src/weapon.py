import pygame
from utilities import import_frames


class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type):
        super().__init__(groups)

        self.type =type

        self.status = 'idle'

        path = f'./assets/images/weapon/{type}/'
        self.frames = {'idle': [], 'attack': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=0.75)
        # self.frames = import_frames(f"./assets/images/weapon/{type}", scale=0.75)
        self.animation_index = 0

        self.image = self.frames[self.status][self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self, flipped=False):
        status = self.frames[self.status]

        self.animation_index += 0.1

        if self.animation_index >= len(status):
            self.animation_index = 0
            if self.status == 'attack':
                self.status = 'idle'
        # if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = status[int(self.animation_index)]
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        screen.blit(self.image, self.rect)