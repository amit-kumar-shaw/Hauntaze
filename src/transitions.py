import sys
import pygame
from settings import *
from stones import Stone
from utilities import import_frames
from sounds import TransitionSound


class StoryTransition:
    """ Cut scenes for story mode """
    def __init__(self, p1, p2, joystick_1=None, joystick_2=None):

        self.joystick_1 = joystick_1
        self.joystick_2 = joystick_2

        self.display = pygame.display.get_surface()
        self.sound = TransitionSound()
        self.sound_index = 0
        self.load_index = 2

        self.tower_surface = pygame.Surface((64, 320))

        self.tower_rect = self.tower_surface.get_rect(topleft=(576, 0))
        self.screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.castle = pygame.image.load("./assets/images/transitions/castle.png").convert_alpha()
        self.exit = pygame.image.load("./assets/images/transitions/exit.png").convert_alpha()
        self.skip_animation = pygame.image.load("./assets/images/transitions/skip_animation.png").convert_alpha()
        self.start = pygame.image.load("./assets/images/transitions/start.png").convert_alpha()

        self.intro_completed = False
        self.life_completed = False
        self.death_completed = False
        self.curse_completed = False
        self.completed = False

        self.reached_tower1 = False
        self.reached_tower2 = False
        self.reached_tower3 = False
        self.stall_completed = False
        self.player_position_initialized = False
        self.skip_active = True
        self.animating = False

        self.wait_frames = []
        self.wait_index = 0
        self.wait_active = False

        self.level = 1
        self.frame_index = 1

        self.intro_frames = None
        self.intro_index = 0

        self.life_frames = None
        self.life_index = 0

        self.death_frames = None
        self.death_index = 0

        self.curse_frames = None
        self.curse_index = 0

        self.all_towers = pygame.image.load(f"./assets/images/transitions/tower/all_towers.png").convert_alpha()
        self.tower_frames = import_frames(f"./assets/images/transitions/tower/tower", scale=1)
        self.tower_index = 0

        self.multiplayer = False
        if p1 and p2:
            self.multiplayer = True
            path = f'./assets/images/transitions/torch/'
            self.ghost_frames = {'idle': [], 'walk': []}

            for status in self.ghost_frames.keys():
                full_path = path + status
                self.ghost_frames[status] = import_frames(full_path, scale=0.8)

        self.ghost_active = False

        self.p1_active = p1
        self.p2_active = p2
        self.path_index = 0
        if self.p1_active:
            path = f'./assets/images/player/p1/'
            self.p1_frames = {'idle': [], 'walk': []}

            for status in self.p1_frames.keys():
                full_path = path + status
                self.p1_frames[status] = import_frames(full_path, scale=0.8)

            self.p1_frame_index = 0
            self.p1_image = self.p1_frames['idle'][0]
            self.p1_rect = self.p1_image.get_rect(bottomleft=(24, 288))
            self.p1_direction = pygame.math.Vector2()
            self.p1_flipped = False
            self.p1_direction_changed = False
            self.p1_path = [[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                            (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0),
                            (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)],
                            [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)
                             ],
                            [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)
                             ],
                            []
                            ]

        if self.p2_active:
            path = f'./assets/images/player/p2/'
            self.p2_frames = {'idle': [], 'walk': []}

            for status in self.p2_frames.keys():
                full_path = path + status
                self.p2_frames[status] = import_frames(full_path, scale=0.8)
            self.p2_index = 0
            self.p2_frame_index = 0
            self.p2_image = self.p2_frames['idle'][self.p2_index]
            self.p2_rect = self.p2_image.get_rect(bottomleft=(16, 288))
            self.p2_direction = pygame.math.Vector2()
            self.p2_flipped = False
            self.p2_direction_changed = False
            self.p2_path = [[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                            (1, 0), (1, 0), (1, 0),
                            (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (-1, 0), (-1, 0),
                            (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)],
                            [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)
                             ],
                            [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                             (1, 0), (1, 0), (1, 0)
                             ],
                            []
                            ]

        self.stones = []
        self.stones.append(Stone((160, SCREEN_HEIGHT / 2), 'life', 1.5))
        self.stones.append(Stone((320, SCREEN_HEIGHT / 2), 'death', 1.5))
        self.stones.append(Stone((480, SCREEN_HEIGHT / 2), 'curse', 1.5))
        for stone in self.stones:
            stone.active = False

    def update(self):
        """ update when showing cut scenes """

        # change player image when player dies
        if self.multiplayer and not self.ghost_active and not (self.p1_active and self.p2_active):
            self.activate_ghost()

        if self.level <= 5:
            if not self.intro_completed:
                self.intro()
            else:
                if self.wait_active:
                    self.wait_start()
                else:
                    self.tower()
        elif 5 < self.level <= 10:
            if not self.life_completed:
                self.life()
            else:
                if self.wait_active:
                    self.wait_start()
                else:
                    self.tower()
        elif 10 < self.level <= 15:
            if not self.death_completed:
                self.death()
            else:
                if self.wait_active:
                    self.wait_start()
                else:
                    self.tower()
        else:
            if not self.curse_completed:
                self.curse()
            else:
                self.wait_start()
        #
        # self.draw()

    def activate_ghost(self):
        """ change player image when player dies """
        if not self.p1_active:
            self.p1_frames = self.ghost_frames
            self.p1_active = True
        elif not self.p2_active:
            self.p2_frames = self.ghost_frames
            self.p2_active = True
        self.ghost_active = True

    def wait_start(self):
        """ wait for layer input to start game """

        self.wait_index += 0.2
        if self.wait_index >= len(self.wait_frames):
            self.wait_index = 0

        if self.level == 1:
            self.display.blit(self.wait_frames[int(self.wait_index)], (139, 180, 44, 40), (139, 180, 44, 40))
            self.display.blit(self.wait_frames[int(self.wait_index)], (458, 182, 44, 39), (458, 182, 44, 39))

        self.display.blit(self.wait_frames[int(self.wait_index)], (299, 181, 42, 39), (299, 181, 42, 39))

        keys = pygame.key.get_pressed()
        if not (keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON))) and not self.skip_active:
            self.skip_active = True
        if (keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON))) and self.skip_active:
            self.wait_active = False
            self.sound.confirm.play()

            # exit game when story mode completed
            if self.level == 16:
                pygame.quit()
                sys.exit()

    def intro(self):
        """ display information when game starts """

        if self.intro_frames is None:
            self.screen_surface.blit(self.castle, (0, 0))
            self.screen_surface.blit(self.skip_animation, self.skip_animation.get_rect(midright=(632,350)))
            self.sound_index = 4
            self.load_index = 2
            self.intro_frames = []
            self.animating = True

        # load frames one frame at a time for efficiency
        if self.load_index <= 299:
            if self.load_index < 10:
                self.intro_frames.append(pygame.image.load(f"./assets/images/transitions/intro2/intro_00{self.load_index}.png").convert())
            elif self.load_index < 100:
                self.intro_frames.append(pygame.image.load(f"./assets/images/transitions/intro2/intro_0{self.load_index}.png").convert())
            else:
                self.intro_frames.append(pygame.image.load(f"./assets/images/transitions/intro2/intro_{self.load_index}.png").convert())
            self.load_index += 1

        # skip animation
        keys = pygame.key.get_pressed()
        if ((keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON))) and self.skip_active) or self.intro_index > 222:
            self.intro_completed = True
            if not self.intro_index > 222:
                self.sound.confirm.play()
            self.skip_active = False
            self.wait_frames = import_frames("./assets/images/transitions/wait_intro", scale=1)
            self.wait_index = 0
            self.wait_active = True
            self.display.blit(self.wait_frames[self.wait_index], (0, 0))
            self.display.blit(self.start, self.start.get_rect(midright=(632, 350)))
            return

        self.intro_index += 0.2
        if self.intro_index >= len(self.intro_frames): self.intro_index = 225

        # display title
        if self.intro_index < 0.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (160, 50, 320, 20), (160, 50, 320, 20))

        # display first line
        elif 4 < self.intro_index < 74:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (35, 112, 572, 16), (35, 112, 572, 16))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 74:
                    self.sound_index = 80

        # display second line
        elif 80 < self.intro_index < 117:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (172, 144, 297, 13), (172, 144, 297, 13))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 116:
                    self.sound_index = 131

        # display life stone text
        elif 131 < self.intro_index < 131.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (95, 222, 130, 14), (95, 222, 130, 14))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.appear.play()
                self.sound_index = 145

        # display death stone text
        elif 145 < self.intro_index < 145.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (245, 222, 150, 16), (245, 222, 150, 16))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.appear.play()
                self.sound_index = 160

        # display curse stone text
        elif 160 < self.intro_index < 160.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (405, 222, 152, 15), (405, 222, 152, 15))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.appear.play()
                self.sound_index = 176

        # display last line
        elif 175 < self.intro_index < 222:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (126, 263, 387, 16), (126, 263, 387, 16))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2

        # display life stone
        if 131 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (139, 180, 44, 40), (139, 180, 44, 40))

        # display death stone
        if 145 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (299, 181, 42, 39), (299, 181, 42, 39))

        # display curse stone
        if 160 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (458, 182, 44, 39), (458, 182, 44, 39))

        if self.intro_completed:
            self.screen_surface.fill('black')
        self.display.blit(self.screen_surface, (0, 0))

    def life(self):
        """ cut scene after winning life stone """

        if self.life_frames is None:
            self.screen_surface.blit(self.castle, (0, 0))
            self.screen_surface.blit(self.skip_animation, self.skip_animation.get_rect(midright=(632, 350)))
            self.sound_index = 4
            self.load_index = 2
            self.life_frames = []

        # load frames one frame at a time for efficiency
        if self.load_index <= 299:
            if self.load_index < 10:
                self.life_frames.append(
                    pygame.image.load(f"./assets/images/transitions/life/life_00{self.load_index}.png").convert())
            elif self.load_index < 100:
                self.life_frames.append(
                    pygame.image.load(f"./assets/images/transitions/life/life_0{self.load_index}.png").convert())
            else:
                self.life_frames.append(
                    pygame.image.load(f"./assets/images/transitions/life/life_{self.load_index}.png").convert())
            self.load_index += 1

        # skip animation
        keys = pygame.key.get_pressed()
        if ((keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON))) and self.skip_active) or self.life_index > 261:
            self.life_completed = True
            if not self.life_index > 261:
                self.sound.confirm.play()
            self.skip_active = False
            self.wait_frames = import_frames("./assets/images/transitions/wait_life", scale=1)
            self.wait_index = 0
            self.wait_active = True
            self.display.blit(self.wait_frames[self.wait_index], (0, 0))
            self.display.blit(self.start, self.start.get_rect(midright=(632, 350)))
            return

        self.life_index += 0.2
        if self.life_index >= len(self.life_frames): self.life_index = 265

        # display title and life stone text
        if self.life_index < 0.5:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (255, 223, 131, 14), (255, 223, 131, 14))

        # display first line
        elif 4 < self.life_index < 39:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (180, 112, 280, 15), (180, 112, 280, 15))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 38:
                    self.sound_index = 44

        # display second line
        elif 44 < self.life_index < 112:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (48, 142, 542, 18), (48, 142, 542, 18))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 112:
                    self.sound_index = 130

        # display third line
        elif 130 < self.life_index < 196:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (46, 262, 548, 19), (46, 262, 548, 19))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 196:
                    self.sound_index = 202

        # display last line
        elif 202 < self.life_index < 261:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (82, 290, 475, 21), (82, 290, 475, 21))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2

        # display life stone
        self.screen_surface.blit(self.life_frames[int(self.life_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        if self.life_completed:
            self.screen_surface.fill('black')

        self.display.blit(self.screen_surface, (0, 0))

    def death(self):
        """ cut scene after winning death stone """

        if self.death_frames is None:
            self.screen_surface.blit(self.castle, (0, 0))
            self.screen_surface.blit(self.skip_animation, self.skip_animation.get_rect(midright=(632, 350)))
            self.sound_index = 4
            self.load_index = 2
            self.death_frames = []

        # load frames one frame at a time for efficiency
        if self.load_index <= 299:
            if self.load_index < 10:
                self.death_frames.append(
                    pygame.image.load(f"./assets/images/transitions/death2/death_00{self.load_index}.png").convert())
            elif self.load_index < 100:
                self.death_frames.append(
                    pygame.image.load(f"./assets/images/transitions/death2/death_0{self.load_index}.png").convert())
            else:
                self.death_frames.append(
                    pygame.image.load(f"./assets/images/transitions/death2/death_{self.load_index}.png").convert())
            self.load_index += 1

        # skip animation
        keys = pygame.key.get_pressed()
        if ((keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON))) and self.skip_active) or self.death_index > 250:
            self.death_completed = True
            if not self.death_index > 250:
                self.sound.confirm.play()
            self.skip_active = False
            self.wait_frames = import_frames("./assets/images/transitions/wait_death", scale=1)
            self.wait_index = 0
            self.wait_active = True
            self.display.blit(self.wait_frames[self.wait_index], (0, 0))
            self.display.blit(self.start, self.start.get_rect(midright=(632, 350)))
            return

        self.death_index += 0.2
        if self.death_index >= len(self.death_frames): self.death_index = 253

        # display title and death stone text
        if self.death_index < 0.5:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (245, 223, 151, 15), (245, 223, 151, 15))

        # display first line
        elif 4 < self.death_index < 40:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (170, 111, 298, 16), (170, 111, 298, 16))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 40:
                    self.sound_index = 44

        # display second line
        elif 44 < self.death_index < 114:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (45, 141, 551, 19), (45, 141, 551, 19))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 114:
                    self.sound_index = 120

        # display third line
        elif 120 < self.death_index < 196:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (6, 262, 627, 19), (6, 262, 627, 19))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 196:
                    self.sound_index = 202

        # display last line
        elif 202 < self.death_index < 250:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (123, 292, 392, 15), (123, 292, 392, 15))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2

        # display death stone
        self.screen_surface.blit(self.death_frames[int(self.death_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        if self.death_completed:
            self.screen_surface.fill('black')

        self.display.blit(self.screen_surface, (0, 0))

    def curse(self):
        """ cut scene after winning curse stone """

        if self.curse_frames is None:
            self.screen_surface.blit(self.castle, (0, 0))
            self.screen_surface.blit(self.skip_animation, self.skip_animation.get_rect(midright=(632, 350)))
            self.sound_index = 4
            self.load_index = 2
            self.curse_frames = []

        # load frames one frame at a time for efficiency
        if self.load_index <= 149:
            if self.load_index < 10:
                self.curse_frames.append(
                    pygame.image.load(f"./assets/images/transitions/curse2/curse_00{self.load_index}.png").convert())
            elif self.load_index < 100:
                self.curse_frames.append(
                    pygame.image.load(f"./assets/images/transitions/curse2/curse_0{self.load_index}.png").convert())
            else:
                self.curse_frames.append(
                    pygame.image.load(f"./assets/images/transitions/curse2/curse_{self.load_index}.png").convert())
            self.load_index += 1

        # skip animation
        keys = pygame.key.get_pressed()
        if ((keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON))) and self.skip_active) or self.curse_index > 133:
            self.curse_completed = True
            if not self.curse_index > 133:
                self.sound.confirm.play()
            self.skip_active = False
            self.wait_frames = import_frames("./assets/images/transitions/wait_curse", scale=1)
            self.wait_index = 0
            self.wait_active = True
            self.display.blit(self.wait_frames[self.wait_index], (0, 0))
            self.display.blit(self.exit, self.exit.get_rect(midright=(632, 350)))
            return

        self.curse_index += 0.2
        if self.curse_index >= len(self.curse_frames): self.curse_index = 135

        # display title and curse stone text
        if self.curse_index < 0.5:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (244, 222, 152, 17), (244, 222, 152, 17))

        # display first line
        elif 4 < self.curse_index < 40:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (170, 111, 299, 16), (170, 111, 299, 16))
            if int(self.curse_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 40:
                    self.sound_index = 44

        # display second line
        elif 44 < self.curse_index < 98:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (107, 142, 424, 19), (107, 142, 424, 19))
            if int(self.curse_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 98:
                    self.sound_index = 106

        # display third line
        elif 105 < self.curse_index < 133:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (182, 262, 279, 20), (182, 262, 279, 20))
            if int(self.curse_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2

        # display curse stone
        self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        self.display.blit(self.screen_surface, (0, 0))

    def tower(self):
        """ display the towers """

        # move from start position to first tower
        if self.level == 1:
            if self.reached_tower1:
                self.change_tower()
            else:
                if not self.player_position_initialized:
                    self.display.blit(self.all_towers, (0, 0))
                    if self.p1_active:
                        self.p1_rect = self.p1_image.get_rect(bottomleft=(24, 288))
                    if self.p2_active:
                        self.p2_rect = self.p1_image.get_rect(bottomleft=(16, 288))
                    self.player_position_initialized = True
                self.go_to_tower(1)

        # move from first tower to second tower
        elif self.level == 6:
            if self.reached_tower2:
                self.change_tower()
            else:
                if not self.player_position_initialized:
                    self.display.blit(self.all_towers, (0, 0))
                    if self.p1_active:
                        self.p1_rect = self.p1_image.get_rect(bottomleft=(160, 96))
                    if self.p2_active:
                        self.p2_rect = self.p1_image.get_rect(bottomleft=(152, 96))
                    self.player_position_initialized = True
                self.go_to_tower(2)

        # move from second tower to third tower
        elif self.level == 11:
            if self.reached_tower3:
                self.change_tower()
            else:
                if not self.player_position_initialized:
                    self.display.blit(self.all_towers, (0, 0))
                    if self.p1_active:
                        self.p1_rect = self.p1_image.get_rect(bottomleft=(346, 96))
                    if self.p2_active:
                        self.p2_rect = self.p1_image.get_rect(bottomleft=(338, 96))
                    self.player_position_initialized = True
                self.go_to_tower(3)

        # make player move one floor up in a tower
        else:
            if self.path_index >= len(self.p1_path[0]):
                self.completed = True
                self.path_index = 0
                if self.p1_active:
                    self.p1_direction_changed = False
                    self.p1_image = self.p1_frames['idle'][0]
                if self.p2_active:
                    self.p2_direction_changed = False
                    self.p2_image = self.p2_frames['idle'][0]
            else:
                self.move_players()

            if self.p1_active and self.p1_flipped:
                self.p1_image = pygame.transform.flip(self.p1_image, True, False)
            if self.p2_active and self.p2_flipped:
                self.p2_image = pygame.transform.flip(self.p2_image, True, False)
            self.tower_surface.blit(self.tower_frames[int((self.level-1)/5)], (0, 0))
            if self.p2_active:
                self.tower_surface.blit(self.p2_image, self.p2_rect)
            if self.p1_active:
                self.tower_surface.blit(self.p1_image, self.p1_rect)

            self.display.blit(self.tower_surface, self.tower_rect)
            self.path_index += 1

    def move_players(self):
        """ make players move in the tower """

        x = (self.level - 1) % 5
        if x == 0:
            self.change_tower()
        else:
            if x % 2 == 0:
                if self.p1_active:
                    self.p1_direction.x = -1
                if self.p2_active:
                    self.p2_direction.x = -1
            else:
                if self.p1_active:
                    self.p1_direction.x = 1
                if self.p2_active:
                    self.p2_direction.x = 1

            if self.p1_active:
                if self.path_index > 18 and not self.p1_direction_changed:
                    self.p1_flipped = not self.p1_flipped
                    self.p1_direction_changed = True

                self.p1_rect.x += self.p1_direction.x * self.p1_path[0][int(self.path_index)][0]
                self.p1_rect.y -= self.p1_path[0][int(self.path_index)][1]
                if self.path_index % 6 == 0:
                    self.sound.player_move.play()

                status = self.p1_frames['walk']
                self.p1_frame_index += 0.2
                if self.p1_frame_index >= len(status):
                    self.p1_frame_index = 0

                self.p1_image = status[int(self.p1_frame_index)]

            if self.p2_active:
                if self.path_index > 26 and not self.p2_direction_changed:
                    self.p2_flipped = not self.p2_flipped
                    self.p2_direction_changed = True

                self.p2_rect.x += self.p2_direction.x * self.p2_path[0][int(self.path_index)][0]
                self.p2_rect.y -= self.p2_path[0][int(self.path_index)][1]
                if self.path_index % 6 == 0:
                    self.sound.player_move.play()

                status = self.p2_frames['walk']
                self.p2_frame_index += 0.2
                if self.p2_frame_index >= len(status):
                    self.p2_frame_index = 0

                self.p2_image = status[int(self.p2_frame_index)]

    def go_to_tower(self, tower):
        """ make the player move from one tower to another """
        if tower == 3:
            tower = 2
        self.screen_surface.blit(self.all_towers, (self.p1_rect.x - 16, self.p1_rect.y - 16, 36, 50), (self.p1_rect.x - 16, self.p1_rect.y - 16, 36, 50))
        if self.p1_active:
            self.p1_rect.x += self.p1_path[tower][int(self.path_index)][0]
            self.p1_rect.y += self.p1_path[tower][int(self.path_index)][1]
            if self.path_index % 6 == 0:
                self.sound.player_move.play()

            status = self.p1_frames['walk']
            self.p1_frame_index += 0.2
            if self.p1_frame_index >= len(status):
                self.p1_frame_index = 0

            self.p1_image = status[int(self.p1_frame_index)]

            self.screen_surface.blit(self.p1_image, self.p1_rect)

        if self.p2_active:
            self.p2_rect.x += self.p2_path[tower][int(self.path_index)][0]
            self.p2_rect.y += self.p2_path[tower][int(self.path_index)][1]
            if self.path_index % 6 == 0:
                self.sound.player_move.play()

            status = self.p2_frames['walk']
            self.p2_frame_index += 0.2
            if self.p2_frame_index >= len(status):
                self.p2_frame_index = 0

            self.p2_image = status[int(self.p2_frame_index)]

            self.screen_surface.blit(self.p2_image, self.p2_rect)

        self.display.blit(self.screen_surface, (self.p1_rect.x - 16, self.p1_rect.y - 16, 32, 48), (self.p1_rect.x - 16, self.p1_rect.y - 16, 32, 48))

        self.path_index += 1
        if self.path_index >= len(self.p1_path[tower]):
            self.path_index = 0
            if self.level == 1:
                self.reached_tower1 = True
            elif self.level == 6:
                self.reached_tower2 = True
            elif self.level == 11:
                self.reached_tower3 = True

    def stall(self):
        """ when the player movement is completed, wait for 1 sec to start the game """
        if self.path_index > 60:
            self.path_index = 0
            self.stall_completed = True
        self.path_index += 1

    def change_tower(self):
        """ after tower change scene, make the player position at ground floor of the new tower"""
        if self.stall_completed:
            self.tower_surface.blit(self.tower_frames[int((self.level - 1) / 5)], (0, 0))
            if self.p1_active:
                self.p1_image = self.p1_frames['idle'][0]
                self.p1_rect = self.p1_image.get_rect(bottomleft=(24, 288))
                self.tower_surface.blit(self.p1_image, self.p1_rect)
            if self.p2_active:
                self.p2_image = self.p2_frames['idle'][0]
                self.p2_rect = self.p1_image.get_rect(bottomleft=(16, 288))
                self.tower_surface.blit(self.p2_image, self.p2_rect)

            self.display.blit(self.tower_surface, self.tower_rect)

            self.completed = True
            self.stall_completed = False
            self.player_position_initialized = False
        else:
            self.stall()
