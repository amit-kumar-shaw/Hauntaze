import math
from math import sin

import pygame
from pygame.locals import *
from settings import *
from torch import Torch
from music import PlayerSound
from utilities import import_frames


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, collectible_sprites, enemy_sprites, player2=False):
        super().__init__(groups)

        if player2:
            self.import_assets(2, 0.7)
        else:
            self.import_assets(1, 0.7)

        self.frame_index = 0

        # self.image = self.player_still
        self.status = 'idle'
        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        #self.mask = pygame
        self.is_flipped = False

        self.torch = Torch(pos)
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
        self.ui_update = True

        self.is_big_torch = False
        self.big_torch_time = 0

        self.is_ghost = False

        self.is_attacking = False
        self.weapon_active = False
        self.weapon = None
        self.attack_end_time = 0

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
            self.ATTACK = K_m

        else:
            self.MOVE_LEFT = K_a
            self.MOVE_RIGHT = K_d
            self.MOVE_UP = K_w
            self.MOVE_DOWN = K_s
            self.ATTACK = K_z

    def import_assets(self, player, scale):
        path = f'./assets/images/player/p{player}/'
        self.frames = {'idle': [], 'walk': [], 'dead': [], 'attack': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=scale)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[self.MOVE_RIGHT]:
            self.direction.x = 1
            self.is_flipped = False
        elif keys[self.MOVE_LEFT]:
            self.direction.x = -1
            self.is_flipped = True
        else:
            self.direction.x = 0

        if keys[self.MOVE_UP]:
            self.direction.y = -1
        elif keys[self.MOVE_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[self.ATTACK] and self.weapon_active and pygame.time.get_ticks() - self.attack_end_time >= 00 and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0
            self.status = 'attack'
            self.weapon.status = 'attack'

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
                # if pygame.sprite.spritecollide(player.sprite, obstacle, False, pygame.sprite.collide_mask):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

    def update_status(self):
        if self.is_attacking:
            self.status = 'attack'
        elif self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'
        else:
            self.status = 'walk'

    def animate(self):
        # if self.direction.x == 0 and self.direction.y == 0:
        #     self.image = self.player_still
        # else:
        #     self.frame_index += 0.1
        #     if self.frame_index >= len(self.player_walk): self.frame_index = 0
        #     self.image = self.player_walk[int(self.frame_index)]

        status = self.frames[self.status]

        # loop over frame index
        self.frame_index += 0.1
        if self.frame_index >= len(status):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False
                self.attack_end_time = pygame.time.get_ticks()
            if self.status =='dead':
                self.frame_index = len(status) - 1

        self.image = status[int(self.frame_index)]
        if self.is_flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        # if self.direction.x >= 0:
        #     self.image = image
        # else:
        #     flipped_image = pygame.transform.flip(image, True, False)
        #     self.image = flipped_image

        if self.is_invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def collectible_collisions(self):
        for sprite in self.collectible_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                self.collectible_sprites.remove(sprite)
                if sprite.type == 'coin':
                    self.score += 1
                    self.ui_update = True
                    self.sounds.play_coin_collection()
                    sprite.kill()
                elif sprite.type == 'torch':
                    self.is_big_torch = True
                    self.torch.scale(1)
                    self.big_torch_time = pygame.time.get_ticks()
                    sprite.kill()
                elif sprite.type == 'sword':
                    self.weapon_active = True


    def enemy_collisions(self):
        for sprite in self.enemy_sprites.sprites():
            if sprite.rect.colliderect(self.rect) and not self.is_invincible:
                if self.is_attacking:
                    self.enemy_sprites.remove(sprite)
                    sprite.kill()
                else:
                    self.is_invincible = True
                    self.sounds.play_enemy_collision()
                    self.lives -= 1
                    self.ui_update = True
                    self.hurt_time = pygame.time.get_ticks()

    def death_animate(self):
        if self.visibility_radius >= 1:
            self.visibility_radius -= 0.5
        else:
            if not self.level_completed:
                self.is_alive = False
                self.torch.kill()
                self.kill()
            elif not self.is_ghost:
                self.is_ghost = True

    def invincibility_timer(self):
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= INVINSIBILITY_DURATION:
                self.is_invincible = False

    def key_collisions(self):
        if self.rect.colliderect(self.key.rect) and not self.key_picked:
            self.sounds.play_key_collection()
            self.key_picked = True
            self.ui_update = True
            self.key.kill()

    def door_collisions(self):
        # if self.rect.colliderect(self.door.rect) and self.key_picked:
        if pygame.sprite.collide_rect_ratio(0.3)(self, self.door) and self.key_picked:
            # self.sounds.play_key_collection()
            self.level_completed = True

    def attach_torch(self):
        self.torch.rect = self.torch.image.get_rect(center=(self.rect.x + 2, self.rect.y + 2))

    def update(self):
        if self.lives > 0 and not self.level_completed:
            self.input()
            self.update_status()
            self.animate()
            self.rect.x += self.direction.x * self.speed
            self.horizontal_collisions()

            self.rect.y += self.direction.y * self.speed
            self.vertical_collisions()
            self.collectible_collisions()
            self.key_collisions()

            self.invincibility_timer()

            self.torch.rect = self.torch.image.get_rect(center=(self.rect.x, self.rect.y + 2))
            if self.weapon_active:
                if self.weapon.status == 'idle':
                    self.weapon.rect = self.weapon.image.get_rect(center=(self.rect.x + 6, self.rect.y ))
                else:
                    if self.is_flipped:
                        self.weapon.rect = self.weapon.image.get_rect(midright=self.rect.midleft)
                        self.weapon.animate(flipped=True)
                    else:
                        self.weapon.rect = self.weapon.image.get_rect(midleft=self.rect.midright)
                        self.weapon.animate(flipped=False)
            self.torch.animate()
            if self.is_big_torch:
                self.torch_update()
            self.door_collisions()
            self.enemy_collisions()
        else:
            if not self.status == 'dead' and self.lives == 0:
                self.status = 'dead'
                self.frame_index = 0
            if self.status == 'dead':
                self.animate()
            if self.frame_index >= len(self.frames[self.status]) - 1 and self.status == 'dead':
                self.death_animate()
            if self.level_completed:
                self.death_animate()

    def torch_update(self):
        if pygame.time.get_ticks() - self.big_torch_time < 7000:
            if self.visibility_radius < 2 * VISIBILITY_RADIUS:
                self.visibility_radius += 0.5
        else:
            if self.visibility_radius > VISIBILITY_RADIUS:
                self.visibility_radius -= 0.2
            else:
                self.visibility_radius = VISIBILITY_RADIUS
                self.is_big_torch = False
                self.torch.scale(0.5)

    def reset(self):
        self.visibility_radius = VISIBILITY_RADIUS
        self.level_completed = False
        self.key_picked = False
        self.status = 'idle'
        self.ui_update = True
        self.is_ghost = False

        self.is_attacking = False
        self.weapon_active = False
        self.weapon = None
