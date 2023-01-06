import sys

import pygame
from settings import *
from stones import Stone
from utilities import import_frames


class Transition:
    def __init__(self, p1, p2):

        self.display = pygame.display.get_surface()

        # self.multiplayer = multiplayer
        self.tower_surface = pygame.Surface((64, 320))

        self.tower_rect = self.tower_surface.get_rect(topleft=(576, 0))
        self.screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.castle = pygame.image.load("./assets/images/transitions/castle.png").convert_alpha()

        self.intro_completed = False
        self.life_completed = False
        self.death_completed = False
        self.curse_completed = False
        self.completed = False

        self.level = 1
        self.frame_index = 1

        self.intro_frames = None
        self.intro_index = 0

        self.life_frames = None
        self.life_index = 0

        self.death_frames = None
        self.death_index = 0

        self.curse_frames = None
        self.curse_index = 0

        self.tower1_frames = import_frames(f"./assets/images/transitions/tower/tower1", scale=1)
        self.tower_index = 0

        self.p1_active = p1
        self.p2_active = p2
        self.path_index = 0
        if self.p1_active:
            path = f'./assets/images/player/p1/'
            self.p1_frames = {'idle': [], 'walk': []}

            for status in self.p1_frames.keys():
                full_path = path + status
                self.p1_frames[status] = import_frames(full_path, scale=0.8)

            self.p1_frame_index = 0
            self.p1_image = self.p1_frames['idle'][0]
            self.p1_rect = self.p1_image.get_rect(bottomleft=(24, 288))
            self.p1_direction = pygame.math.Vector2()
            self.p1_flipped = False
            self.p1_direction_changed = False
            self.p1_path = [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                            (1, 0), (1, 0), (1, 0), (1, 0),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0),
                            (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)]

        if self.p2_active:
            path = f'./assets/images/player/p2/'
            self.p2_frames = {'idle': [], 'walk': []}

            for status in self.p2_frames.keys():
                full_path = path + status
                self.p2_frames[status] = import_frames(full_path, scale=0.8)
            self.p2_index = 0
            self.p2_frame_index = 0
            self.p2_image = self.p2_frames['idle'][self.p2_index]
            self.p2_rect = self.p2_image.get_rect(bottomleft=(16, 288))
            self.p2_direction = pygame.math.Vector2()
            self.p2_flipped = False
            self.p2_direction_changed = False
            self.p2_path = [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                            (1, 0),
                            (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1),
                            (0, 1),
                            (0, 1), (0, 1), (0, 1), (0, 1),
                            (-1, 0), (-1, 0),
                            (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)]

        self.stones = []
        self.stones.append(Stone((160, SCREEN_HEIGHT / 2), 'life', 1.5))
        self.stones.append(Stone((320, SCREEN_HEIGHT / 2), 'death', 1.5))
        self.stones.append(Stone((480, SCREEN_HEIGHT / 2), 'curse', 1.5))
        for stone in self.stones:
            stone.active = False

    def update(self):
        # if self.level == 1:
        #     self.intro()
        # elif self.level == 6:
        #     self.life()
        # elif self.level == 11:
        #     self.death()
        # else:
        #     self.tower()

        if self.level <= 5:
            if not self.intro_completed:
                self.intro()
            else:
                self.tower()
        elif 5 < self.level <= 10:
            if not self.life_completed:
                self.life()
            else:
                self.tower()
        elif 10 < self.level <= 15:
            if not self.death_completed:
                self.death()
            else:
                self.tower()
        else:
            self.curse()
        #
        # self.draw()

    def intro(self):
        if self.intro_frames is None:
            self.intro_frames = import_frames(f"./assets/images/transitions/intro", scale=1)
            self.screen_surface.fill('black')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.intro_completed = True

        self.intro_index += 0.2
        if self.intro_index >= len(self.intro_frames): self.intro_index = 225

        # self.screen_surface = self.intro_frames[int(self.intro_index)]
        if self.intro_index < 0.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (160, 50, 320, 20), (160, 50, 320, 20))
        elif 4 < self.intro_index < 75:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (84, 112, 475, 16), (84, 112, 475, 16))
        elif 80 < self.intro_index < 117:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (198, 144, 246, 13), (198, 144, 246, 13))
        elif 131 < self.intro_index < 131.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (101, 222, 116, 14), (101, 222, 116, 14))
        elif 145 < self.intro_index < 145.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (253, 222, 133, 16), (253, 222, 133, 16))
        elif 160 < self.intro_index < 160.5:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (413, 222, 134, 15), (413, 222, 134, 15))
        elif 175 < self.intro_index < 222:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (161, 263, 319, 16), (161, 263, 319, 16))
        if 131 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (139, 180, 44, 40), (139, 180, 44, 40))
        if 145 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (299, 181, 42, 39), (299, 181, 42, 39))
        if 160 < self.intro_index:
            self.screen_surface.blit(self.intro_frames[int(self.intro_index)], (458, 182, 44, 39), (458, 182, 44, 39))

        if self.intro_completed:
            self.screen_surface.fill('black')
        self.display.blit(self.screen_surface, (0, 0))

    def life(self):
        if self.life_frames is None:
            self.life_frames = import_frames(f"./assets/images/transitions/life", scale=1)
            self.screen_surface.fill('black')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.life_completed = True

        self.life_index += 0.2
        if self.life_index >= len(self.life_frames): self.life_index = 265

        # self.screen_surface = self.life_frames[int(self.life_index)]
        if self.life_index < 0.5:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (255, 223, 131, 14), (255, 223, 131, 14))
        elif 4 < self.life_index < 39:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (180, 112, 280, 15), (180, 112, 280, 15))
        elif 44 < self.life_index < 112:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (48, 142, 542, 18), (48, 142, 542, 18))
        elif 130 < self.life_index < 196:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (46, 262, 548, 19), (46, 262, 548, 19))
        elif 202 < self.life_index < 261:
            self.screen_surface.blit(self.life_frames[int(self.life_index)], (82, 290, 475, 21), (82, 290, 475, 21))

        self.screen_surface.blit(self.life_frames[int(self.life_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        if self.life_completed:
            self.screen_surface.fill('black')

        self.display.blit(self.screen_surface, (0, 0))

    def death(self):
        if self.death_frames is None:
            self.death_frames = import_frames(f"./assets/images/transitions/death", scale=1)
            self.screen_surface.fill('black')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.death_completed = True

        self.death_index += 0.2
        if self.death_index >= len(self.death_frames): self.death_index = 253

        # self.screen_surface = self.death_frames[int(self.death_index)]
        if self.death_index < 0.5:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (245, 223, 151, 15), (245, 223, 151, 15))
        elif 4 < self.death_index < 40:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (170, 111, 298, 16), (170, 111, 298, 16))
        elif 44 < self.death_index < 114:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (45, 141, 551, 19), (45, 141, 551, 19))
        elif 120 < self.death_index < 196:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (6, 262, 627, 19), (6, 262, 627, 19))
        elif 202 < self.death_index < 250:
            self.screen_surface.blit(self.death_frames[int(self.death_index)], (123, 292, 392, 15), (123, 292, 392, 15))

        self.screen_surface.blit(self.death_frames[int(self.death_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        if self.death_completed:
            self.screen_surface.fill('black')

        self.display.blit(self.screen_surface, (0, 0))

    def curse(self):
        if self.curse_frames is None:
            self.curse_frames = import_frames(f"./assets/images/transitions/curse", scale=1)
            self.screen_surface.fill('black')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.curse_completed = True
            pygame.quit()
            sys.exit()

        self.curse_index += 0.2
        if self.curse_index >= len(self.curse_frames): self.curse_index = 135

        # self.screen_surface = self.curse_frames[int(self.curse_index)]
        if self.curse_index < 0.5:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (196, 49, 249, 28), (196, 49, 249, 28))
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (244, 222, 152, 17), (244, 222, 152, 17))
        elif 4 < self.curse_index < 40:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (170, 111, 299, 16), (170, 111, 299, 16))
        elif 44 < self.curse_index < 98:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (107, 142, 424, 19), (107, 142, 424, 19))
        elif 105 < self.curse_index < 133:
            self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (182, 262, 279, 20), (182, 262, 279, 20))

        self.screen_surface.blit(self.curse_frames[int(self.curse_index)], (300, 181, 40, 39), (300, 181, 40, 39))

        self.display.blit(self.screen_surface, (0, 0))

    def tower(self):

        if self.path_index >= 80:
            self.completed = True
            self.tower_index = 0
            self.path_index = 0
            if self.p1_active:
                self.p1_direction_changed = False
                self.p1_image = self.p1_frames['idle'][0]
            if self.p2_active:
                self.p2_direction_changed = False
                self.p2_image = self.p2_frames['idle'][0]
        else:
            self.move_players()

        if self.p1_active and self.p1_flipped:
            self.p1_image = pygame.transform.flip(self.p1_image, True, False)
        if self.p2_active and self.p2_flipped:
            self.p2_image = pygame.transform.flip(self.p2_image, True, False)
        self.tower_surface.blit(self.tower1_frames[0], (0, 0))
        if self.p2_active:
            self.tower_surface.blit(self.p2_image, self.p2_rect)
        if self.p1_active:
            self.tower_surface.blit(self.p1_image, self.p1_rect)

        self.display.blit(self.tower_surface, self.tower_rect)
        self.path_index += 1

    def move_players(self):
        x = (self.level - 1) % 5 #if self.level % 5 != 0 else 5
        if x == 0:
            self.change_tower()
        else:
            if x % 2 == 0:
                if self.p1_active:
                    self.p1_direction.x = -1
                if self.p2_active:
                    self.p2_direction.x = -1
            else:
                if self.p1_active:
                    self.p1_direction.x = 1
                if self.p2_active:
                    self.p2_direction.x = 1

            if self.p1_active:
                if self.path_index > 16 and not self.p1_direction_changed:
                    self.p1_flipped = not self.p1_flipped
                    self.p1_direction_changed = True

                self.p1_rect.x += self.p1_direction.x * self.p1_path[int(self.path_index)][0]
                self.p1_rect.y -= self.p1_path[int(self.path_index)][1]

                status = self.p1_frames['walk']
                self.p1_frame_index += 0.2
                if self.p1_frame_index >= len(status):
                    self.p1_frame_index = 0

                self.p1_image = status[int(self.p1_frame_index)]

            if self.p2_active:
                if self.path_index > 24 and not self.p2_direction_changed:
                    self.p2_flipped = not self.p2_flipped
                    self.p2_direction_changed = True

                self.p2_rect.x += self.p2_direction.x * self.p2_path[int(self.path_index)][0]
                self.p2_rect.y -= self.p2_path[int(self.path_index)][1]

                status = self.p2_frames['walk']
                self.p2_frame_index += 0.2
                if self.p2_frame_index >= len(status):
                    self.p2_frame_index = 0

                self.p2_image = status[int(self.p2_frame_index)]

    def change_tower(self):
        if self.p1_active:
            self.p1_rect = self.p1_image.get_rect(bottomleft=(24, 288))
        if self.p2_active:
            self.p2_rect = self.p1_image.get_rect(bottomleft=(16, 288))

    def draw(self):

        if self.level == 1 or self.level == 6 or self.level == 11 or self.level == 16:
            self.display.blit(self.screen_surface, (0, 0))
        else:
            self.display.blit(self.tower_surface, self.tower_rect)

    def intro_gen(self):
        self.frame_index += 1
        for stone in self.stones:
            stone.animate()
        self.screen_surface.fill('black')
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Welcome to Hauntaze!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'The search of forbidden treasure has cursed you to turn into a ghost.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'To lift the curse you need to collect:'
        if self.frame_index > 80:
            if self.frame_index - 80 < len(m1):
                m1 = m1[0:self.frame_index - 80]
            font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
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
                m1 = m1[0:self.frame_index - 175]
            font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/intro/intro_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/intro/intro_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/intro/intro_{self.frame_index}.png')

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
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Life Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'The Life Stone gives you the power to revive yourself once you die.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index - 45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
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
                m1 = m1[0:self.frame_index - 130]
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
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/life/life_00{self.frame_index}.png')
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
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Death Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'The Death Stone gives you the power to kill all your enemies at once.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index - 45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
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
                m1 = m1[0:self.frame_index - 120]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Press the Yellow button to activate Death Stone.'
        if self.frame_index > 202:
            if self.frame_index - 202 < len(m1):
                m1 = m1[0:self.frame_index - 202]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 300))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index < 300:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/death/death_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/death/death_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/death/death_{self.frame_index}.png')

    def stone3_gen(self):
        self.frame_index += 1

        self.stones[0].active = True
        self.stones[1].active = True
        self.stones[2].active = True
        self.stones[0].animate()
        self.stones[1].animate()
        self.stones[2].animate()
        # for stone in self.stones:
        #     stone.animate()
        self.screen_surface.fill('black')
        font = pygame.font.Font('./assets/fonts/1.ttf', 24)
        msg = font.render('Congratulations!', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have collected The Curse Stone.'

        if self.frame_index > 5:
            if self.frame_index - 5 < len(m1):
                m1 = m1[0:self.frame_index - 5]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 120))
            self.screen_surface.blit(msg, msg_rect)

        m1 = 'Your curse is lifted and forbidden treasure is yours.'
        if self.frame_index > 45:
            if self.frame_index - 45 < len(m1):
                m1 = m1[0:self.frame_index - 45]
            font = pygame.font.Font('./assets/fonts/1.ttf', 12)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 150))
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
            self.stones[2].rect = self.stones[2].image.get_rect(center=(320, 200))
            self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
            font = pygame.font.Font('./assets/fonts/1.ttf', 14)
            msg = font.render('The Curse Stone', False, 'white')
            msg_rect = msg.get_rect(center=(320, 230))
            self.screen_surface.blit(msg, msg_rect)

        # if self.frame_index > 0:
        #     self.stones[2].rect = self.stones[2].image.get_rect(center=(480, 200))
        #     self.screen_surface.blit(self.stones[2].image, self.stones[2].rect)
        #     font = pygame.font.Font('./assets/fonts/1.ttf', 14)
        #     msg = font.render('The Curse Stone', False, 'white')
        #     msg_rect = msg.get_rect(center=(480, 230))
        #     self.screen_surface.blit(msg, msg_rect)

        m1 = 'You have completed Hauntaze.'
        if self.frame_index > 105:
            if self.frame_index - 105 < len(m1):
                m1 = m1[0:self.frame_index - 105]
            font = pygame.font.Font('./assets/fonts/1.ttf', 15)
            msg = font.render(m1, False, 'white')
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH / 2, 270))
            self.screen_surface.blit(msg, msg_rect)

        if self.frame_index < 150:
            if self.frame_index < 10:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/curse/curse_00{self.frame_index}.png')
            elif self.frame_index < 100:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/curse/curse_0{self.frame_index}.png')
            else:
                pygame.image.save(self.screen_surface,
                                  f'./assets/images/transitions/curse/curse_{self.frame_index}.png')
