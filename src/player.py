from math import sin
import pygame
from settings import *
from torch import Torch
from sounds import PlayerSound
from utilities import import_frames


class Player(pygame.sprite.Sprite):
    """ player sprite for the game """

    def __init__(self, pos, groups, collision_sprites, collectible_sprites, enemy_sprites, joystick=None,
                 player2=False):
        super().__init__(groups)

        self.joystick = joystick

        # import player assets
        if player2:
            self.import_assets(2, 0.7)
        else:
            self.import_assets(1, 0.7)

        self.frame_index = 0

        self.status = 'idle'
        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.mask = pygame.mask.from_surface(self.image)
        self.is_flipped = False

        # special stones for story mode
        self.life_stone_available = False
        self.death_stone_available = False
        self.life_stone_activated = False
        self.death_stone_activated = False

        # for revival option in story mode
        self.wait_revival = False
        self.revival_position = None
        self.revival_time = 0
        self.time_frames = import_frames('./assets/images/player/numbers', 1)
        self.timer = self.time_frames[10]
        self.timer_rect = self.timer.get_rect(center=self.rect.center)

        # instantiate torch sprite
        self.torch = Torch(pos)

        self.sounds = PlayerSound()

        self.player2 = player2
        self.lives = PLAYER_LIVES
        self.is_alive = True
        self.is_invincible = False
        self.hurt_time = 0
        self.mask_time = 0
        self.move = True
        self.is_slow = False
        self.web_time = 0
        self.web = pygame.image.load('./assets/images/web/web2.png').convert_alpha()
        self.score = 0
        self.key_active = True
        self.key_picked = False
        self.visibility_radius = VISIBILITY_RADIUS
        self.door = None
        self.key = None
        self.level_completed = False
        self.ui_update = True

        self.is_big_torch = False
        self.big_torch_time = 0

        self.is_ghost = False

        # for weapon
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
        self.trap_sprites = None

        # player keys
        if player2:
            self.MOVE_LEFT = PLAYER2_MOVE_LEFT
            self.MOVE_RIGHT = PLAYER2_MOVE_RIGHT
            self.MOVE_UP = PLAYER2_MOVE_UP
            self.MOVE_DOWN = PLAYER2_MOVE_DOWN
            self.ATTACK = PLAYER2_ATTACK
            self.DEATH_STONE = PLAYER2_DEATH
            self.LIFE_STONE = PLAYER2_LIFE

        else:
            self.MOVE_LEFT = PLAYER1_MOVE_LEFT
            self.MOVE_RIGHT = PLAYER1_MOVE_RIGHT
            self.MOVE_UP = PLAYER1_MOVE_UP
            self.MOVE_DOWN = PLAYER1_MOVE_DOWN
            self.ATTACK = PLAYER1_ATTACK
            self.DEATH_STONE = PLAYER1_DEATH
            self.LIFE_STONE = PLAYER1_LIFE

    def import_assets(self, player, scale):
        """import player assets"""
        path = f'./assets/images/player/p{player}/'
        self.frames = {'idle': [], 'walk': [], 'dead': [], 'attack': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=scale)

    def input(self):
        """ check user input """
        keys = pygame.key.get_pressed()

        if keys[self.MOVE_RIGHT] or (
                self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) > AXIS_THRESHOLD):
            self.direction.x = 1
            self.is_flipped = False
        elif keys[self.MOVE_LEFT] or (
                self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) < -AXIS_THRESHOLD):
            self.direction.x = -1
            self.is_flipped = True
        else:
            self.direction.x = 0

        if keys[self.MOVE_UP] or (self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) < -AXIS_THRESHOLD):
            self.direction.y = -1
        elif keys[self.MOVE_DOWN] or (
                self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) > AXIS_THRESHOLD):
            self.direction.y = 1
        else:
            self.direction.y = 0

        if (keys[self.ATTACK] or (self.joystick is not None and self.joystick.get_button(
            BLACK_BUTTON))) and self.weapon_active and pygame.time.get_ticks() - self.attack_end_time >= ATTACK_DELAY and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0
            self.status = 'attack'
            self.weapon.status = 'attack'
            if self.weapon.type == 'sword':
                self.sounds.sword.play()
            elif self.weapon.type == 'flamethrower':
                self.sounds.flamethrower.play()

        if (keys[self.DEATH_STONE] or (
                self.joystick is not None and self.joystick.get_button(YELLOW_BUTTON))) and self.death_stone_available:
            self.death_stone_activated = True

    def revival_input(self):
        """ check revival input only after player dies """
        keys = pygame.key.get_pressed()
        if (keys[self.LIFE_STONE] or (
                self.joystick is not None and self.joystick.get_button(BLUE_BUTTON))) and self.life_stone_available:
            self.life_stone_activated = True
            self.sounds.revive.play()

    def horizontal_collisions(self):
        """ check left/right wall collisions """
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

    def vertical_collisions(self):
        """ check top/bottom wall collisions """
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

    def update_status(self):
        """ update player status """
        if self.is_attacking:
            self.status = 'attack'
        elif self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'
        else:
            self.status = 'walk'

    def animate(self):
        """ update player frame """

        status = self.frames[self.status]

        # loop over frame index
        self.frame_index += 0.1
        if self.frame_index >= len(status):
            self.frame_index = 0
            if self.is_attacking and not self.weapon.status == 'attack':
                self.is_attacking = False
                self.attack_end_time = pygame.time.get_ticks()
            if self.status == 'dead':
                self.frame_index = len(status) - 1

        self.image = status[int(self.frame_index)]

        if self.is_flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        # update player alpha value when invincible
        if self.is_invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def wave_value(self):
        """ player alpha value during invincibility """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def collectible_collisions(self):
        """ pick collectibles on collision """

        for sprite in self.collectible_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if sprite.type == 'coin' and sprite.status == 'active':
                    self.score += 1
                    self.ui_update = True
                    self.sounds.coin_collection.play()
                    sprite.status = 'picked'
                    sprite.animation_index = 0
                    # sprite.kill()
                elif sprite.type == 'torch' and sprite.status == 'active':
                    self.is_big_torch = True
                    self.torch.scale(1)
                    self.big_torch_time = pygame.time.get_ticks()
                    self.sounds.special_item.play()
                    sprite.status = 'picked'
                    sprite.animation_index = 0
                elif (sprite.type == 'web1' or sprite.type == 'web2') and not self.is_invincible and sprite.status == 'active':
                    sprite.status = 'picked'
                    sprite.animation_index = 0
                    self.sounds.trap.play()
                    self.is_slow = True
                    self.web_time = pygame.time.get_ticks()
                elif sprite.type == 'mask1' or sprite.type == 'mask2' and sprite.status == 'active':
                    sprite.status = 'picked'
                    sprite.animation_index = 0
                    self.sounds.special_item.play()
                    self.is_invincible = True
                    self.mask_time = pygame.time.get_ticks()

    def enemy_collisions(self):
        """ check enemy collision """

        for sprite in self.enemy_sprites.sprites():
            if sprite.rect.colliderect(self.rect) and not self.is_invincible and sprite.status != 'dead':
                if pygame.sprite.collide_mask(self, sprite):
                    self.is_invincible = True
                    self.sounds.enemy_collision.play()
                    self.lives -= 1
                    if self.lives == 0 and self.weapon_active:
                        self.weapon.status = 'idle'
                        self.weapon.animation_index = 0
                    self.ui_update = True
                    self.hurt_time = pygame.time.get_ticks()

    def trap_collisions(self):
        """ check collision with spikes """
        for sprite in self.trap_sprites.sprites():
            if sprite.rect.colliderect(self.rect) and not self.is_invincible and not sprite.state == 'off':
                if pygame.sprite.collide_mask(self, sprite):
                    self.is_invincible = True
                    self.sounds.enemy_collision.play()
                    self.lives -= 1
                    if self.lives == 0 and self.weapon_active:
                        self.weapon.status = 'idle'
                        self.weapon.animation_index = 0
                    self.ui_update = True
                    self.hurt_time = pygame.time.get_ticks()

    def death_animate(self):
        """ animate when played dies"""
        if self.visibility_radius >= 1:
            self.visibility_radius -= 0.5
        else:
            if not self.level_completed:
                if self.life_stone_available:
                    self.wait_revival = True
                    self.revival_time = pygame.time.get_ticks()
                else:
                    self.is_alive = False
                    self.sounds.die.play()
                    self.torch.kill()
                    if self.weapon_active:
                        self.weapon.kill()
                    self.kill()

            elif not self.is_ghost:
                self.is_ghost = True

    def invincibility_timer(self):
        """ disable invincibility after 5 secs """
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if (current_time - self.hurt_time >= INVINSIBILITY_DURATION) and (current_time - self.mask_time >= 5000):
                self.is_invincible = False

    def weapon_collisions(self):
        """ pick weapon """

        if self.weapon is not None and self.rect.colliderect(self.weapon.rect) and not self.weapon_active:
            self.sounds.special_item.play()
            self.weapon_active = True

    def key_collisions(self):
        """ pick key """

        if self.rect.colliderect(self.key.rect) and not self.key_picked:
            self.sounds.key_collection.play()
            self.key_picked = True
            self.ui_update = True
            self.key.kill()

    def door_collisions(self):
        """ check door collision and level complete on collision """

        if pygame.sprite.collide_rect_ratio(0.8)(self, self.door) and self.key_picked:
            self.sounds.level_up.play()
            self.level_completed = True

    def attach_torch(self):
        """ update torch location when level starts """

        self.torch.rect = self.torch.image.get_rect(center=(self.rect.x + 2, self.rect.y + 2))

    def update(self):
        """ update player every frame """

        # when player active
        if self.lives > 0 and not self.level_completed:
            self.input()
            self.update_status()
            self.animate()

            if self.is_slow and pygame.time.get_ticks() - self.web_time > 5000:
                self.is_slow = False

            if not self.is_slow:
                self.move = True

            if self.move:
                self.rect.x += self.direction.x * self.speed
            self.horizontal_collisions()

            if self.move:
                self.rect.y += self.direction.y * self.speed
            self.vertical_collisions()
            self.enemy_collisions()
            self.collectible_collisions()
            if self.key_active:
                self.key_collisions()

            self.invincibility_timer()

            self.torch.rect = self.torch.image.get_rect(center=(self.rect.x, self.rect.y + 2))
            if self.weapon_active:
                if self.weapon.status == 'idle':
                    self.weapon.rect = self.weapon.image.get_rect(center=(self.rect.x + 8, self.rect.y + 3))
                    self.weapon.animate()
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
            self.weapon_collisions()

            self.trap_collisions()
            self.move = not self.move

            # increase one life on collecting 50 coins
            if self.score == 50:
                self.lives += 1
                self.sounds.life_up.play()
                self.score = 0
                self.ui_update = True

        # when player dies but life stone is available
        elif self.wait_revival:
            if pygame.time.get_ticks() - self.revival_time < 11000:
                self.revival_input()

                # show time left to revive
                self.timer = self.time_frames[10 - int((pygame.time.get_ticks() - self.revival_time) / 1000)]
                self.timer_rect = self.timer.get_rect(center=self.torch.rect.center)

                if self.life_stone_activated:
                    self.lives = PLAYER_LIVES
                    self.wait_revival = False
                    self.status = 'idle'

                    # revive player at level start position
                    self.rect.topleft = self.revival_position
                    self.visibility_radius = VISIBILITY_RADIUS
                    self.life_stone_activated = False
                    self.life_stone_available = False
                    self.ui_update = True
            else:
                self.wait_revival = False
                self.life_stone_activated = False
                self.life_stone_available = False

        # when player dies or completes level
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
        """ update visibility when picked big torch """

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
        """ reset player properties for a new level """

        self.visibility_radius = VISIBILITY_RADIUS
        self.level_completed = False
        self.key_picked = False
        self.key_active = True
        self.status = 'idle'
        self.ui_update = True
        self.is_ghost = False
        self.is_slow = False

        self.is_attacking = False
        self.weapon_active = False
        self.weapon = None
