from enum import Enum

import pygame
from settings import *
from level import Level
from player import Player
from ui import UI


class Status(Enum):
    RUNNING = 1
    COMPLETED = 2


class StoryMode:
    def __init__(self, player1=False, player2=False):
        self.status = Status.RUNNING
        self.player1_active = player1
        self.player2_active = player2
        self.player1 = None
        self.player2 = None
        self.multiplayer = False
        if player1 and player2:
            self.multiplayer = True
        if player1:
            self.player1 = Player((0, 0), PLAYER1_SPRITE,
                                  collision_sprites=None, collectible_sprites=None, enemy_sprites=None)
        if player2:
            self.player2 = Player((0, 0), PLAYER2_SPRITE,
                                  collision_sprites=None, collectible_sprites=None, enemy_sprites=None, player2=True)
        self.current_level = 4
        self.level = Level(True, self.player1_active, self.player1, self.player2_active, self.player2, self.current_level, multiplayer=self.multiplayer)
        self.ui = UI(player1, player2, self.level)
        self.ui.current_level = self.current_level
        self.ui.update_level()

    def run(self):
        if self.status == Status.RUNNING:
            self.level.run()
            if (self.player1_active and self.player1.ui_update) or (self.player2_active and self.player2.ui_update):
                self.ui.update()
                if self.player1_active:
                    self.player1.ui_update = False
                if self.player2_active:
                    self.player2.ui_update = False
            if self.level.completed:
                self.status = Status.COMPLETED
        elif self.status == Status.COMPLETED:
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_RETURN]:
            if self.player1_active: self.player1.reset()
            if self.player2_active: self.player2.reset()
            self.current_level += 1
            self.level = Level(True, self.player1_active, self.player1, self.player2_active, self.player2, self.current_level, multiplayer=self.multiplayer)
            self.ui.level = self.level
            self.ui.current_level = self.current_level
            self.ui.update_level()
            self.status = Status.RUNNING
