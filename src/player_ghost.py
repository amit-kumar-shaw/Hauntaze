from settings import *
from utilities import import_frames
from pygame.locals import *


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos, status, player2=False):
        super().__init__()

        self.status = status

        if status == 'dead':
            self.frames = import_frames("./assets/images/player/torch", scale=0.5)
            # self.frame_index = 0
            # self.image = self.frames[self.frame_index]
        else:
            self.frames = import_frames('./assets/images/ghost', scale=0.7)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        self.visibility_radius = GHOST_VISIBILITY

        # ghost keys
        if player2:
            self.MOVE_LEFT = K_LEFT
            self.MOVE_RIGHT = K_RIGHT
            self.MOVE_UP = K_UP
            self.MOVE_DOWN = K_DOWN

        else:
            self.MOVE_LEFT = K_a
            self.MOVE_RIGHT = K_d
            self.MOVE_UP = K_w
            self.MOVE_DOWN = K_s

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[self.MOVE_RIGHT]:
            self.direction.x = 1
        elif keys[self.MOVE_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[self.MOVE_UP]:
            self.direction.y = -1
        elif keys[self.MOVE_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def animate(self):
        if self.status == 'dead':
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames): self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.input()
        self.animate()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
