import pygame
from random import choice


class Tile(pygame.sprite.Sprite):
    """wall and floor tiles of level map"""
    def __init__(self, pos, groups, level, wall, storymode=False):
        super().__init__(groups)

        floor = None

        # each tower in the story mode has different floor theme
        if storymode:
            if 1 <= level <= 5:
                floor = 'grass'
            elif 6 <= level <= 10:
                floor = 'floor'
            elif 11 <= level <= 15:
                floor = 'sand'
        else:
            if 1 <= level <= 15:
                floor = 'grass'
            elif 16 <= level <= 35:
                floor = 'floor'
            elif 36 <= level <= 50:
                floor = 'sand'

        if wall:
            wall1 = pygame.image.load("./assets/images/tiles/tile_1.png").convert_alpha()
            wall2 = pygame.image.load("./assets/images/tiles/tile_2.png").convert_alpha()
            wall3 = pygame.image.load("./assets/images/tiles/tile_3.png").convert_alpha()
            wall4 = pygame.image.load("./assets/images/tiles/tile_4.png").convert_alpha()
            wall5 = pygame.image.load("./assets/images/tiles/tile_5.png").convert_alpha()
            wall6 = pygame.image.load("./assets/images/tiles/tile_6.png").convert_alpha()
            self.image = choice([wall1, wall2, wall3, wall4, wall5, wall6])
        else:
            floor1 = pygame.image.load(f"./assets/images/tiles/{floor}_1.png").convert_alpha()
            floor2 = pygame.image.load(f"./assets/images/tiles/{floor}_2.png").convert_alpha()
            floor3 = pygame.image.load(f"./assets/images/tiles/{floor}_3.png").convert_alpha()
            floor4 = pygame.image.load(f"./assets/images/tiles/{floor}_4.png").convert_alpha()
            self.image = choice([floor1, floor1, floor1, floor1, floor1, floor1, floor2, floor3, floor4])

        self.rect = self.image.get_rect(topleft=pos)
