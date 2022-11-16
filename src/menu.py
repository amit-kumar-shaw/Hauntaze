import random

import pygame
from settings import *

class Menu():
    def __init__(self, ):
        self.screen = pygame.display.get_surface()
        self.is_story_mode = True
        self.multiplayer = False
        self.is_player1_ready = False
        self.is_player2_ready = False
        self.animation_index = 0
        self.animation_direction = 1
        self.mode_transition = False
        self.transition_index = 5

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1] and not self.is_player1_ready:
            self.is_player1_ready = True

        if keys[pygame.K_2] and not self.is_player2_ready:
            self.is_player2_ready = True

        if keys[pygame.K_DOWN] and self.is_story_mode:
            self.is_story_mode = False
            self.mode_transition = True
            self.transition_index = -5

        if keys[pygame.K_UP] and not self.is_story_mode:
            self.is_story_mode = True
            self.mode_transition = True
            self.transition_index = -5

    def game_mode(self):

        if self.mode_transition:
            self.transition_index += 1
            if self.transition_index == 5: self.mode_transition = False

        # set font and color
        selected_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 20 + self.transition_index)
        deselected_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 20 - self.transition_index)
        selected_color = ['red', 'white']
        deselected_color = ['black', 'grey']

        # Story Mode
        font = selected_font if self.is_story_mode else deselected_font
        color = selected_color if self.is_story_mode else deselected_color
        text = font.render('Story Mode', False, color[0])
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 100))
        self.screen.blit(text, text_rect)
        text = font.render('Story Mode', False, color[1])
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5 - 1, SCREEN_HEIGHT - 100 - 2))
        self.screen.blit(text, text_rect)

        # Unlimited Mode
        font = deselected_font if self.is_story_mode else selected_font
        color = deselected_color if self.is_story_mode else selected_color
        text = font.render('Unlimited Mode', False, color[0])
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 70))
        self.screen.blit(text, text_rect)
        text = font.render('Unlimited Mode', False, color[1])
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5 - 1, SCREEN_HEIGHT - 70 - 2))
        self.screen.blit(text, text_rect)

    def update(self):

        self.check_input()

        # set background image
        background = pygame.image.load(f'./assets/images/background/6.png').convert()
        # background = pygame.transform.rotozoom(background, 0, 1/3)
        self.screen.blit(background, (0, 0))

        # player1 = pygame.image.load('./assets/images/player/p1_01.png').convert_alpha()
        # player1 = pygame.transform.rotozoom(player1, 0, 2)
        # player1_rect = player1.get_rect(center=((SCREEN_WIDTH//2)-100, SCREEN_HEIGHT//2))
        # player2 = pygame.image.load('./assets/images/player/p2_01.png').convert_alpha()
        # player2 = pygame.transform.rotozoom(player2, 0, 5)
        # player2_rect = player2.get_rect(center=((SCREEN_WIDTH // 2) + 100, SCREEN_HEIGHT // 2))

        # title animation
        self.animation_index += 0.08# * self.animation_direction
        if self.animation_index >= 2: self.animation_index = 0
        # if self.animation_index > 12: self.animation_direction = -1
        # if self.animation_index <= 0: self.animation_direction = 1


        # title
        title_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 50)#+int(self.animation_index))
        title = title_font.render('HAUNTAZE', False, 'red')
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2 + 1, 50 + 2))
        self.screen.blit(title, title_rect)

        title = title_font.render('HAUNTAZE', False, 'white')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # player 1
        font = pygame.font.Font('./assets/fonts/1.ttf', 20)
        text = font.render('Player 1', False, 'black')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 220))
        self.screen.blit(text,text_rect)
        text = font.render('Player 1', False, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25 - 1, SCREEN_HEIGHT - 220 - 1))
        self.screen.blit(text, text_rect)

        # player 2
        text = font.render('Player 2', False, 'black')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 220))
        self.screen.blit(text, text_rect)
        text = font.render('Player 2', False, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75 - 1, SCREEN_HEIGHT - 220 - 1))
        self.screen.blit(text, text_rect)

        # player 1 insert coin
        msg = 'Ready' if self.is_player1_ready else 'Insert Coin'
        font = pygame.font.Font('./assets/fonts/1.ttf', 15 +
                                int(self.animation_index if not self.is_player1_ready else 0))
                                #(1 if int(self.animation_index) % 6 == 0 and not self.is_player1_ready else 0))
        text = font.render(msg, False, 'orange')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 200))
        self.screen.blit(text, text_rect)
        text = font.render(msg, False, 'yellow')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25 - 1, SCREEN_HEIGHT - 200 - 1))
        self.screen.blit(text, text_rect)

        # player 2 insert coin
        msg = 'Ready' if self.is_player2_ready else 'Insert Coin'
        font = pygame.font.Font('./assets/fonts/1.ttf', 15 +
                                int(self.animation_index if not self.is_player2_ready else 0))
                                #(1 if int(self.animation_index) % 6 == 0 and not self.is_player2_ready else 0))
        text = font.render(msg, False, 'orange')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 200))
        self.screen.blit(text, text_rect)
        text = font.render(msg, False, 'yellow')
        text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75 - 1, SCREEN_HEIGHT - 200 - 1))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font('./assets/fonts/1.ttf', 15)
        start_msg = font.render('Press ENTER to start', False, 'white')
        msg_rect = start_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT-20))
        # self.screen.blit(background, (0, 0))
        # self.screen.blit(title, title_rect)
        # self.screen.blit(player1, player1_rect)
        # self.screen.blit(player2, player2_rect)
        if self.is_player1_ready or self.is_player2_ready:
            self.screen.blit(start_msg, msg_rect)

        self.game_mode()
        # title_font = pygame.font.Font('./assets/fonts/PixelDevilsdeal.ttf', 50)
        # title = title_font.render('HAUNTAZE', False, TITLE_COLOR)
        # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        # self.screen.blit(title, title_rect)
        #
        # title_font = pygame.font.Font('./assets/fonts/PixelRunes.ttf', 50)
        # title = title_font.render('HAUNTAZE', False, TITLE_COLOR)
        # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 280))
        # self.screen.blit(title, title_rect)