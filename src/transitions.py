import pygame
from settings import *
from stones import Stone
from utilities import import_frames


class Transition:
    def __init__(self, multiplayer):

        self.display = pygame.display.get_surface()

        self.multiplayer = multiplayer
        self.tower_surface = pygame.Surface((64, 320))
        self.tower_rect = self.tower_surface.get_rect(topleft=(576, 0))
        self.screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.level = 1
        self.frame_index = 1

        self.intro_frames = import_frames(f"./assets/images/transitions/intro", scale=1)
        self.intro_index = 0

        self.stones = []
        self.stones.append(Stone((160, SCREEN_HEIGHT / 2), 'life', 1.5))
        self.stones.append(Stone((320, SCREEN_HEIGHT / 2), 'death', 1.5))
        self.stones.append(Stone((480, SCREEN_HEIGHT / 2), 'curse', 1.5))
        for stone in self.stones:
            stone.active = True

    def update(self):
        if self.level == 1:
            self.intro()
        self.draw()

    def intro(self):
        self.intro_index += 0.2
        if self.intro_index >= len(self.intro_frames): self.intro_index = 225
        self.screen_surface = self.intro_frames[int(self.intro_index)]

    def intro_gen(self):
        self.frame_index += 1
        for stone in self.stones:
            stone.animate()
        self.screen_surface.fill('black')
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Welcome to Hauntaze!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'The search of forbidden treasure has cursed you to turn into a ghost.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index-5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'To lift the curse you need to collect:'
        if self.frame_index > 80:
            if self.frame_index - 80 < len(m1):
                m1 = m1[0:self.frame_index-80]
            font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 150))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 130:
            self.stones[0].rect = self.stones[0].image.get_rect(center=(160, 200))
            self.screen_surface.blit(self.stones[0].image, self.stones[0].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render('The Life Stone', False, 'white')
            msg_rect = msg.get_rect(center=(160, 230))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 145:
            self.stones[1].rect = self.stones[1].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[1].image, self.stones[1].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render('The Death Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 160:
            self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
            self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render('The Curse Stone', False, 'white')
            msg_rect = msg.get_rect(center=(480, 230))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Defeat the stone defenders and lift your curse.'
        if self.frame_index > 175:
            if self.frame_index - 175 < len(m1):
                m1 = m1[0:self.frame_index-175]
            font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface, f'./assets/images/transitions/intro/intro_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface, f'./assets/images/transitions/intro/intro_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/intro/intro_{self.frame_index}.png')

    def draw(self):

        if self.level == 1:
            self.display.blit(self.screen_surface, (0, 0))
        else:
            self.display.blit(self.tower_surface, self.tower_rect)
