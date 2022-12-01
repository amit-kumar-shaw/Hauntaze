from enum import Enum

import pygame
from settings import *
from menu import Menu
from story_mode import StoryMode
from survival_mode import SurvivalMode


# Enum for game status
class Status(Enum):
    MENU = 1
    INTRO = 2
    RUNNING = 3
    PAUSED = 4
    OVER = 5


class Game:
    def __init__(self):
        self.status = Status.MENU
        self.menu = Menu()
        self.mode = None

    def run(self):
        if self.status == Status.MENU:
            self.menu.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] and (self.menu.is_player1_ready or self.menu.is_player2_ready):
                self.status = Status.RUNNING
                self.mode = SurvivalMode(player1=self.menu.is_player1_ready, player2=self.menu.is_player2_ready)
        elif self.status == Status.INTRO:
            pass
        elif self.status == Status.RUNNING:
            self.mode.run()
        elif self.status == Status.PAUSED:
            pass
        elif self.status == Status.OVER:
            pass

