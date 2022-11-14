import random

import pygame
from settings import *

class Menu():
    def __init__(self, ):
        self.screen = pygame.display.get_surface()
        self.isStoryMode = False
        self.multiplayer = False

    def update(self):

        # set background image
        background = pygame.image.load(f'./assets/images/background/4.png').convert()
        background = pygame.transform.rotozoom(background, 0, 1/3)
        self.screen.blit(background, (0, 0))

        # player1 = pygame.image.load('./assets/images/player/p1_01.png').convert_alpha()
        # player1 = pygame.transform.rotozoom(player1, 0, 2)
        # player1_rect = player1.get_rect(center=((SCREEN_WIDTH//2)-100, SCREEN_HEIGHT//2))
        # player2 = pygame.image.load('./assets/images/player/p2_01.png').convert_alpha()
        # player2 = pygame.transform.rotozoom(player2, 0, 5)
        # player2_rect = player2.get_rect(center=((SCREEN_WIDTH // 2) + 100, SCREEN_HEIGHT // 2))

        title_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 50)
        title = title_font.render('HAUNTAZE', False, 'red')
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2 + 1, 50 + 2))
        self.screen.blit(title, title_rect)

        title = title_font.render('HAUNTAZE', False, 'white')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 20)
        start_msg = font.render('Press ENTER to start', False, 'white')
        msg_rect = start_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT-20))
        # self.screen.blit(background, (0, 0))
        # self.screen.blit(title, title_rect)
        # self.screen.blit(player1, player1_rect)
        # self.screen.blit(player2, player2_rect)
        self.screen.blit(start_msg, msg_rect)

        # title_font = pygame.font.Font('./assets/fonts/PixelDevilsdeal.ttf', 50)
        # title = title_font.render('HAUNTAZE', False, TITLE_COLOR)
        # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        # self.screen.blit(title, title_rect)
        #
        # title_font = pygame.font.Font('./assets/fonts/PixelRunes.ttf', 50)
        # title = title_font.render('HAUNTAZE', False, TITLE_COLOR)
        # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 280))
        # self.screen.blit(title, title_rect)