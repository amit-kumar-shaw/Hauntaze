from enum import Enum

import pygame

from settings import *
from menu import Menu
from story_mode import StoryMode
from survival_mode import SurvivalMode
from sounds import GameSound


# Enum for game status
class Status(Enum):
    """Different game states"""
    MENU = 1
    RUNNING = 2
    PAUSED = 3
    OVER = 4


class Game:
    """Main game flow"""

    def __init__(self, joysticks=None):
        self.status = Status.MENU
        self.mode = None
        self.pause_animation = 0
        self.exit_active = False
        self.sound = GameSound()
        self.joysticks = joysticks
        self.joystick = joysticks[0] if joysticks is not None else None

        # instantiate menu
        self.menu = Menu(self.joystick)
        self.sound.play_background(self.sound.menu)

        # for pause screen
        self.pause_surface = pygame.Surface((SCREEN_WIDTH, (ROWS * CELL_SIZE * TILE_HEIGHT)))
        self.resume_text = pygame.image.load("./assets/images/transitions/resume.png").convert_alpha()

    def run(self):
        """run the game logic"""

        # get the keyboard input
        keys = pygame.key.get_pressed()

        # show menu screen
        if self.status == Status.MENU:

            # update menu frames
            self.menu.update()

            # check start button after coin inserted
            if (keys[CONFIRM] or (
                    self.joystick is not None and self.joystick.get_button(START_BUTTON))) and self.menu.coin_inserted:
                self.menu.sound.confirm.play()
                self.sound.stop_background()

                # change game state
                self.status = Status.RUNNING

                # instantiate game mode based on menu input
                if self.menu.is_story_mode:
                    self.mode = StoryMode(player1=self.menu.is_player1_ready, player2=self.menu.is_player2_ready,
                                          joysticks=self.joysticks)
                else:
                    self.mode = SurvivalMode(player1=self.menu.is_player1_ready, player2=self.menu.is_player2_ready,
                                             joysticks=self.joysticks)

        # run the game
        elif self.status == Status.RUNNING:

            # run game mode
            self.mode.run()

            # check for pause button when game mode is running
            if (self.mode.status.value == 1) and (
                    keys[PAUSE] or (self.joystick is not None and self.joystick.get_button(RED_BUTTON))):
                self.status = Status.PAUSED
                self.exit_active = False

            # end game when player failed level
            if self.mode.level.failed:
                self.status = Status.OVER

        # show pause screen
        elif self.status == Status.PAUSED:

            # show pause
            self.pause()

            # check to resume game
            if keys[CONFIRM] or (self.joystick is not None and self.joystick.get_button(START_BUTTON)):
                self.status = Status.RUNNING

        # end game and load menu when game is over
        elif self.status == Status.OVER:
            self.status = Status.MENU
            self.menu = Menu(self.joystick)
            self.sound.play_background(self.sound.menu)

    def pause(self):
        """ Display pause screen """

        self.pause_surface.fill('black')

        self.pause_animation += 0.08

        if self.pause_animation >= 2:
            self.pause_animation = 0

        # Pause message
        font = pygame.font.Font('./assets/fonts/1.ttf', 40 + int(self.pause_animation))
        title = font.render('Game Paused', False, 'red')
        title_rect = title.get_rect(midbottom=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
        self.pause_surface.blit(title, title_rect)

        title = font.render('Game Paused', False, 'yellow')
        title_rect = title.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pause_surface.blit(title, title_rect)

        # Resume game button
        msg_rect = self.resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))
        self.pause_surface.blit(self.resume_text, msg_rect)

        pygame.display.get_surface().blit(self.pause_surface, (0, 0))
