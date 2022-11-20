import pygame



class Door(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./assets/images/door/tile_0045.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)