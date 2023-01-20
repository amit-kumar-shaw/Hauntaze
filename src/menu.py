import pygame
from settings import *
from sounds import MenuSound
from utilities import import_frames


class Menu:
    """ Menu screen for the game """

    def __init__(self, joystick=None):
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
        self.coin_frames = import_frames("./assets/images/menu/coin_text", 1)

        self.sound = MenuSound()

        self.story_frames = import_frames("./assets/images/menu/story_frames", 1)
        self.survival_frames = import_frames("./assets/images/menu/survival_frames/", 1)
        self.single_frames = import_frames("./assets/images/menu/single_frames/", 1)
        self.multi_frames = import_frames("./assets/images/menu/multi_frames/", 1)

        self.vertical_transition = False
        self.horizontal_transition = False
        self.player_selected = True
        self.story = True
        self.horizontal_index = 5
        self.vertical_index = 5

        self.credits_button = pygame.image.load(f'./assets/images/menu/credits.png').convert_alpha()

        self.credits_frames = import_frames('./assets/images/menu/credits', 1)
        self.credits_transition_index = 0
        self.credits_active = False
        self.credits_transition = 0

    def update(self):
        """ update the menu every frame """

        # display background image
        self.screen.blit(self.background, (0, 0))

        # title animation
        self.animation_index += 0.08
        if self.animation_index >= 2:
            self.animation_index = 0

        rect = self.title_frames[int(self.animation_index)].get_rect(center=(SCREEN_WIDTH / 2, 70))

        self.screen.blit(self.title_frames[int(self.animation_index)], rect)

        # display credits or menu screen
        if self.credits_active or self.credits_transition != 0:
            self.show_credits()
        else:
            self.update_menu()

    def input(self):
        """ check keyboard and joystick inputs of player 1"""

        keys = pygame.key.get_pressed()

        if (keys[COIN_KEYBOARD] or (
                self.joystick is not None and self.joystick.get_button(COIN_BUTTON))) and not self.coin_inserted:
            self.coin_inserted = True
            self.sound.insert_coin.play()

        if keys[PLAYER1_MOVE_DOWN] or (self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) > AXIS_THRESHOLD):
            if not self.horizontal_transition and self.player_selected:
                self.sound.select.play()
                self.player_selected = False
                self.vertical_transition = True
                self.vertical_index = -1

        if keys[PLAYER1_MOVE_UP] or (self.joystick is not None and self.joystick.get_axis(UP_DOWN_AXIS) < -AXIS_THRESHOLD):
            if not self.horizontal_transition and not self.player_selected:
                self.sound.select.play()
                self.player_selected = True
                self.vertical_transition = True
                self.vertical_index = -1

        if keys[PLAYER1_MOVE_LEFT] or (
                self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) < -AXIS_THRESHOLD):
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

        if keys[PLAYER1_MOVE_RIGHT] or (
                self.joystick is not None and self.joystick.get_axis(LEFT_RIGHT_AXIS) > AXIS_THRESHOLD):
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

        if (keys[PLAYER1_DEATH] or (
                self.joystick is not None and self.joystick.get_button(YELLOW_BUTTON))) and not self.credits_active:
            self.credits_active = True
            self.credits_transition = 1

    def update_menu(self):
        """ update menu screen """

        self.is_story_mode = self.story

        # check inputs
        self.input()

        if self.vertical_transition:
            self.vertical_index += 1
            if self.vertical_index == 5:
                self.vertical_transition = False

        if self.horizontal_transition:
            self.horizontal_index += 1
            if self.horizontal_index == 5:
                self.horizontal_transition = False

        v_alt_index = 5 - self.vertical_index

        # Single player or Multiplayer option
        player_frame = self.multi_frames if self.multiplayer else self.single_frames

        index = self.vertical_index if self.player_selected else v_alt_index
        frame = player_frame[index]
        frame_rect = frame.get_rect(midleft=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - 120))
        self.screen.blit(frame, frame_rect)

        # Story mode or survival mode option
        mode_frame = self.story_frames if self.story else self.survival_frames

        index = v_alt_index if self.player_selected else self.vertical_index
        frame = mode_frame[index]
        frame_rect = frame.get_rect(midleft=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - 90))
        self.screen.blit(frame, frame_rect)

        if self.multiplayer:
            self.is_player2_ready = True
        else:
            self.is_player2_ready = False

        # credits button
        frame_rect = self.credits_button.get_rect(midleft=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - 60))
        self.screen.blit(self.credits_button, frame_rect)

        # insert coin info
        frame = self.coin_frames[int(self.animation_index)] if not self.coin_inserted else self.coin_frames[2]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT - 60))
        self.screen.blit(frame, frame_rect)

        # show players and handshake or boxing icon based on menu selection
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
        """ display credits screen """

        keys = pygame.key.get_pressed()
        # check back button
        if (keys[PAUSE] or (
                self.joystick is not None and self.joystick.get_button(RED_BUTTON))) and self.credits_active:
            self.credits_active = False
            self.credits_transition = -1

        # animate credits on/off transition
        if self.credits_transition_index >= len(self.credits_frames):
            self.credits_transition = 0
            self.credits_transition_index = len(self.credits_frames) - 1
        elif self.credits_transition_index < 0:
            self.credits_transition = 0
            self.credits_transition_index = 0

        frame = self.credits_frames[int(self.credits_transition_index)]
        frame_rect = frame.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 130))
        self.screen.blit(frame, frame_rect)

        self.credits_transition_index += self.credits_transition
