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
            number = choice([1, 2, 3, 4, 5, 6])
            self.image = pygame.image.load(f"./assets/images/tiles/tile_{number}.png").convert_alpha()
        else:
            number = choice([1, 1, 1, 1, 1, 1, 1, 2, 3, 4])
            self.image = pygame.image.load(f"./assets/images/tiles/{floor}_{number}.png").convert_alpha()


        self.rect = self.image.get_rect(topleft=pos)
