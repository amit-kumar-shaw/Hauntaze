import pygame

import map_generator
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self):

        # level setup
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # create cover surface for limited visibility
        self.cover_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.cover_surf.fill(0)
        self.cover_surf.set_colorkey((255, 255, 255))

        self.setup_level()

    def setup_level(self):

        level_map = map_generator.generate(COLUMNS, ROWS, CELL_SIZE)
        for col_index in range(ROWS * CELL_SIZE):
            for row_index in range(COLUMNS * CELL_SIZE):
                y = col_index * TILE_HEIGHT
                x = row_index * TILE_WIDTH
                if level_map[(row_index, col_index)] == '#' or level_map[(row_index, col_index)] == ' ':
                    Tile((x, y), [self.visible_sprites, self.collision_sprites])
                    Tile((x + 16, y), [self.visible_sprites, self.collision_sprites])
                    Tile((x, y + 16), [self.visible_sprites, self.collision_sprites])
                    Tile((x + 16, y + 16), [self.visible_sprites, self.collision_sprites])
                if level_map[(row_index, col_index)] == 'A':
                    self.player1 = Player((x, y), [self.visible_sprites, self.active_sprites], self.collision_sprites)
                if level_map[(row_index, col_index)] == 'B':
                    self.player2 = Player((x, y), [self.visible_sprites, self.active_sprites], self.collision_sprites,
                                          player2=True)

    def run(self):
        # run the entire game (level)
        self.active_sprites.update()
        # self.visible_sprites.custom_draw(self.player1)
        self.visible_sprites.draw(self.display_surface)
