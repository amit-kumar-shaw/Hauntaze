import random

import pygame
from settings import *
from music import GameSound

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
        self.transition_index = 10

        self.background = pygame.image.load(f'./assets/images/background/8.png').convert()
        self.player1_surf = self.plain_text('Player 1', 20)
        self.player1_rect = self.player1_surf.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 220))
        self.player2_surf = self.plain_text('Player 2', 20)
        self.player2_rect = self.player2_surf.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 220))
        self.mode1_frames = self.mode_frames('Story Mode')
        self.mode2_frames = self.mode_frames('Survival Mode')
        self.coin_frames = self.coin_text()
        self.start_surf = self.plain_text('Press ENTER to start', 15)
        self.start_rect = self.start_surf.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 20))

        self.sound = GameSound()
        self.sound.menu.play(loops=-1)

    def check_input(self):
        keys = pygame.key.get_pressed()

        # insert coin for player 1
        if keys[pygame.K_1] and not self.is_player1_ready:
            self.is_player1_ready = True
            self.sound.play_insert_coin()

        # insert coin for player 2
        if keys[pygame.K_2] and not self.is_player2_ready:
            self.is_player2_ready = True
            self.sound.play_insert_coin()

        # toggle game modes
        if keys[pygame.K_DOWN] and self.is_story_mode:
            self.is_story_mode = False
            self.mode_transition = True
            self.transition_index = -1
            self.sound.play_mode_select()

        if keys[pygame.K_UP] and not self.is_story_mode:
            self.is_story_mode = True
            self.mode_transition = True
            self.transition_index = -1
            self.sound.play_mode_select()

    def game_mode(self):

        if self.mode_transition:
            self.transition_index += 1
            if self.transition_index == 10: self.mode_transition = False

        alt_index = 10 - self.transition_index

        # Mode 1
        index = self.transition_index if self.is_story_mode else alt_index
        frame = self.mode1_frames[index]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 100))
        self.screen.blit(frame, frame_rect)

        # Mode 2
        index = alt_index if self.is_story_mode else self.transition_index
        frame = self.mode2_frames[index]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 70))
        self.screen.blit(frame, frame_rect)

        # # set font and color
        # selected_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 20 + self.transition_index)
        # deselected_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 20 - self.transition_index)
        # selected_color = ['red', 'white']
        # deselected_color = ['black', 'grey']
        #
        #
        #
        # text_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
        # text_surf.fill((0,0,0,0))
        # text_rect = text_surf.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 100))
        # # Story Mode
        # font = selected_font if self.is_story_mode else deselected_font
        # color = selected_color if self.is_story_mode else deselected_color
        # text = font.render('Story Mode', False, color[0])
        # # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 100))
        # # self.screen.blit(text, text_rect)
        # rect = text.get_rect(center=(100, 25))
        # text_surf.blit(text, rect)
        # text = font.render('Story Mode', False, color[1])
        # # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5 - 1, SCREEN_HEIGHT - 100 - 2))
        # # self.screen.blit(text, text_rect)
        # rect = text.get_rect(center=(100-1, 25-2))
        # text_surf.blit(text, rect)
        # self.screen.blit(text_surf, text_rect)
        # # Survival Mode
        # font = deselected_font if self.is_story_mode else selected_font
        # color = deselected_color if self.is_story_mode else selected_color
        # text = font.render('Survival Mode', False, color[0])
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 70))
        # self.screen.blit(text, text_rect)
        # text = font.render('Survival Mode', False, color[1])
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5 - 1, SCREEN_HEIGHT - 70 - 2))
        # self.screen.blit(text, text_rect)

    def update(self):

        self.check_input()

        # set background image
        # background = pygame.image.load(f'./assets/images/background/8.png').convert()
        # background = pygame.transform.rotozoom(background, 0, 1/3)
        self.screen.blit(self.background, (0, 0))

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
        # title_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 50)#+int(self.animation_index))
        # title = title_font.render('HAUNTAZE', False, 'red')
        # title_rect = title.get_rect(center=(SCREEN_WIDTH//2 + 1, 50 + 2))
        # self.screen.blit(title, title_rect)
        #
        # title = title_font.render('HAUNTAZE', False, 'white')
        # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        # self.screen.blit(title, title_rect)

        # player 1
        # font = pygame.font.Font('./assets/fonts/1.ttf', 20)
        # text = font.render('Player 1', False, 'black')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 220))
        # self.screen.blit(text,text_rect)
        # text = font.render('Player 1', False, 'white')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25 - 1, SCREEN_HEIGHT - 220 - 1))
        # self.screen.blit(text, text_rect)
        self.screen.blit(self.player1_surf, self.player1_rect)

        # player 2
        # text = font.render('Player 2', False, 'black')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 220))
        # self.screen.blit(text, text_rect)
        # text = font.render('Player 2', False, 'white')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75 - 1, SCREEN_HEIGHT - 220 - 1))
        # self.screen.blit(text, text_rect)
        self.screen.blit(self.player2_surf, self.player2_rect)

        # player 1 insert coin
        frame = self.coin_frames[int(self.animation_index)] if not self.is_player1_ready else self.coin_frames[2]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 200))
        self.screen.blit(frame, frame_rect)

        # msg = 'Ready' if self.is_player1_ready else 'Insert Coin'
        # font = pygame.font.Font('./assets/fonts/1.ttf', 15 +
        #                         int(self.animation_index if not self.is_player1_ready else 0))
        #                         #(1 if int(self.animation_index) % 6 == 0 and not self.is_player1_ready else 0))
        # text = font.render(msg, False, 'orange')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 200))
        # self.screen.blit(text, text_rect)
        # text = font.render(msg, False, 'yellow')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.25 - 1, SCREEN_HEIGHT - 200 - 1))
        # self.screen.blit(text, text_rect)

        # player 2 insert coin
        frame = self.coin_frames[int(self.animation_index)] if not self.is_player2_ready else self.coin_frames[2]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 200))
        self.screen.blit(frame, frame_rect)

        # msg = 'Ready' if self.is_player2_ready else 'Insert Coin'
        # font = pygame.font.Font('./assets/fonts/1.ttf', 15 +
        #                         int(self.animation_index if not self.is_player2_ready else 0))
        #                         #(1 if int(self.animation_index) % 6 == 0 and not self.is_player2_ready else 0))
        # text = font.render(msg, False, 'orange')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 200))
        # self.screen.blit(text, text_rect)
        # text = font.render(msg, False, 'yellow')
        # text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.75 - 1, SCREEN_HEIGHT - 200 - 1))
        # self.screen.blit(text, text_rect)

        # font = pygame.font.Font('./assets/fonts/1.ttf', 15)
        # start_msg = font.render('Press ENTER to start', False, 'white')
        # msg_rect = start_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT-20))
        # self.screen.blit(background, (0, 0))
        # self.screen.blit(title, title_rect)
        # self.screen.blit(player1, player1_rect)
        # self.screen.blit(player2, player2_rect)
        if self.is_player1_ready or self.is_player2_ready:
            # self.screen.blit(start_msg, msg_rect)
            self.screen.blit(self.start_surf, self.start_rect)

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

    def mode_frames(self, text_msg):
        frames = []
        selected_color = ['red', 'white']
        deselected_color = ['black', 'grey']

        for i in range(11):
            text_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 0))
            font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 15 + i)
            color = selected_color if i > 5 else deselected_color

            text = font.render(text_msg, False, color[0])
            rect = text.get_rect(center=(100, 25))
            text_surf.blit(text, rect)
            text = font.render(text_msg, False, color[1])
            rect = text.get_rect(center=(100 - 1, 25 - 2))
            text_surf.blit(text, rect)
            frames.append(text_surf)

        return frames

    def plain_text(self, text_msg, size):
        text_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))

        font = pygame.font.Font('./assets/fonts/1.ttf', size)
        text = font.render(text_msg, False, 'black')
        text_rect = text.get_rect(center=(100, 25))
        text_surf.blit(text, text_rect)
        text = font.render(text_msg, False, 'white')
        text_rect = text.get_rect(center=(100 - 1, 25 - 1))
        text_surf.blit(text, text_rect)

        return text_surf

    def coin_text(self):
        frames = []

        for i in range(3):
            text_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 0))
            msg = 'Insert Coin' if i < 2 else 'Ready'
            font = pygame.font.Font('./assets/fonts/1.ttf', 15 + i)
            text = font.render(msg, False, 'orange')
            text_rect = text.get_rect(center=(100, 25))
            text_surf.blit(text, text_rect)
            text = font.render(msg, False, 'yellow')
            text_rect = text.get_rect(center=(100 - 1, 25 - 1))
            text_surf.blit(text, text_rect)

            frames.append(text_surf)

        return frames