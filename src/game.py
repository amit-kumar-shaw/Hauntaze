import sys
from enum import Enum

import pygame
from settings import *
from menu import Menu
from story_mode import StoryMode
from survival_mode import SurvivalMode
from music import GameSound


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
        self.pause_animation = 0
        self.exit_active = False
        self.sound = GameSound()

    def run(self):
        keys = pygame.key.get_pressed()

        # show menu screen
        if self.status == Status.MENU:
            self.menu.update()
            if keys[pygame.K_RETURN] and (self.menu.is_player1_ready or self.menu.is_player2_ready):
                self.sound.play_confirmation()
                self.menu.sound.menu.stop()
                self.status = Status.RUNNING
                if self.menu.is_story_mode:
                    self.mode = StoryMode(player1=self.menu.is_player1_ready, player2=self.menu.is_player2_ready)
                else:
                    self.mode = SurvivalMode(player1=self.menu.is_player1_ready, player2=self.menu.is_player2_ready)

        # show game intro
        elif self.status == Status.INTRO:
            pass

        # run the game
        elif self.status == Status.RUNNING:
            self.mode.fps = self.fps
            self.mode.run()

            if keys[pygame.K_ESCAPE]:
                self.status = Status.PAUSED
                self.exit_active = False
                # events = pygame.event.get()
                # for event in events:
                #     if event.type == pygame.KEYDOWN:
                #         self.status = Status.RUNNING
            if self.mode.level.failed:
                self.status = Status.OVER

        # show pause screen
        elif self.status == Status.PAUSED:
            self.pause()
            if not keys[pygame.K_ESCAPE]:
                self.exit_active = True
            if keys[pygame.K_RETURN]:
                self.status = Status.RUNNING
            elif keys[pygame.K_ESCAPE] and self.exit_active:
                # pass
                pygame.quit()
                sys.exit()

        # end game and load menu
        elif self.status == Status.OVER:
            self.status = Status.MENU
            self.menu = Menu()

    def pause(self):
        pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pause_surface.fill('black')

        self.pause_animation += 0.08

        if self.pause_animation >= 2: self.pause_animation = 0

        # Pause message
        font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 60 + int(self.pause_animation))
        title = font.render('Game Paused', False, 'red')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
        pause_surface.blit(title, title_rect)

        title = font.render('Game Paused', False, 'yellow')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pause_surface.blit(title, title_rect)

        # Resume game message
        font = pygame.font.Font('./assets/fonts/1.ttf', 15)
        resume_msg = font.render('Press ENTER to resume', False, 'white')
        msg_rect = resume_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        pause_surface.blit(resume_msg, msg_rect)

        # Exit game message
        font = pygame.font.Font('./assets/fonts/4.ttf', 16)
        exit_msg = font.render('ESC: Exit', False, 'white')
        msg_rect = exit_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        pause_surface.blit(exit_msg, msg_rect)

        pygame.display.get_surface().blit(pause_surface, (0, 0))

    def exit_menu(self):
        pass

