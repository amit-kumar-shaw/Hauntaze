from settings import *
from utilities import import_frames
from pygame.locals import *


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos, story_mode, player2=False):
        super().__init__()

        self.story_mode = story_mode

        if self.story_mode:
            self.frames = import_frames("./assets/images/player/torch", scale=0.5)
        else:
            self.frames = import_frames('./assets/images/ghost/idle', scale=0.7)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        self.visibility_radius = GHOST_VISIBILITY

        if not story_mode:
            self.smoke = Smoke(self.rect.center)

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

    def horizontal_border(self):
        if self.rect.x <= 16:
            self.rect.x = 16
        if self.rect.x >= 560 - self.rect.width - 16:
            self.rect.x = 560 - self.rect.width - 16

    def vertical_border(self):
        if self.rect.y <= 16:
            self.rect.y = 16
        if self.rect.y >= 320 - self.rect.height - 16:
            self.rect.y = 320 - self.rect.height - 16

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.input()
        self.animate()

        self.rect.x += self.direction.x * self.speed
        self.horizontal_border()
        self.rect.y += self.direction.y * self.speed
        self.vertical_border()

        if not self.story_mode:
            self.smoke.animate()
            self.smoke.rect = self.smoke.image.get_rect(center = self.rect.center)
            pygame.display.get_surface().blit(self.smoke.image,self.smoke.rect)


class Smoke(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.frames = import_frames('./assets/images/ghost/Smoke', scale=0.5)
        self.frame_index = 0

        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(center=pos)


    def animate(self):

        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]