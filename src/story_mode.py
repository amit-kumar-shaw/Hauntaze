from enum import Enum

import pygame
from settings import *
from level import Level
from player import Player
from stones import StonesUI
from transitions import StoryTransition
from ui import UI


class Status(Enum):
    """ story mode states """
    RUNNING = 1
    COMPLETED = 2
    TRANSITION = 3


class StoryMode:
    """ logic for the story mode """
    def __init__(self, player1=False, player2=False, joysticks=None):

        self.joysticks = joysticks
        self.joystick_1 = None
        self.joystick_2 = None
        if joysticks is not None:
            self.joystick_1 = joysticks[0] if len(joysticks) > 0 else None
            self.joystick_2 = joysticks[1] if len(joysticks) > 1 else None

        # start mode with game intro cut scene
        self.status = Status.TRANSITION

        self.player1_active = player1
        self.player2_active = player2
        self.player1 = None
        self.player2 = None
        self.multiplayer = False

        # instantiate players
        if player1 and player2:
            self.multiplayer = True

        if player1:
            self.player1 = Player((0, 0), PLAYER1_SPRITE,
                                  collision_sprites=None, collectible_sprites=None, enemy_sprites=None,
                                  joystick=self.joystick_1)
        if player2:
            self.player2 = Player((0, 0), PLAYER2_SPRITE,
                                  collision_sprites=None, collectible_sprites=None, enemy_sprites=None,
                                  joystick=self.joystick_2, player2=True)

        # start game with level 1
        self.current_level = 1

        # instantiate first level
        self.level = Level(True, self.player1_active, self.player1, self.player2_active, self.player2,
                           self.current_level, multiplayer=self.multiplayer,
                           joystick_1=self.joystick_1, joystick_2=self.joystick_2)

        # instantiate score/health UI
        self.ui = UI(player1, player2, self.level)
        self.ui.current_level = self.current_level
        self.ui.update_level()

        # instantiate special stones view
        self.stones = StonesUI()

        # instantiate cut scene transitions
        self.transition = StoryTransition(self.player1_active, self.player2_active,
                                          joystick_1=self.joystick_1, joystick_2=self.joystick_2)

    def run(self):
        """ run the story mode logic """

        # run game level and check for completion
        if self.status == Status.RUNNING:

            # run the game level
            self.level.run()

            # update ui only if needs updating
            if (self.player1_active and self.player1.ui_update) or (self.player2_active and self.player2.ui_update):
                self.ui.update()
                if self.player1_active:
                    self.player1.ui_update = False
                if self.player2_active:
                    self.player2.ui_update = False

            # check if level completed and player status
            if self.level.completed:
                self.status = Status.COMPLETED
                if self.transition.multiplayer and not self.transition.ghost_active:
                    self.transition.p1_active = self.level.player1_active
                    self.transition.p2_active = self.level.player2_active

        # make the next level ready
        elif self.status == Status.COMPLETED:

            # reset some player properties for new level
            if self.player1_active:
                self.player1.reset()
            if self.player2_active:
                self.player2.reset()

            self.current_level += 1

            self.transition.completed = False

            # add life stone on clearing level 5
            if self.current_level == 6:
                if self.player1_active:
                    self.player1.life_stone_available = True
                if self.player2_active:
                    self.player2.life_stone_available = True

            # add death stone on clearing level 10
            if self.current_level == 11:
                if self.player1_active:
                    self.player1.death_stone_available = True
                if self.player2_active:
                    self.player2.death_stone_available = True

            # instantiate new level
            if self.current_level <= 15:
                self.level = Level(True, self.player1_active, self.player1, self.player2_active, self.player2,
                                   self.current_level, multiplayer=self.multiplayer,
                                   joystick_1=self.joystick_1, joystick_2=self.joystick_2)

                # update ui
                self.ui.level = self.level
                self.ui.current_level = self.current_level
                self.ui.update_level()

            self.status = Status.TRANSITION

        elif self.status == Status.TRANSITION:

            self.transition.level = self.current_level

            # update cut scene frames
            self.transition.update()

            if self.transition.completed:
                self.status = Status.RUNNING

        # activate stones ui based on the level
        if self.current_level > 5:
            self.stones.stones[0].active = True
        if self.current_level > 10:
            self.stones.stones[1].active = True
        if self.current_level > 15:
            self.stones.stones[2].active = True

        # always display stones ui
        self.stones.update()
