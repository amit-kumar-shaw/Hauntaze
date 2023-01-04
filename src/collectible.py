import pygame
from utilities import import_frames


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type):
        super().__init__(groups)
        self.type = type



        self.frames = {'active': [], 'picked': []}
        if type == 'coin':

            self.frames['active'] = import_frames(f'./assets/images/coin/active', scale=0.5)
            self.frames['picked'] = import_frames(f'./assets/images/coin/picked', scale=2)
            self.pos = tuple(8 + x for x in pos)
        elif type == 'torch':
            self.frames['active'] = import_frames(f'./assets/images/big_torch/active', scale=0.8)
            self.frames['picked'] = import_frames(f'./assets/images/big_torch/picked', scale=2)
            self.pos = tuple(8 + x for x in pos)
        elif type == 'web1':
            self.frames['active'] = import_frames(f'./assets/images/web/web1/active', scale=1)
            self.frames['picked'] = import_frames(f'./assets/images/web/web1/picked', scale=2)
            self.pos = pos
        elif type == 'web2':
            self.frames['active'] = import_frames(f'./assets/images/web/web2/active', scale=1)
            self.frames['picked'] = import_frames(f'./assets/images/web/web2/picked', scale=2)
            self.pos = tuple(2 + x for x in pos)

        elif type == 'mask1' or type == 'mask2':
            self.frames['active'] = import_frames(f'./assets/images/mask/active', scale=1)
            self.frames['picked'] = import_frames(f'./assets/images/mask/picked', scale=2)
            self.pos = tuple(8 + x for x in pos)

        self.status = 'active'

        self.animation_index = 0

        self.image = self.frames[self.status][self.animation_index]

        if self.type == 'web1' or self.type == 'web2':
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            self.rect = self.image.get_rect(center=self.pos)

    def animate(self):

        status = self.frames[self.status]

        self.animation_index += 0.08
        if self.animation_index >= len(status):
            self.animation_index = 0
            if self.status == 'picked':
                self.kill()
        self.image = status[int(self.animation_index)]
        if self.type == 'web1' or self.type == 'web2':
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
