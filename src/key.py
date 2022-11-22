import pygame


class Key(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        t1 = pygame.image.load("./assets/images/key/1.png").convert_alpha()
        t2 = pygame.image.load("./assets/images/key/2.png").convert_alpha()
        t3 = pygame.image.load("./assets/images/key/3.png").convert_alpha()
        t4 = pygame.image.load("./assets/images/key/4.png").convert_alpha()

        self.frames = [pygame.transform.rotozoom(t1, 0, 0.75),
                       pygame.transform.rotozoom(t2, 0, 0.75),
                       pygame.transform.rotozoom(t3, 0, 0.75), pygame.transform.rotozoom(t4, 0, 0.75)]
        self.animation_index = 0

        self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]