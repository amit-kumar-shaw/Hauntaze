import math
from math import sin

import pygame
from pygame.locals import *
from settings import *
from torch import Torch
from  music import PlayerSound

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, collectible_sprites, enemy_sprites, player2=False):
        super().__init__(groups)

        if player2:
            self.player_still = pygame.image.load('./assets/images/player/p2_01.png').convert_alpha()
            self.player_walk_1 = pygame.image.load('./assets/images/player/p2_02.png').convert_alpha()
            self.player_walk_2 = pygame.image.load('./assets/images/player/p2_03.png').convert_alpha()
            # self.image = pygame.image.load("./v1/p1_01.png").convert_alpha()
        else:
            self.player_still = pygame.image.load('./assets/images/player/p1_01.png').convert_alpha()
            self.player_walk_1 = pygame.image.load('./assets/images/player/p1_02.png').convert_alpha()
            self.player_walk_2 = pygame.image.load('./assets/images/player/p1_03.png').convert_alpha()
        # self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.player_walk_1 = pygame.transform.rotozoom(self.player_walk_1, 0, 0.7)
        self.player_walk_2 = pygame.transform.rotozoom(self.player_walk_2, 0, 0.7)
        self.player_still = pygame.transform.rotozoom(self.player_still, 0, 0.7)
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_index = 0

        self.image = self.player_still

        self.rect = self.image.get_rect(topleft=pos)

        self.torch = Torch(pos, groups)
        self.player2 = player2
        self.lives = LIVES
        self.is_alive = True
        self.is_invincible = False
        self.hurt_time = 0
        self.score = 0
        self.key_picked = False
        self.visibility_radius = VISIBILITY_RADIUS
        self.sounds = PlayerSound()
        self.door = None
        self.key = None
        self.level_completed = False


        # player movement
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        self.collision_sprites = collision_sprites
        self.collectible_sprites = collectible_sprites
        self.enemy_sprites = enemy_sprites

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
                    # if self.direction.y <= 0 and ((sprite.rect.bottomleft[1] - self.rect.topright[1]) < 3) and
                    #     pygame.Rect.collidepoint():
                    #     self.rect.topright = sprite.rect.bottomleft #+ (0,1)
                    # if self.direction.y >= 0 and ((self.rect.bottomright[1] - sprite.rect.topleft[1]) < 3):
                    #     self.rect.bottomright = sprite.rect.topleft #- (0,1)
                    # print(sprite.rect.bottomleft, sprite.rect.bottomleft[0])
                    self.rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

    def animate(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.image = self.player_still
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

        if self.is_invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def collectible_collisions(self):
        for sprite in self.collectible_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                self.score += 1
                self.sounds.play_coin_collection()
                sprite.kill()

    def enemy_collisions(self):
        for sprite in self.enemy_sprites.sprites():
            if sprite.rect.colliderect(self.rect) and not self.is_invincible:
                self.is_invincible = True
                self.sounds.play_enemy_collision()
                self.lives -= 1
                self.hurt_time = pygame.time.get_ticks()


    def death_animate(self):
        if self.visibility_radius > 1:
            self.visibility_radius -= 0.5
        else:
            if not self.level_completed:
                self.is_alive = False
                self.torch.kill()
                self.kill()

    def invincibility_timer(self):
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= INVINSIBILITY_DURATION:
                self.is_invincible = False


    def key_collisions(self):
        if self.rect.colliderect(self.key.rect) and not self.key_picked:
            self.sounds.play_key_collection()
            self.key_picked = True
            self.key.kill()

    def door_collisions(self):
        if self.rect.colliderect(self.door.rect) and self.key_picked:
            # self.sounds.play_key_collection()
            self.level_completed = True


    def display_details(self):
        font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        player_name = font.render('Player 1', False, 'white')
        player_rect = player_name.get_rect(midleft=(16, (ROWS*CELL_SIZE*TILE_HEIGHT) + 8))
        hearts_rect = []
        heart = pygame.image.load("./assets/images/heart.png").convert_alpha()
        heart = pygame.transform.rotozoom(heart, 0, 0.75)
        key = pygame.image.load("./assets/images/key/3.png").convert_alpha()
        #key = pygame.transform.rotozoom(key, 0, 0.75)
        key_rect = key.get_rect(bottomleft = player_rect.bottomright)
        for i in range(0,self.lives):
            hearts_rect.append(heart.get_rect(topleft = (16 + (i*12), (ROWS*CELL_SIZE*TILE_HEIGHT) + 14) ))

        coin = pygame.image.load("./assets/images/coin.png").convert_alpha()
        coin_rect = coin.get_rect(topleft=(16, (ROWS * CELL_SIZE * TILE_HEIGHT) + 24))

        score_font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        score_msg = score_font.render(f'{self.score}', False, 'white')
        score_rect = score_msg.get_rect(topleft=(30, (ROWS * CELL_SIZE * TILE_HEIGHT) + 26))

        if self.player2:
            key = pygame.image.load("./assets/images/key/1.png").convert_alpha()
            #key = pygame.transform.rotozoom(key, 0, 0.75)
            player_name = font.render('Player 2', False, 'white')
            player_rect = player_name.get_rect(midright=(SCREEN_WIDTH - 16, (ROWS*CELL_SIZE*TILE_HEIGHT) + 5))
            key_rect = key.get_rect(bottomright=player_rect.bottomleft)
            for i in range(0, self.lives):
                hearts_rect[i] = heart.get_rect(topright=(SCREEN_WIDTH - 16 - (i * 12), (ROWS * CELL_SIZE * TILE_HEIGHT) + 14))
            coin_rect = coin.get_rect(topright=(SCREEN_WIDTH - 16, (ROWS * CELL_SIZE * TILE_HEIGHT) + 24))
            score_rect = score_msg.get_rect(topright=(SCREEN_WIDTH - 30, (ROWS * CELL_SIZE * TILE_HEIGHT) + 26))

        pygame.display.get_surface().blit(player_name, player_rect)
        if self.key_picked:
            pygame.display.get_surface().blit(key, key_rect)
        for i in range(0, self.lives):
            pygame.display.get_surface().blit(heart, hearts_rect[i])
        pygame.display.get_surface().blit(coin, coin_rect)
        pygame.display.get_surface().blit(score_msg, score_rect)


    def update(self):
        if self.lives > 0 and not self.level_completed:
            self.input()
            self.animate()
            self.rect.x += self.direction.x * self.speed
            self.horizontal_collisions()

            self.rect.y += self.direction.y * self.speed
            self.vertical_collisions()
            self.collectible_collisions()
            self.key_collisions()

            self.invincibility_timer()



            self.torch.rect = self.image.get_rect(midtop=(self.rect.x + 2, self.rect.y))
            self.torch.animate()
            self.door_collisions()
            self.enemy_collisions()
        else:
            self.death_animate()

        # self.display_details()


        # font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        # score_msg = font.render(f'Player 1 Score: {self.score}', False, 'white')
        # msg_rect = score_msg.get_rect(midleft=(10, SCREEN_HEIGHT - 10))
        # if self.player2:
        #     score_msg = font.render(f'Player 2 Score: {self.score}', False, 'white')
        #     msg_rect = score_msg.get_rect(midright=(SCREEN_WIDTH -10, SCREEN_HEIGHT - 10))
        #
        # pygame.display.get_surface().blit(score_msg, msg_rect)
