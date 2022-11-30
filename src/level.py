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


class Level:
    def __init__(self, player1 = False, player2 = False):

        # level setup
        self.display_surface = pygame.display.get_surface()

        self.animation_index = 0

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
        self.cover_surf = pygame.Surface((SCREEN_WIDTH, (ROWS*CELL_SIZE*TILE_HEIGHT)), pygame.SRCALPHA)
        self.cover_surf.fill(COVER_COLOR)
        self.cover_surf.set_colorkey((255, 255, 255))
        self.player1_active = player1
        self.player2_active = player2
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

        key_door_cells = random.sample(other_cells, 4)

        # # draw door
        # d = random.choice(list(key_door_cells[2].room))
        # self.door = Door(tuple(TILE_SIZE * x for x in d), [self.visible_sprites, self.active_sprites],
        #                  )

        # draw player and keys
        if self.player1_active:
            self.player1 = Player(tuple(TILE_SIZE*x for x in player_cells[0]),
                                  [self.visible_sprites, self.active_sprites],
                              self.collision_sprites, self.collectible_sprites, self.enemy_sprites)
            c = random.choice(list(key_door_cells[0].room))
            self.player1.key = Key(tuple(TILE_SIZE * x for x in c), self.key1_sprite)
            c = random.choice(list(key_door_cells[1].room))
            self.player1.door = Door(tuple(TILE_SIZE * x for x in c), self.door1_sprite)

        if self.player2_active:
            self.player2 = Player(tuple(TILE_SIZE*x for x in player_cells[1]),
                                  [self.visible_sprites, self.active_sprites],
                              self.collision_sprites, self.collectible_sprites, self.enemy_sprites,
                                      player2=True)
            c = random.choice(list(key_door_cells[2].room))
            self.player2.key = Key(tuple(TILE_SIZE * x for x in c), self.key2_sprite)
            c = random.choice(list(key_door_cells[3].room))
            self.player2.door = Door(tuple(TILE_SIZE * x for x in c), self.door2_sprite)


        self.coins = []
        coin_cells = random.sample(list(set(other_cells) - set(key_door_cells)), 15)
        for cell in coin_cells:
            c = random.choice(list(cell.room))
            self.coins.append(Collectible(tuple(TILE_SIZE * x for x in c), [self.visible_sprites, self.collectible_sprites]))


        # draw enemies
        self.enemys = []
        enemy_cells = random.sample(other_cells, 12)
        for enemy in enemy_cells:
            e = random.choice(list(enemy.room))
            self.enemys.append(
                Enemy(tuple(TILE_SIZE * x for x in e), [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                              self.collision_sprites))



    def run(self):
        # run the entire game (level)
        self.active_sprites.update()

        self.draw_visible_region()

        self.visible_sprites.draw(self.display_surface)

        for coin in self.coins:
            coin.animate()

        # draw key if the player is nearby
        if self.player1_active and math.dist(self.player1.torch.rect.center,self.player1.key.rect.center) < VISIBILITY_RADIUS:
            self.player1.key.update()
            self.key1_sprite.draw(self.display_surface)
            self.player1.key.animate()
        if self.player2_active and math.dist(self.player2.torch.rect.center,self.player2.key.rect.center) < VISIBILITY_RADIUS:
            self.player2.key.update()
            self.key2_sprite.draw(self.display_surface)
            self.player2.key.animate()

        # draw key if the player is nearby
        if self.player1_active and math.dist(self.player1.torch.rect.center,
                                                 self.player1.door.rect.center) < VISIBILITY_RADIUS:
            self.player1.door.update()
            self.door1_sprite.draw(self.display_surface)

        if self.player2_active and math.dist(self.player2.torch.rect.center,
                                                 self.player2.door.rect.center) < VISIBILITY_RADIUS:
            self.player2.door.update()
            self.door2_sprite.draw(self.display_surface)

        self.check_player_status()

        # open door if key collected
        if (self.player1_active and self.player1.key_picked) and not self.player1.door.isOpen:
            pygame.draw.rect(self.cover_surf, (0, 0, 0, 0), self.player1.door.rect)
            self.player1.door.open()
            self.door1_sprite.draw(self.display_surface)

        if (self.player2_active and self.player2.key_picked) and not self.player2.door.isOpen:
            pygame.draw.rect(self.cover_surf, (0, 0, 0, 0), self.player2.door.rect)
            self.player2.door.open()
            self.door2_sprite.draw(self.display_surface)

        # draw the cover surface to hide the map
        self.display_surface.blit(self.cover_surf, (0, 0))

        self.cover_surf.fill(COVER_COLOR)

        # display game over
        if ((not self.player1_active) and
                (not self.player2_active)):
            self.game_over()

    def check_player_status(self):
        if self.player1_active and self.player1.lives == 0:
            self.player1_active = False
        if self.player2_active and self.player2.lives == 0:
            self.player2_active = False

    def draw_visible_region(self):

        for i in range(0,5):
            if self.player1_active:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50*i)),
                                   (self.player1.torch.rect.centerx, self.player1.torch.rect.centery),
                                   VISIBILITY_RADIUS * float(1 - (i*i)/100))
            if self.player2_active:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50*i)),
                                   (self.player2.torch.rect.centerx, self.player2.torch.rect.centery),
                                   VISIBILITY_RADIUS * float(1 - (i*i)/100))

        # draw enemy indicator
        for enemy in self.enemys:
            if (self.player1_active and math.dist(self.player1.torch.rect.center,enemy.rect.center) > VISIBILITY_RADIUS) and not self.player2_active:
                pygame.draw.circle(self.cover_surf, ('red'), enemy.rect.center, 1)
            if (self.player2_active and math.dist(self.player2.torch.rect.center,enemy.rect.center) > VISIBILITY_RADIUS) and not self.player1_active:
                pygame.draw.circle(self.cover_surf, ('red'), enemy.rect.center, 1)
            if (self.player1_active and math.dist(self.player1.torch.rect.center,enemy.rect.center) > VISIBILITY_RADIUS) and (self.player2_active and math.dist(self.player2.torch.rect.center,enemy.rect.center) > VISIBILITY_RADIUS):
                pygame.draw.circle(self.cover_surf, ('red'), enemy.rect.center, 1)

    def game_over(self):
        # title animation
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

    # TODO: Level completed
