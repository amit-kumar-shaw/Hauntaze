import pygame
from utilities import import_frames


class Weapon(pygame.sprite.Sprite):
    """player weapons"""
    def __init__(self, pos, groups, collision_sprites, type):
        super().__init__(groups)

        self.type =type

        self.status = 'idle'

        path = f'./assets/images/weapon/{type}/'
        self.frames = {'idle': [], 'attack': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=0.7)

        self.animation_index = 0

        self.image = self.frames[self.status][self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.collision_sprites = collision_sprites

    def animate(self, flipped=False):
        """update weapon frames"""

        status = self.frames[self.status]

        self.animation_index += 0.1

        if self.animation_index >= len(status):
            self.animation_index = 0
            if self.status == 'attack':
                self.status = 'idle'

        self.image = status[int(self.animation_index)]
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)

        if self.status == 'attack':
            self.check_wall_collision()

    def check_wall_collision(self):
        """stop weapon attack when flamethrower collide with walls"""

        for sprite in self.collision_sprites.sprites():
            if self.type == 'flamethrower' and sprite.rect.colliderect(self.rect):
                self.animation_index = 0
                self.status = 'idle'

    def draw(self, screen):
        """draw weapon on screen"""

        screen.blit(self.image, self.rect)
