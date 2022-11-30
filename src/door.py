import pygame
from utilities import import_frames


class Door(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.closed_frame = pygame.image.load("./assets/images/door/door_closed.png").convert_alpha()
        self.open_frame = pygame.image.load("./assets/images/door/door_open.png").convert_alpha()
        self.open_frame = pygame.transform.rotozoom(self.open_frame, 0, 0.5)

        # self.animation_frames = import_frames("./assets/images/door/open_animation", scale=0.5)
        self.animation_frames = []
        for i in range(14):
            if i<9:
                frame = pygame.image.load(f"./assets/images/door/open_animation/open_0{i+1}.png").convert_alpha()
                self.animation_frames.append(pygame.transform.rotozoom(frame, 0, 0.5))
            else:
                frame = pygame.image.load(f"./assets/images/door/open_animation/open_{i + 1}.png").convert_alpha()
                self.animation_frames.append(pygame.transform.rotozoom(frame, 0, 0.5))
        self.animation_index = 0

        self.isOpen = False

        self.image = pygame.transform.rotozoom(self.closed_frame, 0, 0.5)
        self.rect = self.image.get_rect(topleft = pos)

    def open(self):
        self.animation_index += 0.08

        if self.animation_index >= len(self.animation_frames):
            self.animation_index = 0
            self.isOpen = True
            self.image = self.open_frame
            return

        if self.animation_index > 6:
            self.play_open_sound()

        self.image = self.animation_frames[int(self.animation_index)]

    def play_open_sound(self):
        sound = pygame.mixer.Sound('./assets/Audio/doorOpen_4.mp3')
        sound.set_volume(0.7)
        sound.play()