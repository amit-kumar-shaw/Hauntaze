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
        self.start_surf = self.plain_text('Insert Coin to start', 16)
        self.start_rect = self.start_surf.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 20))

        self.sound = GameSound()
        self.sound.menu.play(loops=-1)

        self.story_frames = self.create_frames('Story Mode >')
        self.survival_frames = self.create_frames('< Survival Mode')
        self.single_frames = self.create_frames('Single Player >')
        self.multi_frames = self.create_frames('< Multiplayer')
        self.vertical_transition = False
        self.horizontal_transition = False
        self.player_selected = True
        self.story = True
        self.horizontal_index = 5
        self.vertical_index = 5

        size = 16
        self.info_msg = []
        self.info_msg.append(self.text('Lift the curse of the forbidden treasure', size))
        self.info_msg.append(self.text('Play together to lift the curse of the forbidden treasure', size))
        self.info_msg.append(self.text('How many levels can you survive?', size))
        self.info_msg.append(self.text('Compete against each other', size))

    def check_input(self):
        keys = pygame.key.get_pressed()

        # insert coin for player 1
        if keys[pygame.K_1] and not self.is_player1_ready:
            self.is_player1_ready = True
            self.sound.play_confirmation()

        # insert coin for player 2
        if keys[pygame.K_2] and not self.is_player2_ready:
            self.is_player2_ready = True
            self.sound.play_confirmation()

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

    def update(self):



        self.screen.blit(self.background, (0, 0))

        # self.check_input()
        # # title animation
        # self.animation_index += 0.08  # * self.animation_direction
        # if self.animation_index >= 2: self.animation_index = 0
        #
        # self.screen.blit(self.player1_surf, self.player1_rect)
        #
        # self.screen.blit(self.player2_surf, self.player2_rect)
        #
        # # player 1 insert coin
        # frame = self.coin_frames[int(self.animation_index)] if not self.is_player1_ready else self.coin_frames[2]
        # frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 200))
        # self.screen.blit(frame, frame_rect)
        #
        # # player 2 insert coin
        # frame = self.coin_frames[int(self.animation_index)] if not self.is_player2_ready else self.coin_frames[2]
        # frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 200))
        # self.screen.blit(frame, frame_rect)
        #
        # if self.is_player1_ready or self.is_player2_ready:
        #     self.screen.blit(self.start_surf, self.start_rect)
        #
        # self.game_mode()

        self.update_menu()
        self.screen.blit(self.start_surf, self.start_rect)

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

        width = 300
        text_surf = pygame.Surface((width, 50), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))

        font = pygame.font.Font('./assets/fonts/1.ttf', size)
        text = font.render(text_msg, False, 'black')
        text_rect = text.get_rect(center=(width / 2, 25))
        text_surf.blit(text, text_rect)
        text = font.render(text_msg, False, 'white')
        text_rect = text.get_rect(center=((width / 2) - 1, 25 - 1))
        text_surf.blit(text, text_rect)

        return text_surf

    def coin_text(self):
        frames = []

        for i in range(3):
            text_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 0))
            msg = 'Select Player' if i < 2 else 'Ready'
            font = pygame.font.Font('./assets/fonts/1.ttf', 15 + i)
            text = font.render(msg, False, 'orange')
            text_rect = text.get_rect(center=(100, 25))
            text_surf.blit(text, text_rect)
            text = font.render(msg, False, 'yellow')
            text_rect = text.get_rect(center=(100 - 1, 25 - 1))
            text_surf.blit(text, text_rect)

            frames.append(text_surf)

        return frames

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if not self.horizontal_transition and self.player_selected:
                self.sound.play_mode_select()
                self.player_selected = False
                self.vertical_transition = True
                self.vertical_index = -1

        if keys[pygame.K_UP]:
            if not self.horizontal_transition and not self.player_selected:
                self.sound.play_mode_select()
                self.player_selected = True
                self.vertical_transition = True
                self.vertical_index = -1

        if keys[pygame.K_LEFT]:
            if not self.vertical_transition:
                if self.player_selected and self.multiplayer:
                    self.sound.play_mode_select()
                    self.multiplayer = False
                    self.horizontal_transition = True
                    self.horizontal_index = -1
                elif not self.player_selected and not self.story:
                    self.sound.play_mode_select()
                    self.story = True
                    self.horizontal_transition = True
                    self.horizontal_index = -1

        if keys[pygame.K_RIGHT]:
            if not self.vertical_transition:
                if self.player_selected and not self.multiplayer:
                    self.sound.play_mode_select()
                    self.multiplayer = True
                    self.horizontal_transition = True
                    self.horizontal_index = -1
                elif not self.player_selected and self.story:
                    self.sound.play_mode_select()
                    self.story = False
                    self.horizontal_transition = True
                    self.horizontal_index = -1

    def update_menu(self):

        self.is_player1_ready = True
        self.is_story_mode = self.story

        self.input()
        if self.vertical_transition:
            self.vertical_index += 1
            if self.vertical_index == 5:
                self.vertical_transition = False

        if self.horizontal_transition:
            self.horizontal_index += 1
            if self.horizontal_index == 5:
                self.horizontal_transition = False

        h_alt_index = 5 - self.horizontal_index
        v_alt_index = 5 - self.vertical_index

        player_frame = self.multi_frames if self.multiplayer else self.single_frames

        # if self.player_selected:
        index = self.vertical_index if self.player_selected else v_alt_index
        frame = player_frame[index]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 120))
        self.screen.blit(frame, frame_rect)

        mode_frame = self.story_frames if self.story else self.survival_frames
        # Mode Option
        index = v_alt_index if self.player_selected else self.vertical_index
        frame = mode_frame[index]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 90))
        self.screen.blit(frame, frame_rect)

        info = 0
        if self.multiplayer:
            self.is_player2_ready = True
            if self.story:
                info = 1
            else:
                info = 3
        else:
            self.is_player2_ready = False
            if self.story:
                info = 0
            else:
                info = 2
        frame = self.info_msg[info]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 70))
        self.screen.blit(frame, frame_rect)

    def create_frames(self, text_msg):
        frames = []
        selected_color = ['red', 'white']
        deselected_color = ['black', 'grey']

        for i in range(6):
            text_surf = pygame.Surface((300, 50), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 0))
            font = pygame.font.Font('./assets/fonts/1.ttf', 17 + i)
            color = selected_color if i > 0 else deselected_color

            text = font.render(text_msg, False, color[0])
            rect = text.get_rect(center=(150, 25))
            text_surf.blit(text, rect)
            text = font.render(text_msg, False, color[1])
            rect = text.get_rect(center=(150 - 1, 25 - 2))
            text_surf.blit(text, rect)
            frames.append(text_surf)

        return frames

    def text(self, text_msg, size):

        width = 500
        text_surf = pygame.Surface((width, 50), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))

        font = pygame.font.Font('./assets/fonts/4.ttf', size)
        text = font.render(text_msg, False, 'black')
        text_rect = text.get_rect(center=(width / 2, 25))
        text_surf.blit(text, text_rect)
        text = font.render(text_msg, False, 'white')
        text_rect = text.get_rect(center=((width / 2) - 1, 25 - 1))
        text_surf.blit(text, text_rect)

        return text_surf