import sys
import time
from enum import Enum

import pygame

from settings import *
from menu import Menu
from story_mode import StoryMode
from survival_mode import SurvivalMode
from sounds import GameSound




# Enum for game status
class Status(Enum):
    MENU = 1
    INTRO = 2
    RUNNING = 3
    PAUSED = 4
    OVER = 5


class Game:

    def __init__(self, joysticks=None):
        self.status = Status.MENU
        self.mode = None
        self.pause_animation = 0
        self.exit_active = False
        self.sound = GameSound()
        self.joysticks = joysticks
        self.joystick = joysticks[0] if joysticks is not None else None

        self.menu = Menu(self.joystick)
        self.sound.play_background(self.sound.menu)
        self.page = 1

    def run(self):
        keys = pygame.key.get_pressed()
        # show menu screen
        if self.status == Status.MENU:

            self.menu.update()

            if (keys[CONFIRM] or (self.joystick is not None and self.joystick.get_button(START_BUTTON))) and self.menu.coin_inserted:
                self.menu.sound.confirm.play()
                self.sound.stop_background()
                # self.menu.sound.menu.stop()
                self.status = Status.RUNNING
                if self.menu.is_story_mode:
                    self.mode = StoryMode(player1=self.menu.is_player1_ready, player2=self.menu.is_player2_ready, joysticks=self.joysticks)
                else:
                    self.mode = SurvivalMode(player1=self.menu.is_player1_ready, player2=self.menu.is_player2_ready, joysticks=self.joysticks)

        # show game intro
        elif self.status == Status.INTRO:
            self.intro()

        # run the game
        elif self.status == Status.RUNNING:
            self.mode.run()

            if keys[PAUSE] or (self.joystick is not None and self.joystick.get_button(RED_BUTTON)):
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
            # if not keys[pygame.K_ESCAPE]:
            #     self.exit_active = True
            if keys[CONFIRM] or (self.joystick is not None and self.joystick.get_button(START_BUTTON)):
                self.status = Status.RUNNING
            # elif keys[pygame.K_ESCAPE] and self.exit_active:
            #     # pass
            #     pygame.quit()
            #     sys.exit()

        # end game and load menu
        elif self.status == Status.OVER:
            self.status = Status.MENU
            self.menu = Menu()
            self.sound.play_background(self.sound.menu)

    def pause(self):
        pause_surface = pygame.Surface((SCREEN_WIDTH, (ROWS * CELL_SIZE * TILE_HEIGHT)))
        pause_surface.fill('black')

        self.pause_animation += 0.08

        if self.pause_animation >= 2: self.pause_animation = 0

        # Pause message
        # font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 60 + int(self.pause_animation))
        font = pygame.font.Font('./assets/fonts/1.ttf', 40 + int(self.pause_animation))
        title = font.render('Game Paused', False, 'red')
        title_rect = title.get_rect(midbottom=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
        pause_surface.blit(title, title_rect)

        title = font.render('Game Paused', False, 'yellow')
        title_rect = title.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pause_surface.blit(title, title_rect)

        # Resume game message
        font = pygame.font.Font('./assets/fonts/4.ttf', 24)
        resume_msg = font.render('Press Start to resume', False, 'white')
        msg_rect = resume_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        pause_surface.blit(resume_msg, msg_rect)

        # Exit game message
        # font = pygame.font.Font('./assets/fonts/4.ttf', 16)
        # exit_msg = font.render('ESC: Exit', False, 'white')
        # msg_rect = exit_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        # pause_surface.blit(exit_msg, msg_rect)

        pygame.display.get_surface().blit(pause_surface, (0, 0))

    # def intro(self):
    #
    #     keys = pygame.key.get_pressed()
    #
    #     pause_surface = pygame.image.load(f'assets/images/background/intro_1.jpeg').convert()
    #     pause_surface = pygame.transform.rotozoom(pause_surface, 0, 1 / 3)
    #
    #     self.pause_animation += 0.08
    #     if self.pause_animation >= 2: self.pause_animation = 0
    #     font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 40 + int(self.pause_animation))
    #
    #     title = font.render('Here it is, the castle of Dracula', False, 'red')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
    #     pause_surface.blit(title, title_rect)
    #     title = font.render('Here it is, the castle of Dracula', False, 'white')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #     pause_surface.blit(title, title_rect)
    #
    #     font = pygame.font.Font('./assets/fonts/1.ttf', 15)
    #     resume_msg = font.render('Press ENTER to next page', False, 'white')
    #     msg_rect = resume_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    #     pause_surface.blit(resume_msg, msg_rect)
    #
    #     pause_surface_2 = pygame.image.load(f'assets/images/background/intro_2.jpeg').convert()
    #     pause_surface_2 = pygame.transform.rotozoom(pause_surface_2, 0, 1 / 3)
    #     font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 40 + int(self.pause_animation))
    #     title = font.render('Full of treasure', False, 'red')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
    #     pause_surface_2.blit(title, title_rect)
    #     title = font.render('Full of treasure', False, 'white')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #     pause_surface_2.blit(title, title_rect)
    #
    #     pause_surface_3 = pygame.image.load(f'assets/images/background/intro_3.jpeg').convert()
    #     pause_surface_3 = pygame.transform.rotozoom(pause_surface_3, 0, 1 / 3)
    #     font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 40 + int(self.pause_animation))
    #     title = font.render('Also with danger', False, 'red')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
    #     pause_surface_3.blit(title, title_rect)
    #     title = font.render('Also with danger', False, 'white')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #     pause_surface_3.blit(title, title_rect)
    #
    #     pause_surface_4 = pygame.image.load(f'assets/images/background/intro_4.jpeg').convert()
    #     pause_surface_4 = pygame.transform.rotozoom(pause_surface_4, 0, 1 / 3)
    #     font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 40 + int(self.pause_animation))
    #     title = font.render('This night', False, 'red')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
    #     pause_surface_4.blit(title, title_rect)
    #     title = font.render('This night', False, 'white')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #     pause_surface_4.blit(title, title_rect)
    #
    #     pause_surface_5 = pygame.image.load(f'assets/images/background/intro_5.jpeg').convert()
    #     pause_surface_5 = pygame.transform.rotozoom(pause_surface_5, 0, 1 / 3)
    #     font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 40 + int(self.pause_animation))
    #     title = font.render('The treasure hunter comes here', False, 'red')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
    #     pause_surface_5.blit(title, title_rect)
    #     title = font.render('The treasure hunter comes here', False, 'white')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #     pause_surface_5.blit(title, title_rect)
    #
    #     pause_surface_6 = pygame.image.load(f'assets/images/background/intro_5.jpeg').convert()
    #     pause_surface_6 = pygame.transform.rotozoom(pause_surface_6, 0, 1 / 3)
    #     font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 40 + int(self.pause_animation))
    #     title = font.render('Can you escape the maze?', False, 'red')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
    #     pause_surface_6.blit(title, title_rect)
    #     title = font.render('Can you escape the maze?', False, 'white')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #     pause_surface_6.blit(title, title_rect)
    #
    #     pause_surface_7 = pygame.image.load(f'assets/images/background/intro_5.jpeg').convert()
    #     pause_surface_7 = pygame.transform.rotozoom(pause_surface_7, 0, 1 / 3)
    #     font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 40 + int(self.pause_animation))
    #     title = font.render('Or you will lost forever..', False, 'red')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2 + 1))
    #     pause_surface_7.blit(title, title_rect)
    #     title = font.render('Or you will lost forever..', False, 'white')
    #     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #     pause_surface_7.blit(title, title_rect)
    #
    #     if self.page == 1:
    #       pygame.display.get_surface().blit(pause_surface, (0, 0))
    #
    #     elif self.page == 2:
    #       pygame.display.get_surface().blit(pause_surface_2, (0, 0))
    #
    #     elif self.page == 3:
    #       pygame.display.get_surface().blit(pause_surface_3, (0, 0))
    #
    #     elif self.page == 4:
    #       pygame.display.get_surface().blit(pause_surface_4, (0, 0))
    #
    #     elif self.page == 5:
    #       pygame.display.get_surface().blit(pause_surface_5, (0, 0))
    #
    #     elif self.page == 6:
    #       pygame.display.get_surface().blit(pause_surface_6, (0, 0))
    #
    #     elif self.page == 7:
    #       pygame.display.get_surface().blit(pause_surface_7, (0, 0))
    #
    #     elif self.page == 8:
    #       self.status = Status.MENU
    #
    #
    #     if keys[pygame.K_RETURN] and self.page == 1 :
    #         self.page = 2
    #         time.sleep(0.2)
    #     elif keys[pygame.K_RETURN] and self.page == 2 :
    #         self.page = 3
    #         time.sleep(0.2)
    #     elif keys[pygame.K_RETURN] and self.page == 3 :
    #         self.page = 4
    #         time.sleep(0.2)
    #     elif keys[pygame.K_RETURN] and self.page == 4 :
    #         self.page = 5
    #         time.sleep(0.2)
    #     elif keys[pygame.K_RETURN] and self.page == 5 :
    #         self.page = 6
    #         time.sleep(0.2)
    #     elif keys[pygame.K_RETURN] and self.page == 6 :
    #         self.page = 7
    #         time.sleep(0.2)
    #     elif keys[pygame.K_RETURN] and self.page == 7 :
    #         self.page = 8
    #         time.sleep(0.2)
    #
    #
    #
    # def exit_menu(self):
    #     pass

