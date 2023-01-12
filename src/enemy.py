import random
import time

import pygame
from pygame.locals import *
from player import *
from settings import *
from utilities import import_frames
from music import EnemySound


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites, player_weapon_sprites, type='None'):
        super().__init__(groups)
        if type == 'None':
            self.type = random.choice(['bat', 'slime', 'skull'])
        else:
            self.type = type

        path = f'./assets/images/enemy/{self.type}/'
        self.frames = {'active': [], 'dead': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=0.75)

        self.status = 'active'

        self.animation_index = random.choice([0, 1, 2, 3])

        self.image = self.frames[self.status][self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.tog = True
        self.collision_sprites = collision_sprites
        self.player_weapon_sprites = player_weapon_sprites
        self.sound = EnemySound()

        self.timer = 5
        self.movement_update()

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                self.movement_update()

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                self.movement_update()

    def movement_update(self):

        Possible_move = ['Left', 'Right', 'Up', 'Down']

        keys = random.choice(Possible_move)

        if keys == 'Left':
            self.direction.x = -1
            self.direction.y = 0
        elif keys == 'Right':
            self.direction.x = 1
            self.direction.y = 0
        elif keys == 'Up':
            self.direction.x = 0
            self.direction.y = -1
        elif keys == 'Down':
            self.direction.x = 0
            self.direction.y = 1

    def animate(self):

        status = self.frames[self.status]

        self.animation_index += 0.1
        if self.animation_index >= len(status):
            self.animation_index = 0
            if self.status == 'dead':
                self.kill()
        self.image = status[int(self.animation_index)]
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)

    def weapon_collisions(self):
        for sprite in self.player_weapon_sprites.sprites():
            if sprite.rect.colliderect(self.rect) and sprite.status == 'attack':
                if pygame.sprite.collide_mask(self, sprite):
                    self.sound.poof.play()
                    self.status = 'dead'
                    self.animation_index = 0

    def update(self):


        self.animate()
        if self.status == 'active':
            random_time = random.choice(range(10, 15))
            self.timer += 0.1
            if self.timer >= random_time:
                self.timer = 0
                self.movement_update()

            if self.tog:
                self.rect.x += self.direction.x * self.speed
            self.horizontal_collisions()
            if self.tog:
                self.rect.y += self.direction.y * self.speed
            self.vertical_collisions()
            self.weapon_collisions()
            self.tog = not self.tog

    def draw(self, screen):
        screen.blit(self.image, self.rect)
