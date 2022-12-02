import pygame
from settings import *
from level import Level
from ui import UI


class SurvivalMode:
    def __init__(self, player1=False, player2=False):
        self.status = None
        self.player1_active = player1
        self.player2_active = player2
        self.level = Level(player1, player2)
        self.ui = UI(player1, player2, self.level)

    def run(self):
        self.level.run()
        self.ui.update()
