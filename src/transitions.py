import sys
import time

import pygame
from settings import *
from stones import Stone
from utilities import import_frames
from music import TransitionSound


class Transition:
    def __init__(self, p1, p2, joystick_1=None, joystick_2=None):

        self.joystick_1 = joystick_1
        self.joystick_2 = joystick_2

        self.display = pygame.display.get_surface()
        self.sound = TransitionSound()
        self.sound_index = 0
        self.load_index = 2

        # self.multiplayer = multiplayer
        self.tower_surface = pygame.Surface((64, 320))

        self.tower_rect = self.tower_surface.get_rect(topleft=(576, 0))
        self.screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.castle = pygame.image.load("./assets/images/transitions/castle.png").convert_alpha()

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
        # self.tower1_frames = pygame.image.load(f"./assets/images/transitions/tower/tower_1.png").convert_alpha()
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
        if self.multiplayer and not self.ghost_active and not (self.p1_active and self.p2_active):
            self.activate_ghost()

        if self.level <= 5:
            if not self.intro_completed:
                self.intro()
            else:
                self.tower()
        elif 5 < self.level <= 10:
            if not self.life_completed:
                self.life()
            else:
                self.tower()
        elif 10 < self.level <= 15:
            if not self.death_completed:
                self.death()
            else:
                self.tower()
        else:
            self.curse()
        #
        # self.draw()

    def activate_ghost(self):
        if not self.p1_active:
            self.p1_frames = self.ghost_frames
            self.p1_active = True
        elif not self.p2_active:
            self.p2_frames = self.ghost_frames
            self.p2_active = True
        self.ghost_active = True

    def intro(self):
        if self.intro_frames is None:
            # self.intro_frames = import_frames(f"./assets/images/transitions/intro2", scale=1)
            # self.screen_surface.fill('black')
            self.screen_surface.blit(self.castle, (0, 0))
            self.sound_index = 4
            self.load_index = 2
            self.intro_frames = []

        if self.load_index <= 299:
            if self.load_index < 10:
                self.intro_frames.append(pygame.image.load(f"./assets/images/transitions/intro2/intro_00{self.load_index}.png").convert())
            elif self.load_index < 100:
                self.intro_frames.append(pygame.image.load(f"./assets/images/transitions/intro2/intro_0{self.load_index}.png").convert())
            else:
                self.intro_frames.append(pygame.image.load(f"./assets/images/transitions/intro2/intro_{self.load_index}.png").convert())
            self.load_index += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON)):
            self.intro_completed = True

        self.intro_index += 0.2
        if self.intro_index >= len(self.intro_frames): self.intro_index = 225

        # self.screen_surface = self.intro_frames[int(self.intro_index)]
        if self.intro_index < 0.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (160, 50, 320, 20), (160, 50, 320, 20))
        elif 4 < self.intro_index < 74:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (35, 112, 572, 16), (35, 112, 572, 16))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 74:
                    self.sound_index = 80
        elif 80 < self.intro_index < 117:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (172, 144, 297, 13), (172, 144, 297, 13))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 116:
                    self.sound_index = 131
        elif 131 < self.intro_index < 131.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (95, 222, 130, 14), (95, 222, 130, 14))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.appear.play()
                self.sound_index = 145
        elif 145 < self.intro_index < 145.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (245, 222, 150, 16), (245, 222, 150, 16))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.appear.play()
                self.sound_index = 160
        elif 160 < self.intro_index < 160.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (405, 222, 152, 15), (405, 222, 152, 15))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.appear.play()
                self.sound_index = 176
        elif 175 < self.intro_index < 222:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (126, 263, 387, 16), (126, 263, 387, 16))
            if int(self.intro_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
        if 131 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (139, 180, 44, 40), (139, 180, 44, 40))
        if 145 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (299, 181, 42, 39), (299, 181, 42, 39))
        if 160 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (458, 182, 44, 39), (458, 182, 44, 39))

        if self.intro_completed:
            self.screen_surface.fill('black')
        self.display.blit(self.screen_surface, (0, 0))

    def life(self):
        if self.life_frames is None:
            # self.life_frames = import_frames(f"./assets/images/transitions/life", scale=1)
            # self.screen_surface.fill('black')
            self.screen_surface.blit(self.castle, (0, 0))
            self.sound_index = 4
            self.load_index = 2
            self.life_frames = []

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON)):
            self.life_completed = True

        self.life_index += 0.2
        if self.life_index >= len(self.life_frames): self.life_index = 265

        # self.screen_surface = self.life_frames[int(self.life_index)]
        if self.life_index < 0.5:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (255, 223, 131, 14), (255, 223, 131, 14))
        elif 4 < self.life_index < 39:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (180, 112, 280, 15), (180, 112, 280, 15))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 38:
                    self.sound_index = 44
        elif 44 < self.life_index < 112:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (48, 142, 542, 18), (48, 142, 542, 18))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 112:
                    self.sound_index = 130
        elif 130 < self.life_index < 196:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (46, 262, 548, 19), (46, 262, 548, 19))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 196:
                    self.sound_index = 202
        elif 202 < self.life_index < 261:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (82, 290, 475, 21), (82, 290, 475, 21))
            if int(self.life_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2

        self.screen_surface.blit(self.life_frames[int(self.life_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        if self.life_completed:
            self.screen_surface.fill('black')

        self.display.blit(self.screen_surface, (0, 0))

    def death(self):
        if self.death_frames is None:
            # self.death_frames = import_frames(f"./assets/images/transitions/death", scale=1)
            self.screen_surface.blit(self.castle, (0, 0))
            self.sound_index = 4
            self.load_index = 2
            self.death_frames = []

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON)):
            self.death_completed = True

        self.death_index += 0.2
        if self.death_index >= len(self.death_frames): self.death_index = 253

        # self.screen_surface = self.death_frames[int(self.death_index)]
        if self.death_index < 0.5:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (245, 223, 151, 15), (245, 223, 151, 15))
        elif 4 < self.death_index < 40:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (170, 111, 298, 16), (170, 111, 298, 16))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 40:
                    self.sound_index = 44
        elif 44 < self.death_index < 114:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (45, 141, 551, 19), (45, 141, 551, 19))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 114:
                    self.sound_index = 120
        elif 120 < self.death_index < 196:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (6, 262, 627, 19), (6, 262, 627, 19))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 196:
                    self.sound_index = 202
        elif 202 < self.death_index < 250:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (123, 292, 392, 15), (123, 292, 392, 15))
            if int(self.death_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2

        self.screen_surface.blit(self.death_frames[int(self.death_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        if self.death_completed:
            self.screen_surface.fill('black')

        self.display.blit(self.screen_surface, (0, 0))

    def curse(self):
        if self.curse_frames is None:
            # self.curse_frames = import_frames(f"./assets/images/transitions/curse", scale=1)
            self.screen_surface.blit(self.castle, (0, 0))
            self.sound_index = 4
            self.load_index = 2
            self.curse_frames = []

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON)):
            self.curse_completed = True
            pygame.quit()
            sys.exit()

        self.curse_index += 0.2
        if self.curse_index >= len(self.curse_frames): self.curse_index = 135

        # self.screen_surface = self.curse_frames[int(self.curse_index)]
        if self.curse_index < 0.5:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (244, 222, 152, 17), (244, 222, 152, 17))
        elif 4 < self.curse_index < 40:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (170, 111, 299, 16), (170, 111, 299, 16))
            if int(self.curse_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 40:
                    self.sound_index = 44
        elif 44 < self.curse_index < 98:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (107, 142, 424, 19), (107, 142, 424, 19))
            if int(self.curse_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2
                if self.sound_index == 98:
                    self.sound_index = 106
        elif 105 < self.curse_index < 133:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (182, 262, 279, 20), (182, 262, 279, 20))
            if int(self.curse_index) % self.sound_index == 0:
                self.sound.typing.play()
                self.sound_index += 2

        self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        self.display.blit(self.screen_surface, (0, 0))

    def tower(self):

        if self.level == 1:
            if self.reached_tower1:
                self.change_tower()
            else:
                if not self.player_position_initialized:
                    if self.p1_active:
                        self.p1_rect = self.p1_image.get_rect(bottomleft=(24, 288))
                    if self.p2_active:
                        self.p2_rect = self.p1_image.get_rect(bottomleft=(16, 288))
                    self.player_position_initialized = True
                self.go_to_tower(1)
        elif self.level == 6:
            if self.reached_tower2:
                self.change_tower()
            else:
                if not self.player_position_initialized:
                    if self.p1_active:
                        self.p1_rect = self.p1_image.get_rect(bottomleft=(160, 96))
                    if self.p2_active:
                        self.p2_rect = self.p1_image.get_rect(bottomleft=(152, 96))
                    self.player_position_initialized = True
                self.go_to_tower(2)
        elif self.level == 11:
            if self.reached_tower3:
                self.change_tower()
            else:
                if not self.player_position_initialized:
                    if self.p1_active:
                        self.p1_rect = self.p1_image.get_rect(bottomleft=(346, 96))
                    if self.p2_active:
                        self.p2_rect = self.p1_image.get_rect(bottomleft=(338, 96))
                    self.player_position_initialized = True
                self.go_to_tower(3)
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
        x = (self.level - 1) % 5 #if self.level % 5 != 0 else 5
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
                # self.sound.player_move.stop()
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
        if tower == 3:
            tower = 2
        self.screen_surface.blit(self.all_towers, (0, 0))
        if self.p1_active:
            # if self.path_index > 18 and not self.p1_direction_changed:
            #     self.p1_flipped = not self.p1_flipped
            #     self.p1_direction_changed = True
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
            # if self.path_index > 26 and not self.p2_direction_changed:
            #     self.p2_flipped = not self.p2_flipped
            #     self.p2_direction_changed = True

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

        self.display.blit(self.screen_surface, (0, 0))

        self.path_index +=1
        if self.path_index >= len(self.p1_path[tower]):
            self.path_index = 0
            if self.level == 1:
                self.reached_tower1 = True
            elif self.level == 6:
                self.reached_tower2 = True
            elif self.level == 11:
                self.reached_tower3 = True

    def stall(self):
        if self.path_index > 60:
            self.path_index = 0
            self.stall_completed = True
        self.path_index += 1

    def change_tower(self):
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


    def draw(self):

        if self.level == 1 or self.level == 6 or self.level == 11 or self.level == 16:
            self.display.blit(self.screen_surface, (0, 0))
        else:
            self.display.blit(self.tower_surface, self.tower_rect)

    def intro_gen(self):
        self.frame_index += 1
        for stone in self.stones:
            stone.animate()
        self.screen_surface.fill('black')
        self.screen_surface.blit(self.castle, (0, 0))
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Welcome to Hauntaze!', False, 'red')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2 + 1, 60 + 1))
        self.screen_surface.blit(msg, msg_rect)
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Welcome to Hauntaze!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'The search of forbidden treasure has cursed you to turn into a ghost.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'To lift the curse you need to collect:'
        if self.frame_index > 80:
            if self.frame_index - 80 < len(m1):
                m1 = m1[0:self.frame_index - 80]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 130:
            self.stones[0].rect = self.stones[0].image.get_rect(center=(160, 200))
            self.screen_surface.blit(self.stones[0].image, self.stones[0].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Life Stone', False, 'white')
            msg_rect = msg.get_rect(center=(160, 230))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 145:
            self.stones[1].rect = self.stones[1].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[1].image, self.stones[1].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Death Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 160:
            self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
            self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Curse Stone', False, 'white')
            msg_rect = msg.get_rect(center=(480, 230))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Defeat the stone defenders and lift your curse.'
        if self.frame_index > 175:
            if self.frame_index - 175 < len(m1):
                m1 = m1[0:self.frame_index - 175]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        self.display.blit(self.screen_surface, (0, 0))

        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/intro2/intro_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/intro2/intro_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/intro2/intro_{self.frame_index}.png')

    def stone_gen(self):
        self.frame_index += 1

        self.stones[0].active = True
        self.stones[1].active = False
        self.stones[2].active = False
        self.stones[0].animate()
        # for stone in self.stones:
        #     stone.animate()
        self.screen_surface.fill('black')
        self.screen_surface.blit(self.castle, (0, 0))
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, (3, 135, 25))
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2 + 1, 60 + 1))
        self.screen_surface.blit(msg, msg_rect)
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Life Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'The Life Stone gives you the power to revive yourself once you die.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index - 45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 0:
            self.stones[0].rect = self.stones[0].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[0].image, self.stones[0].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Life Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #     self.stones[1].rect = self.stones[1].image.get_rect(center=(320, 200))
        #     self.screen_surface.blit(self.stones[1].image, self.stones[1].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Death Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(320, 230))
        #     self.screen_surface.blit(msg, msg_rect)
        #
        # if self.frame_index > 0:
        #     self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
        #     self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Curse Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(480, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        m1 = 'Remember, you can revive yourself only once during the whole game.'
        if self.frame_index > 130:
            if self.frame_index - 130 < len(m1):
                m1 = m1[0:self.frame_index - 130]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Press the Blue button within 10 seconds to revive yourself.'
        if self.frame_index > 202:
            if self.frame_index - 202 < len(m1):
                m1 = m1[0:self.frame_index - 202]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 300))
            self.screen_surface.blit(msg, msg_rect)

        self.display.blit(self.screen_surface, (0, 0))

        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/life/life_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface, f'./assets/images/transitions/life/life_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/life/life_{self.frame_index}.png')

    def stone2_gen(self):
        self.frame_index += 1

        self.stones[0].active = True
        self.stones[1].active = True
        self.stones[2].active = False
        self.stones[0].animate()
        self.stones[1].animate()
        # for stone in self.stones:
        #     stone.animate()
        self.screen_surface.fill('black')
        self.screen_surface.blit(self.castle, (0, 0))
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, (3, 135, 25))
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2 + 1, 60 + 1))
        self.screen_surface.blit(msg, msg_rect)
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Death Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'The Death Stone gives you the power to kill all your enemies at once.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index - 45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #
        #     self.stones[0].rect = self.stones[0].image.get_rect(center=(320, 200))
        #     self.screen_surface.blit(self.stones[0].image, self.stones[0].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Life Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(320, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 0:
            self.stones[1].rect = self.stones[1].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[1].image, self.stones[1].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Death Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #     self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
        #     self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Curse Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(480, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        m1 = 'Remember, the Death Stone can be activated only once during the whole game.'
        if self.frame_index > 120:
            if self.frame_index - 120 < len(m1):
                m1 = m1[0:self.frame_index - 120]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Press the Yellow button to activate Death Stone.'
        if self.frame_index > 202:
            if self.frame_index - 202 < len(m1):
                m1 = m1[0:self.frame_index - 202]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 300))
            self.screen_surface.blit(msg, msg_rect)
        self.display.blit(self.screen_surface, (0, 0))
        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/death2/death_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/death2/death_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/death2/death_{self.frame_index}.png')

    def stone3_gen(self):
        self.frame_index += 1

        self.stones[0].active = True
        self.stones[1].active = True
        self.stones[2].active = True
        self.stones[0].animate()
        self.stones[1].animate()
        self.stones[2].animate()
        # for stone in self.stones:
        #     stone.animate()
        self.screen_surface.fill('black')
        self.screen_surface.blit(self.castle, (0, 0))
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, (3, 135, 25))
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2 + 1, 60 + 1))
        self.screen_surface.blit(msg, msg_rect)
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Curse Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Your curse is lifted and forbidden treasure is yours.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index - 45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #
        #     self.stones[0].rect = self.stones[0].image.get_rect(center=(320, 200))
        #     self.screen_surface.blit(self.stones[0].image, self.stones[0].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Life Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(320, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 0:
            self.stones[2].rect = self.stones[2].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Curse Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #     self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
        #     self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Curse Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(480, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have completed Hauntaze.'
        if self.frame_index > 105:
            if self.frame_index - 105 < len(m1):
                m1 = m1[0:self.frame_index - 105]
            font = pygame.font.Font('./assets/fonts/1.ttf', 15)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        self.display.blit(self.screen_surface, (0, 0))

        if self.frame_index < 150:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/curse2/curse_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/curse2/curse_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/curse2/curse_{self.frame_index}.png')
