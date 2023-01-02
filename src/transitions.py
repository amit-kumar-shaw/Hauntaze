import pygame
from settings import *
from stones import Stone
from utilities import import_frames


class Transition:
    def __init__(self, multiplayer):

        self.display = pygame.display.get_surface()

        self.multiplayer = multiplayer
        self.tower_surface = pygame.Surface((64, 320))
        self.tower_surface = pygame.image.load("./assets/images/tower1.png").convert_alpha()
        self.tower_rect = self.tower_surface.get_rect(topleft=(576, 0))
        self.screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.level = 1
        self.frame_index = 1

        self.intro_frames = import_frames(f"./assets/images/transitions/intro", scale=1)
        self.intro_index = 0

        self.life_frames = import_frames(f"./assets/images/transitions/life", scale=1)
        self.life_index = 0

        self.death_frames = import_frames(f"./assets/images/transitions/death", scale=1)
        self.death_index = 0

        self.stones = []
        self.stones.append(Stone((160, SCREEN_HEIGHT / 2), 'life', 1.5))
        self.stones.append(Stone((320, SCREEN_HEIGHT / 2), 'death', 1.5))
        self.stones.append(Stone((480, SCREEN_HEIGHT / 2), 'curse', 1.5))
        for stone in self.stones:
            stone.active = False

    def update(self):
        if self.level == 1:
            self.intro()
        elif self.level == 6:
            self.life()
        elif self.level == 11:
            self.death()
        self.draw()

    def intro(self):
        self.intro_index += 0.2
        if self.intro_index >= len(self.intro_frames): self.intro_index = 225
        self.screen_surface = self.intro_frames[int(self.intro_index)]

    def life(self):
        self.life_index += 0.2
        if self.life_index >= len(self.life_frames): self.life_index = 260
        self.screen_surface = self.life_frames[int(self.life_index)]

    def death(self):
        self.death_index += 0.2
        if self.death_index >= len(self.death_frames): self.death_index = 260
        self.screen_surface = self.death_frames[int(self.death_index)]

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

        if self.level == 1 or self.level == 6 or self.level == 11:
            self.display.blit(self.screen_surface, (0, 0))
        else:
            self.display.blit(self.tower_surface, self.tower_rect)

    def stone_gen(self):
        self.frame_index += 1

        self.stones[0].active = True
        self.stones[1].active = False
        self.stones[2].active = False
        self.stones[0].animate()
        # for stone in self.stones:
        #     stone.animate()
        self.screen_surface.fill('black')
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Life Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index-5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'The Life Stone gives you the power to revive yourself once you die.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index-45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 150))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 0:

            self.stones[0].rect = self.stones[0].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[0].image, self.stones[0].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Life Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #     self.stones[1].rect = self.stones[1].image.get_rect(center=(320, 200))
        #     self.screen_surface.blit(self.stones[1].image, self.stones[1].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Death Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(320, 230))
        #     self.screen_surface.blit(msg, msg_rect)
        #
        # if self.frame_index > 0:
        #     self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
        #     self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Curse Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(480, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        m1 = 'Remember, you can revive yourself only once during the whole game.'
        if self.frame_index > 130:
            if self.frame_index - 130 < len(m1):
                m1 = m1[0:self.frame_index-130]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Press the Blue button within 10 seconds to revive yourself.'
        if self.frame_index > 202:
            if self.frame_index - 202 < len(m1):
                m1 = m1[0:self.frame_index - 202]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 300))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface, f'./assets/images/transitions/life/life_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface, f'./assets/images/transitions/life/life_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/life/life_{self.frame_index}.png')

    def stone2_gen(self):
        self.frame_index += 1

        self.stones[0].active = True
        self.stones[1].active = True
        self.stones[2].active = False
        self.stones[0].animate()
        self.stones[1].animate()
        # for stone in self.stones:
        #     stone.animate()
        self.screen_surface.fill('black')
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Death Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index-5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'The Death Stone gives you the power to kill all your enemies at once.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index-45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, 150))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #
        #     self.stones[0].rect = self.stones[0].image.get_rect(center=(320, 200))
        #     self.screen_surface.blit(self.stones[0].image, self.stones[0].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Life Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(320, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        if self.frame_index > 0:
            self.stones[1].rect = self.stones[1].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[1].image, self.stones[1].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Death Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #     self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
        #     self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Curse Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(480, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        m1 = 'Remember, the Death Stone can be activated only once during the whole game.'
        if self.frame_index > 120:
            if self.frame_index - 120 < len(m1):
                m1 = m1[0:self.frame_index-120]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface, f'./assets/images/transitions/death/death_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface, f'./assets/images/transitions/death/death_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/death/death_{self.frame_index}.png')