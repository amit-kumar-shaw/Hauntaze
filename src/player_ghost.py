from settings import *
from utilities import import_frames
from pygame.locals import *


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos, story_mode, player2=False, joystick=None):
        super().__init__()

        self.joystick = joystick

        self.story_mode = story_mode

        self.player2 = player2
        self.partner = None
        if self.story_mode:
            self.frames = import_frames("./assets/images/player/torch", scale=0.5)
        else:
            self.frames = import_frames('./assets/images/ghost/idle', scale=0.7)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)

        self.is_flipped = False

        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        self.visibility_radius = GHOST_VISIBILITY

        if not story_mode:
            self.smoke = Smoke(self.rect.center)

        # ghost keys
        if player2:
            self.MOVE_LEFT = PLAYER2_MOVE_LEFT
            self.MOVE_RIGHT = PLAYER2_MOVE_RIGHT
            self.MOVE_UP = PLAYER2_MOVE_UP
            self.MOVE_DOWN = PLAYER2_MOVE_DOWN

        else:
            self.MOVE_LEFT = PLAYER1_MOVE_LEFT
            self.MOVE_RIGHT = PLAYER1_MOVE_RIGHT
            self.MOVE_UP = PLAYER1_MOVE_UP
            self.MOVE_DOWN = PLAYER1_MOVE_DOWN

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[self.MOVE_RIGHT] or (self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) > AXIS_THRESHOLD):
            self.direction.x = 1
            self.is_flipped = False
        elif keys[self.MOVE_LEFT] or (self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) < -AXIS_THRESHOLD):
            self.direction.x = -1
            self.is_flipped = True
        else:
            self.direction.x = 0

        if keys[self.MOVE_UP] or (self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) < -AXIS_THRESHOLD):
            self.direction.y = -1
        elif keys[self.MOVE_DOWN] or (self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) > AXIS_THRESHOLD):
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
        if self.is_flipped:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.input()
        self.animate()

        if self.partner.visibility_radius > GHOST_VISIBILITY:
            self.visibility_radius = GHOST_VISIBILITY
        else:
            self.visibility_radius = self.partner.visibility_radius
            if self.visibility_radius < 2:
                self.kill()

        self.rect.x += self.direction.x * self.speed
        self.horizontal_border()
        self.rect.y += self.direction.y * self.speed
        self.vertical_border()

        if not self.story_mode:
            self.smoke.animate()
            self.smoke.rect = self.smoke.image.get_rect(center = self.rect.center)
            #pygame.display.get_surface().blit(self.smoke.image,self.smoke.rect)


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