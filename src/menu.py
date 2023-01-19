import random

import pygame
from settings import *
from sounds import MenuSound
from utilities import import_frames


class Menu():
    def __init__(self, joystick =None):
        self.screen = pygame.display.get_surface()
        self.joystick = joystick
        self.is_story_mode = True
        self.multiplayer = False
        self.is_player1_ready = True
        self.is_player2_ready = False
        self.coin_inserted = False
        self.animation_index = 0
        self.animation_direction = 1
        self.mode_transition = False
        self.transition_index = 10

        self.background = pygame.image.load(f'./assets/images/background/castle.png').convert()
        self.title_frames = import_frames('./assets/images/background/title', 1)
        self.p1_frames = import_frames('./assets/images/menu/p1', 1)
        self.p2_frames = import_frames('./assets/images/menu/p2', 1)
        self.mode_identifier = import_frames('./assets/images/menu/mode', 1)
        self.player1_surf = self.plain_text('Player 1', 20)
        self.player1_rect = self.player1_surf.get_rect(center=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 220))
        self.player2_surf = self.plain_text('Player 2', 20)
        self.player2_rect = self.player2_surf.get_rect(center=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 220))
        self.mode1_frames = self.mode_frames('Story Mode')
        self.mode2_frames = self.mode_frames('Survival Mode')
        self.coin_frames = self.coin_text()
        self.start_surf = self.plain_text('Insert Coin to start', 16)
        self.start_rect = self.start_surf.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 20))

        self.sound = MenuSound()
        # self.sound.menu.play(loops=-1)

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

        size = 10
        self.info_msg = []
        self.info_msg.append(self.text('Lift the curse of the forbidden treasure!', size))
        self.info_msg.append(self.text('Lift the curse of the forbidden treasure together!', size))
        self.info_msg.append(self.text('How many levels can you survive?', size))
        self.info_msg.append(self.text('The last survivor wins the game!', size))

        self.credits_button = pygame.image.load(f'./assets/images/menu/credits.png').convert_alpha()

        self.credits_frames = import_frames('./assets/images/menu/credits', 1)
        self.credits_transition_index = 0
        self.credits_active = False
        self.credits_transition = 0

        # pygame.image.save(self.text('Credits', 16), './assets/images/menu/credits1.png')
        # pygame.image.save(self.text('Back', 16), './assets/images/menu/credits2.png')
        # pygame.image.save(self.text('Skip', 16), './assets/images/menu/skip.png')
        # pygame.image.save(self.text('Skip Animation', 16), './assets/images/menu/skip2.png')
        # pygame.image.save(self.text('Continue', 16), './assets/images/transitions/continue1.png')
        # pygame.image.save(self.credits_text('Hauntaze is developed for FabArcade as part of the', 12), './assets/images/menu/1.png')
        # pygame.image.save(
        #     self.credits_text('Media Computing Project at RWTH Aachen University.', 12),
        #     './assets/images/menu/2.png')
        # pygame.image.save(self.credits_text('Students :', 12), './assets/images/menu/3.png')
        # pygame.image.save(self.credits_text('Amit Kumar Shaw', 12), './assets/images/menu/4.png')
        # pygame.image.save(self.credits_text('Hongtao Ye', 12), './assets/images/menu/5.png')
        # pygame.image.save(self.credits_text('Mona Amirsoleimani', 12), './assets/images/menu/6.png')
        # pygame.image.save(self.credits_text('Instructors :', 12), './assets/images/menu/7.png')
        # pygame.image.save(self.credits_text('Prof. Dr. Jan Borchers', 12), './assets/images/menu/8.png')
        # pygame.image.save(self.credits_text('Adrian Wagner', 12), './assets/images/menu/9.png')
        # pygame.image.save(self.credits_text('Anke Brocker', 12), './assets/images/menu/10.png')

    def check_input(self):
        keys = pygame.key.get_pressed()

        # insert coin for player 1
        if keys[pygame.K_1] and not self.is_player1_ready:
            self.is_player1_ready = True
            self.sound.confirm.play()

        # insert coin for player 2
        if keys[pygame.K_2] and not self.is_player2_ready:
            self.is_player2_ready = True
            self.sound.confirm.play()

        # toggle game modes
        if keys[pygame.K_DOWN] and self.is_story_mode:
            self.is_story_mode = False
            self.mode_transition = True
            self.transition_index = -1
            self.sound.confirm.play()

        if keys[pygame.K_UP] and not self.is_story_mode:
            self.is_story_mode = True
            self.mode_transition = True
            self.transition_index = -1
            self.sound.confirm.play()

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
        # title animation
        self.animation_index += 0.08  # * self.animation_direction
        if self.animation_index >= 2: self.animation_index = 0

        rect = self.title_frames[int(self.animation_index)].get_rect(center=(SCREEN_WIDTH/2, 70))

        self.screen.blit(self.title_frames[int(self.animation_index)], rect)

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
        if self.credits_active or self.credits_transition !=0:
            self.show_credits()
        else:
            self.update_menu()
        # self.screen.blit(self.start_surf, self.start_rect)

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
            msg = 'Insert Coin' if i < 2 else 'Ready to play'
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

        if (keys[COIN_KEYBOARD] or (self.joystick is not None and self.joystick.get_button(COIN_BUTTON))) and not self.coin_inserted:
            self.coin_inserted = True
            self.sound.insert_coin.play()

        if keys[pygame.K_DOWN] or (self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) > AXIS_THRESHOLD):
            if not self.horizontal_transition and self.player_selected:
                self.sound.select.play()
                self.player_selected = False
                self.vertical_transition = True
                self.vertical_index = -1

        if keys[pygame.K_UP] or (self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) < -AXIS_THRESHOLD):
            if not self.horizontal_transition and not self.player_selected:
                self.sound.select.play()
                self.player_selected = True
                self.vertical_transition = True
                self.vertical_index = -1

        if keys[pygame.K_LEFT] or (self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) < -AXIS_THRESHOLD):
            if not self.vertical_transition:
                if self.player_selected and self.multiplayer:
                    self.sound.select.play()
                    self.multiplayer = False
                    self.horizontal_transition = True
                    self.horizontal_index = -1
                elif not self.player_selected and not self.story:
                    self.sound.select.play()
                    self.story = True
                    self.horizontal_transition = True
                    self.horizontal_index = -1

        if keys[pygame.K_RIGHT] or (self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) > AXIS_THRESHOLD):
            if not self.vertical_transition:
                if self.player_selected and not self.multiplayer:
                    self.sound.select.play()
                    self.multiplayer = True
                    self.horizontal_transition = True
                    self.horizontal_index = -1
                elif not self.player_selected and self.story:
                    self.sound.select.play()
                    self.story = False
                    self.horizontal_transition = True
                    self.horizontal_index = -1

        if (keys[PLAYER1_DEATH] or (self.joystick is not None and self.joystick.get_button(YELLOW_BUTTON))) and not self.credits_active:
            self.credits_active = True
            self.credits_transition = 1



    def update_menu(self):

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
        frame_rect = frame.get_rect(midleft=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - 120))
        self.screen.blit(frame, frame_rect)

        mode_frame = self.story_frames if self.story else self.survival_frames
        # Mode Option
        index = v_alt_index if self.player_selected else self.vertical_index
        frame = mode_frame[index]
        frame_rect = frame.get_rect(midleft=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - 90))
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

        # frame = self.info_msg[info]
        # frame_rect = frame.get_rect(midleft=(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT - 82))
        # self.screen.blit(frame, frame_rect)




        frame_rect = self.credits_button.get_rect(midleft=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - 60))
        self.screen.blit(self.credits_button, frame_rect)

        frame = self.coin_frames[int(self.animation_index)] if not self.coin_inserted else self.coin_frames[2]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT - 60))
        self.screen.blit(frame, frame_rect)

        if self.multiplayer:
            frame = self.p1_frames[int(self.animation_index)]
            frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT - 120))
            self.screen.blit(frame, frame_rect)

            frame = self.p2_frames[int(self.animation_index)]
            frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT - 120))
            self.screen.blit(frame, frame_rect)

            frame = self.mode_identifier[0] if self.story else self.mode_identifier[1]
            frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT - 110))
            self.screen.blit(frame, frame_rect)
        else:
            frame = self.p1_frames[int(self.animation_index)]
            frame = pygame.transform.flip(frame, True, False)
            frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT - 120))
            self.screen.blit(frame, frame_rect)

    def show_credits(self):
        keys = pygame.key.get_pressed()
        if (keys[PAUSE] or (self.joystick is not None and self.joystick.get_button(RED_BUTTON))) and self.credits_active:
            self.credits_active = False
            self.credits_transition = -1

        if self.credits_transition_index >= len(self.credits_frames):
            self.credits_transition = 0
            self.credits_transition_index = len(self.credits_frames) -1
        elif self.credits_transition_index < 0:
            self.credits_transition = 0
            self.credits_transition_index = 0

        frame = self.credits_frames[int(self.credits_transition_index)]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 130))
        self.screen.blit(frame, frame_rect)

        self.credits_transition_index += self.credits_transition



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
            rect = text.get_rect(midleft=(1, 25))
            text_surf.blit(text, rect)
            text = font.render(text_msg, False, color[1])
            rect = text.get_rect(midleft=(1 - 1, 25 - 2))
            text_surf.blit(text, rect)
            frames.append(text_surf)

        return frames

    def text(self, text_msg, size):

        width = 500
        text_surf = pygame.Surface((width, 50), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))

        font = pygame.font.Font('./assets/fonts/1.ttf', size)
        text = font.render(text_msg, False, 'red')
        # text_rect = text.get_rect(midleft=(width / 2, 25))
        text_rect = text.get_rect(midleft=(1, 25))
        text_surf.blit(text, text_rect)
        text = font.render(text_msg, False, 'white')
        # text_rect = text.get_rect(midleft=((width / 2) - 1, 25 - 1))
        text_rect = text.get_rect(midleft=(1 - 1, 25 - 1))
        text_surf.blit(text, text_rect)

        return text_surf

    def credits_text(self, text_msg, size):

        width = 448
        text_surf = pygame.Surface((width, 16), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))

        font = pygame.font.Font('./assets/fonts/1.ttf', size)
        text = font.render(text_msg, False, 'black')
        text_rect = text.get_rect(midleft=(1, 8))
        text_surf.blit(text, text_rect)

        text = font.render(text_msg, False, 'white')
        text_rect = text.get_rect(midleft=(1 - 1, 8 - 1))
        text_surf.blit(text, text_rect)

        return text_surf