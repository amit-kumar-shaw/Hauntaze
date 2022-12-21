import math
import random

import pygame

import map_generator
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from collectible import Collectible
from key import Key
from door import Door
from music import GameSound
from player_ghost import Ghost


class Level:
    def __init__(self, story_mode, player1_active, player1, player2_active, player2):

        # level setup
        self.display_surface = pygame.display.get_surface()

        self.completed = False
        self.failed = False
        self.animation_index = 0

        self.story_mode = story_mode

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.key1_sprite = pygame.sprite.GroupSingle()
        self.key2_sprite = pygame.sprite.GroupSingle()
        self.door1_sprite = pygame.sprite.GroupSingle()
        self.door2_sprite = pygame.sprite.GroupSingle()

        # create cover surface for limited visibility
        self.cover_surf = pygame.Surface((SCREEN_WIDTH, (ROWS * CELL_SIZE * TILE_HEIGHT)), pygame.SRCALPHA)
        self.cover_surf.fill(COVER_COLOR)
        self.cover_surf.set_colorkey((255, 255, 255))

        # create map surface
        self.map_surf = pygame.Surface((SCREEN_WIDTH, (ROWS * CELL_SIZE * TILE_HEIGHT)))

        # create cropped surface
        self.cropped_surf1 = pygame.Surface((VISIBILITY_RADIUS * 2, VISIBILITY_RADIUS * 2))
        self.cropped_surf2 = pygame.Surface((VISIBILITY_RADIUS * 2, VISIBILITY_RADIUS * 2))
        self.cropped_surf3 = pygame.Surface((GHOST_VISIBILITY * 2, GHOST_VISIBILITY * 2))
        self.cropped_rect1 = self.cropped_surf1.get_rect()
        self.cropped_rect2 = self.cropped_surf2.get_rect()
        self.cropped_rect3 = self.cropped_surf3.get_rect()

        self.player1_active = player1_active
        self.player2_active = player2_active
        self.player1 = player1
        self.player2 = player2

        # Ghost
        self.ghost_active = False
        self.ghost = None

        self.sound = GameSound()
        self.sound.playbackgroundmusic()

        self.setup_level()

    def setup_level(self):

        level_map, player_cells, other_cells = map_generator.generate(COLUMNS, ROWS, CELL_SIZE)

        for col_index in range(ROWS * CELL_SIZE):
            for row_index in range(COLUMNS * CELL_SIZE):
                y = col_index * TILE_HEIGHT
                x = row_index * TILE_WIDTH
                if level_map[(row_index, col_index)] == '.':
                    Tile((x, y), [self.visible_sprites], wall=False)
                if level_map[(row_index, col_index)] == '#':
                    Tile((x, y), [self.visible_sprites, self.collision_sprites], wall=True)
                if level_map[(row_index, col_index)] == 'A':
                    p1 = (x, y)
                    Tile((x, y), [self.visible_sprites], wall=False)
                if level_map[(row_index, col_index)] == 'B':
                    p2 = (x, y)
                    Tile((x, y), [self.visible_sprites], wall=False)

        self.visible_sprites.draw(self.map_surf)
        key_door_cells = random.sample(other_cells, 4)

        # # draw door
        # d = random.choice(list(key_door_cells[2].room))
        # self.door = Door(tuple(TILE_SIZE * x for x in d), [self.visible_sprites, self.active_sprites],
        #                  )

        # draw player and keys
        if self.player1_active:
            # c = random.choice(list(key_door_cells[1].room))
            # door = Door(tuple(TILE_SIZE * x for x in c), self.door1_sprite)
            # self.player1 = Player(tuple(TILE_SIZE * x for x in player_cells[0]),
            #                       [self.active_sprites],
            #                       self.collision_sprites, self.collectible_sprites, self.enemy_sprites)
            self.player1.rect.topleft = tuple(TILE_SIZE * x for x in player_cells[0])
            self.player1.attach_torch()
            self.player1.collision_sprites = self.collision_sprites
            self.player1.collectible_sprites = self.collectible_sprites
            self.player1.enemy_sprites = self.enemy_sprites

            c = random.choice(list(key_door_cells[0].room))
            self.player1.key = Key(tuple(TILE_SIZE * x for x in c), self.key1_sprite)
            c = random.choice(list(key_door_cells[1].room))
            self.player1.door = Door(tuple(TILE_SIZE * x for x in c), self.door1_sprite)
            # self.player1.door = door

        if self.player2_active:
            # c = random.choice(list(key_door_cells[3].room))
            # door = Door(tuple(TILE_SIZE * x for x in c), self.door2_sprite)
            # self.player2 = Player(tuple(TILE_SIZE * x for x in player_cells[1]),
            #                       [self.active_sprites],
            #                       self.collision_sprites, self.collectible_sprites, self.enemy_sprites,
            #                       player2=True)

            self.player2.rect.topleft = tuple(TILE_SIZE * x for x in player_cells[1])
            self.player2.attach_torch()
            self.player2.collision_sprites = self.collision_sprites
            self.player2.collectible_sprites = self.collectible_sprites
            self.player2.enemy_sprites = self.enemy_sprites

            c = random.choice(list(key_door_cells[2].room))
            self.player2.key = Key(tuple(TILE_SIZE * x for x in c), self.key2_sprite)
            c = random.choice(list(key_door_cells[3].room))
            self.player2.door = Door(tuple(TILE_SIZE * x for x in c), self.door2_sprite)
            # self.player2.door = door

        self.coins = []
        coin_cells = random.sample(list(set(other_cells) - set(key_door_cells)), 15)
        for cell in coin_cells:
            c = random.choice(list(cell.room))
            self.coins.append(
                Collectible(tuple(TILE_SIZE * x for x in c), [self.visible_sprites, self.collectible_sprites], type='coin'))

        cell = random.sample(list(set(other_cells) - set(key_door_cells)), 1)
        c = random.choice(list(cell[0].room))
        Collectible(tuple(TILE_SIZE * x for x in c), [self.visible_sprites, self.collectible_sprites], type='torch')

        # draw enemies
        self.enemys = []
        enemy_cells = random.sample(other_cells, 5)
        for enemy in enemy_cells:
            e = random.choice(list(enemy.room))
            self.enemys.append(
                Enemy(tuple(TILE_SIZE * x for x in e), [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                      self.collision_sprites))

    def run(self):

        # Activate ghost


        # run the entire game (level)
        self.active_sprites.update()

        if self.player1_active:
            PLAYER1_SPRITE.update()

        if self.player2_active:
            PLAYER2_SPRITE.update()

        self.draw_visible_region()

        # self.visible_sprites.draw(self.display_surface)
        # self.collision_sprites.draw(self.display_surface)

        # draw the map surface
        # self.display_surface.blit(self.map_surf, (0, 0))
        if self.player1_active:
            if self.player1.visibility_radius != VISIBILITY_RADIUS:
                self.cropped_surf1 = pygame.Surface(
                    (self.player1.visibility_radius * 2, self.player1.visibility_radius * 2))
            self.cropped_rect1 = self.cropped_surf1.get_rect(center=self.player1.torch.rect.center)
            self.display_surface.blit(self.map_surf, self.cropped_rect1, self.cropped_rect1)
        if self.player2_active:
            if self.player2.visibility_radius != VISIBILITY_RADIUS:
                self.cropped_surf2 = pygame.Surface(
                    (self.player2.visibility_radius * 2, self.player2.visibility_radius * 2))
            self.cropped_rect2 = self.cropped_surf2.get_rect(center=self.player2.torch.rect.center)
            self.display_surface.blit(self.map_surf, self.cropped_rect2, self.cropped_rect2)
        if self.ghost_active:
            if self.story_mode:
                self.cropped_rect3 = self.cropped_surf3.get_rect(center=self.ghost.rect.center)
                self.display_surface.blit(self.map_surf, self.cropped_rect3, self.cropped_rect3)
            # else:
            #     pygame.draw.circle(self.display_surface, (0, 0, 0),
            #                        (self.ghost.rect.centerx, self.ghost.rect.centery),
            #                        self.ghost.visibility_radius)

        # cover surface
        if self.player1_active:
            self.display_surface.blit(self.cover_surf, self.cropped_rect1, self.cropped_rect1)
        if self.player2_active:
            self.display_surface.blit(self.cover_surf, self.cropped_rect2, self.cropped_rect2)
        if self.ghost_active and self.story_mode:
            self.display_surface.blit(self.cover_surf, self.cropped_rect3, self.cropped_rect3)

        # for coin in self.coins:
        #     coin.animate()

        # self.collectible_sprites.draw(self.display_surface)
        self.collectible_sprites.update()
        for sprite in self.collectible_sprites.sprites():
            # if (self.player1_active and pygame.sprite.collide_rect_ratio(1)(sprite, self.cropped_surf1) or (
            #         self.player2_active and pygame.sprite.collide_rect_ratio(1)(sprite, self.cropped_surf2))):
            if (self.player1_active and self.cropped_rect1.contains(sprite)) or (
                    self.player2_active and self.cropped_rect2.contains(sprite)):
                sprite.draw(self.display_surface)

        # draw key if the player is nearby
        if self.player1_active and math.dist(self.player1.torch.rect.center,
                                             self.player1.key.rect.center) < self.player1.visibility_radius:
            # self.player1.key.update()
            self.key1_sprite.draw(self.display_surface)
            self.player1.key.animate()

        if self.player2_active and math.dist(self.player2.torch.rect.center,
                                             self.player2.key.rect.center) < self.player2.visibility_radius:
            # self.player2.key.update()
            self.key2_sprite.draw(self.display_surface)
            self.player2.key.animate()

        # draw door if the player is nearby
        if self.player1_active and math.dist(self.player1.torch.rect.center,
                                             self.player1.door.rect.center) < self.player1.visibility_radius:
            # self.player1.door.update()
            self.door1_sprite.draw(self.display_surface)

        if self.player2_active and math.dist(self.player2.torch.rect.center,
                                             self.player2.door.rect.center) < self.player2.visibility_radius:
            # self.player2.door.update()
            self.door2_sprite.draw(self.display_surface)

        # open door if key collected
        if (self.player1_active and self.player1.key_picked) and not self.player1.door.isOpen:
            # pygame.draw.rect(self.cover_surf, (0, 0, 0, 0), self.player1.door.rect)
            self.player1.door.open()
            self.door1_sprite.draw(self.display_surface)

        if (self.player2_active and self.player2.key_picked) and not self.player2.door.isOpen:
            # pygame.draw.rect(self.cover_surf, (0, 0, 0, 0), self.player2.door.rect)
            self.player2.door.open()
            self.door2_sprite.draw(self.display_surface)

        #self.active_sprites.draw(self.display_surface)
        for sprite in self.enemy_sprites.sprites():
            # if (self.player1_active and pygame.sprite.collide_rect_ratio(1)(sprite, self.cropped_rect1)) or (
            #         self.player2_active and pygame.sprite.collide_rect_ratio(1)(sprite, self.cropped_rect2)):
            if (self.player1_active and self.cropped_rect1.contains(sprite)) or (
                        self.player2_active and self.cropped_rect2.contains(sprite)) or (
                        self.ghost_active and self.cropped_rect3.contains(sprite)):
                sprite.draw(self.display_surface)

        if self.player1_active and self.player1.visibility_radius > 1:
            PLAYER1_SPRITE.draw(self.display_surface)
        if self.player2_active and self.player2.visibility_radius > 1:
            PLAYER2_SPRITE.draw(self.display_surface)

        # Ghost update
        if self.ghost_active:
            self.ghost.update()
            self.display_surface.blit(self.ghost.image,self.ghost.rect)

        # draw the cover surface to hide the map
        # self.display_surface.blit(self.cover_surf, (0, 0))
        # if self.player1_active:
        #     self.display_surface.blit(self.cover_surf, self.cropped_rect1, self.cropped_rect1)
        # if self.player2_active:
        #     self.display_surface.blit(self.cover_surf, self.cropped_rect2, self.cropped_rect2)
        # if self.ghost_active and self.story_mode:
        #     self.display_surface.blit(self.cover_surf, self.cropped_rect3, self.cropped_rect3)

        self.cover_surf.fill(COVER_COLOR)

        # display game over
        if ((not self.player1_active) and
                (not self.player2_active)):
            self.game_over()

        # level completed msg
        if self.player1_active and self.player1.level_completed and not self.player2_active:
            self.level_completed()

        if self.player2_active and self.player2.level_completed and not self.player1_active:
            self.level_completed()

        if self.player1_active and self.player1.level_completed and self.player2_active and self.player2.level_completed:
            self.level_completed()

        self.check_player_status()

        # TODO: Tower - remove after test
        tower = pygame.image.load("./assets/images/tower.png").convert_alpha()
        self.display_surface.blit(tower, (560,0))
        # print(self.player1_active, self.player1.is_alive, self.player1.lives)

    def check_player_status(self):
        if self.player1_active and not self.player1.is_alive:
            self.player1_active = False
            if not self.ghost_active:
                self.ghost = Ghost(self.player1.rect.topleft, self.story_mode, player2=False)
                self.ghost_active = True
        if self.player2_active and not self.player2.is_alive:
            self.player2_active = False
            if not self.ghost_active:
                self.ghost = Ghost(self.player2.rect.topleft, self.story_mode, player2=True)
                self.ghost_active = True

        if self.player1_active and self.player1.is_ghost and not self.ghost_active:
            self.ghost = Ghost(self.player1.rect.topleft, self.story_mode, player2=False)
            self.ghost_active = True
        if self.player2_active and self.player2.is_ghost and not self.ghost_active:
            self.ghost = Ghost(self.player2.rect.topleft, self.story_mode, player2=True)
            self.ghost_active = True

    def draw_visible_region(self):

        for i in range(0, 5):
            if self.player1_active:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50 * i)),
                                   (self.player1.torch.rect.centerx, self.player1.torch.rect.centery),
                                   self.player1.visibility_radius * float(1 - (i * i) / 100))
            if self.player2_active:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50 * i)),
                                   (self.player2.torch.rect.centerx, self.player2.torch.rect.centery),
                                   self.player2.visibility_radius * float(1 - (i * i) / 100))
            if self.ghost_active and self.story_mode:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50 * i)),
                                   (self.ghost.rect.centerx, self.ghost.rect.centery),
                                   self.ghost.visibility_radius * float(1 - (i * i) / 100))

        # draw enemy indicator
        for enemy in self.enemys:
            if (self.player1_active and math.dist(self.player1.torch.rect.center,
                                                  enemy.rect.center) > self.player1.visibility_radius) and not self.player2_active:
                pygame.draw.circle(self.display_surface, 'red', enemy.rect.center, 1)
            if (self.player2_active and math.dist(self.player2.torch.rect.center,
                                                  enemy.rect.center) > self.player2.visibility_radius) and not self.player1_active:
                pygame.draw.circle(self.display_surface, 'red', enemy.rect.center, 1)
            if (self.player1_active and math.dist(self.player1.torch.rect.center,
                                                  enemy.rect.center) > self.player1.visibility_radius) and (
                    self.player2_active and math.dist(self.player2.torch.rect.center,
                                                      enemy.rect.center) > self.player2.visibility_radius):
                pygame.draw.circle(self.display_surface, 'red', enemy.rect.center, 1)

        # TODO: remove in final game. Only for testing and debugging
        if self.player1_active:
            pygame.draw.circle(self.display_surface, 'green', self.player1.door.rect.center, 3)
            pygame.draw.circle(self.display_surface, 'yellow', self.player1.key.rect.center, 3)

        if self.player2_active:
            pygame.draw.circle(self.display_surface, 'pink', self.player2.door.rect.center, 3)
            pygame.draw.circle(self.display_surface, 'orange', self.player2.key.rect.center, 3)

    def game_over(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.failed = True
        self.animation_index += 0.08

        if self.animation_index >= 2: self.animation_index = 0

        # title
        font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 75 + int(self.animation_index))
        title = font.render('Game Over', False, 'yellow')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
        self.display_surface.blit(title, title_rect)

        title = font.render('Game Over', False, 'red')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.display_surface.blit(title, title_rect)

        # Restart game message
        font = pygame.font.Font('./assets/fonts/1.ttf', 15)
        resume_msg = font.render('Press ENTER to restart', False, 'white')
        msg_rect = resume_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.display_surface.blit(resume_msg, msg_rect)

    # TODO: Level completed
    def level_completed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.completed = True
        self.animation_index += 0.08

        if self.animation_index >= 2: self.animation_index = 0

        # title
        font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 60 + int(self.animation_index))
        title = font.render('Level Completed', False, 'red')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
        self.display_surface.blit(title, title_rect)

        title = font.render('Level Completed', False, 'yellow')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.display_surface.blit(title, title_rect)

        # Continue game message
        font = pygame.font.Font('./assets/fonts/1.ttf', 15)
        resume_msg = font.render('Press ENTER to continue', False, 'white')
        msg_rect = resume_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.display_surface.blit(resume_msg, msg_rect)
