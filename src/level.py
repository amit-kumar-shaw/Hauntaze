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

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.key1_sprite = pygame.sprite.GroupSingle()
        self.key2_sprite = pygame.sprite.GroupSingle()

        # create cover surface for limited visibility
        self.cover_surf = pygame.Surface((SCREEN_WIDTH, (ROWS*CELL_SIZE*TILE_HEIGHT)), pygame.SRCALPHA)
        self.cover_surf.fill(COVER_COLOR)
        self.cover_surf.set_colorkey((255, 255, 255))
        self.player1_active = player1
        self.player2_active = player2
        self.setup_level()

    def setup_level(self):

        level_map, player_cells, other_cells = map_generator.generate(COLUMNS, ROWS, CELL_SIZE)
        p1 = p2 = (0, 0)
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
        key_door_cells = random.sample(other_cells, 3)
        if self.player1_active:
            self.player1 = Player(tuple(TILE_SIZE*x for x in player_cells[0]),
                                  [self.visible_sprites, self.active_sprites],
                              self.collision_sprites, self.collectible_sprites)
            c = random.choice(list(key_door_cells[0].room))
            self.player1_key = Key(tuple(TILE_SIZE * x for x in c), self.key1_sprite)

        if self.player2_active:
            self.player2 = Player(tuple(TILE_SIZE*x for x in player_cells[1]),
                                  [self.visible_sprites, self.active_sprites],
                              self.collision_sprites, self.collectible_sprites,
                                      player2=True)
            c = random.choice(list(key_door_cells[1].room))
            self.player2_key = Key(tuple(TILE_SIZE * x for x in c), self.key2_sprite)


        self.coins = []
        coin_cells = random.sample(other_cells, 15)
        for cell in coin_cells:
            c = random.choice(list(cell.room))
            self.coins.append(Collectible(tuple(TILE_SIZE * x for x in c), [self.visible_sprites, self.collectible_sprites]))

        # self.door = []
        # door_cells = random.sample(other_cells, 1)
        # for door in door_cells:
        d = random.choice(list(key_door_cells[1].room))
        self.door = Door(tuple(TILE_SIZE * x for x in d), [self.visible_sprites, self.active_sprites],
                     )

        self.enemys = []
        enemy_cells = random.sample(other_cells, 12)
        for enemy in enemy_cells:
            e = random.choice(list(enemy.room))
            self.enemys.append(
                Enemy(tuple(TILE_SIZE * x for x in e), [self.visible_sprites, self.active_sprites],
                              self.collision_sprites))



    def run(self):
        # run the entire game (level)
        self.active_sprites.update()

        self.draw_visible_region()

        self.visible_sprites.draw(self.display_surface)

        for coin in self.coins:
            coin.animate()

        # draw key if the player is nearby
        if self.player1_active and math.dist(self.player1.torch.rect.center,self.player1_key.rect.center) < VISIBILITY_RADIUS:
            self.player1_key.update()
            self.key1_sprite.draw(self.display_surface)
            self.player1_key.animate()
        if self.player2_active and math.dist(self.player2.torch.rect.center,self.player2_key.rect.center) < VISIBILITY_RADIUS:
            self.player2_key.update()
            self.key2_sprite.draw(self.display_surface)
            self.player2_key.animate()

        # draw the cover surface to hide the map
        # self.display_surface.blit(self.cover_surf, (0, 0))

        self.cover_surf.fill(COVER_COLOR)


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
