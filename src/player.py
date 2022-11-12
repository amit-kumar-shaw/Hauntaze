import pygame
from pygame.locals import *
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, player2=False):
        super().__init__(groups)
        if player2:
            self.image = pygame.image.load("./assets/images/player_hongtao/tile_0098.png").convert_alpha()
        else:
            self.image = pygame.image.load("./assets/images/player_hongtao/tile_0097.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.collision_sprites = collision_sprites

        # player keys
        if player2:
            self.MOVE_LEFT = K_LEFT
            self.MOVE_RIGHT = K_RIGHT
            self.MOVE_UP = K_UP
            self.MOVE_DOWN = K_DOWN

        else:
            self.MOVE_LEFT = K_a
            self.MOVE_RIGHT = K_d
            self.MOVE_UP = K_w
            self.MOVE_DOWN = K_s

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[self.MOVE_RIGHT]:
            self.direction.x = 1
        elif keys[self.MOVE_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[self.MOVE_UP]:
            self.direction.y = -1
        elif keys[self.MOVE_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

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

    def update(self):
        self.input()

        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()

        self.rect.y += self.direction.y * self.speed
        self.vertical_collisions()
        
