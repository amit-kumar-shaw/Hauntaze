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
        self.speed = PLAYER_SPEED
        self.collision_sprites = collision_sprites

    def move (self):
        if Player.rect.centerx > self.rect.centerx:
            self.direction = 1
            self.rect.x += self.direction.x * self.speed
        if Player.__init__().rect.x > self.rect.x:
            self.direction = -1
            self.rect.x += self.direction.x * self.speed
        if Player.rect.centery > self.rect.centery:
            self.direction = 1
            self.rect.y += self.direction.y * self.speed
        if Player.rect.y > self.rect.y:
            self.direction = -1
            self.rect.y += self.direction.y * self.speed

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


