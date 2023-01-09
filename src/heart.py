import pygame


class Item (pygame.sprite.Sprite):
    def __init__(self, pos, groups, itemtype, name):
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()

        self.frames = [pygame.transform.rotozoom(t1, 0, 0.5),
                       pygame.transform.rotozoom(t2, 0, 0.5), pygame.transform.rotozoom(t3, 0, 0.5)]
        self.animation_index = random.choice([0, 1, 2])

        self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):

        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]