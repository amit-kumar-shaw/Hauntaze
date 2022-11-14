import random
import time

import pygame
from pygame.locals import *
from player import *
from settings import *

class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./assets/images/enemy_hongtao/tile_0120.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.collision_sprites = collision_sprites


    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

    def movement_update(self):

        Possible_move = ['Left', 'Right', 'Up', 'Down']

        keys = random.choice(Possible_move)

        if keys == 'Left':
            self.direction.x = -1
        elif keys == 'Right':
            self.direction.x = 1
        elif keys == 'Up':
            self.direction.y = -1
        elif keys == 'Down':
            self.direction.y = 1








    def update(self):

        self.movement_update()

        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        self.rect.y += self.direction.y * self.speed
        self.vertical_collisions()




