import pygame
from utilities import import_frames


class Door(pygame.sprite.Sprite):
    '''Each level Door'''
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.closed_frame = pygame.image.load("./assets/images/door/door_closed.png").convert_alpha()
        self.open_frame = pygame.image.load("./assets/images/door/door_open.png").convert_alpha()
        self.open_frame = pygame.transform.rotozoom(self.open_frame, 0, 0.5)

        self.animation_frames = import_frames("./assets/images/door/open_animation", scale=0.5)

        self.animation_index = 0

        self.isOpen = False

        self.image = pygame.transform.rotozoom(self.closed_frame, 0, 0.5)
        self.rect = self.image.get_rect(topleft = pos)

        self.sound = pygame.mixer.Sound('./assets/Audio/player/door_open.ogg')
        self.sound.set_volume(0.7)

    def open(self):
        '''door open animation when key is picked by player'''

        self.animation_index += 0.08

        if self.animation_index >= len(self.animation_frames):
            self.animation_index = 0
            self.isOpen = True
            self.image = self.open_frame
            return

        if self.animation_index > 6 and self.animation_index < 6.1:
            self.sound.play()

        self.image = self.animation_frames[int(self.animation_index)]
