import random

import pygame

import map_generator
from settings import *
from tile import Tile
from player import Player
from collectible import Collectible


class Level:
    def __init__(self):

        # level setup
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()

        # create cover surface for limited visibility
        self.cover_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.cover_surf.fill(COVER_COLOR)
        self.cover_surf.set_colorkey((255, 255, 255))

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
        self.player1 = Player(tuple(TILE_SIZE*x for x in player_cells[0]), [self.visible_sprites, self.active_sprites], self.collision_sprites)
        self.player2 = Player(tuple(TILE_SIZE*x for x in player_cells[1]), [self.visible_sprites, self.active_sprites], self.collision_sprites,
                                      player2=True)

        self.coins = []
        coin_cells = random.sample(other_cells, 15)
        for cell in coin_cells:
            c = random.choice(list(cell.room))
            self.coins.append(Collectible(tuple(TILE_SIZE * x for x in c), [self.visible_sprites, self.collectible_sprites]))


    def run(self):
        # run the entire game (level)
        self.active_sprites.update()
        # self.visible_sprites.custom_draw(self.player1)

        # draw visible area around players
        # pygame.draw.circle(self.cover_surf, (255, 255, 255), (self.player1.rect.centerx, self.player1.rect.centery),
        #                    VISIBILITY_RADIUS)
        # pygame.draw.circle(self.cover_surf, (255, 255, 255), (self.player2.rect.centerx, self.player2.rect.centery),
        #                    VISIBILITY_RADIUS)

        self.draw_visible_region()

        self.visible_sprites.draw(self.display_surface)

        for coin in self.coins:
            coin.animate()

        # self.display_surface.blit(self.cover_surf, (0, 0))
        # pygame.display.flip()
        self.cover_surf.fill(COVER_COLOR)

    def draw_visible_region(self):
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 200), (self.player1.rect.centerx, self.player1.rect.centery),
                           VISIBILITY_RADIUS)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 200), (self.player2.rect.centerx, self.player2.rect.centery),
                           VISIBILITY_RADIUS)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 150), (self.player1.rect.centerx, self.player1.rect.centery),
                           VISIBILITY_RADIUS * 0.97)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 150), (self.player2.rect.centerx, self.player2.rect.centery),
                           VISIBILITY_RADIUS * 0.97)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 100), (self.player1.rect.centerx, self.player1.rect.centery),
                           VISIBILITY_RADIUS * 0.93)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 100), (self.player2.rect.centerx, self.player2.rect.centery),
                           VISIBILITY_RADIUS * 0.93)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 50), (self.player1.rect.centerx, self.player1.rect.centery),
                           VISIBILITY_RADIUS * 0.88)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 50), (self.player2.rect.centerx, self.player2.rect.centery),
                           VISIBILITY_RADIUS * 0.88)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 0), (self.player1.rect.centerx, self.player1.rect.centery),
                           VISIBILITY_RADIUS * 0.80)
        pygame.draw.circle(self.cover_surf, (0, 0, 0, 0), (self.player2.rect.centerx, self.player2.rect.centery),
                           VISIBILITY_RADIUS * 0.80)