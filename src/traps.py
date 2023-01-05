import random

import pygame
from utilities import import_frames


class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        path = f'./assets/images/spikes/'
        self.frames = {'on': [], 'off': [], 'in': [], 'out': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=1)

        self.state = 'off'
        self.animation_index = 0

        self.image = self.frames[self.state][self.animation_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.on_duration = random.choice([4000, 2000, 3000])
        self.on_start_time = 0

        self.off_duration = random.choice([4000, 2000, 3000])
        self.off_start_time = 0

    def animate(self):

        state = self.frames[self.state]

        self.animation_index += 0.05
        if self.animation_index >= len(state):
            self.animation_index = 0
            if self.state == 'in':
                self.state = 'off'
                self.off_start_time = pygame.time.get_ticks()
            elif self.state == 'out':
                self.state = 'on'
                self.on_start_time = pygame.time.get_ticks()
        self.image = state[int(self.animation_index)]

    def update(self):
        self.animate()
        if self.state == 'off' and pygame.time.get_ticks() - self.off_start_time > self.off_duration:
            self.state = 'out'
            self.animation_index = 0
        elif self.state == 'on' and pygame.time.get_ticks() - self.on_start_time > self.on_duration:
            self.state = 'in'
            self.animation_index = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)