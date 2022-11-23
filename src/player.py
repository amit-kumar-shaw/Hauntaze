import pygame
from pygame.locals import *
from settings import *
from torch import Torch

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, collectible_sprites, player2=False):
        super().__init__(groups)

        if player2:
            self.player_still = pygame.image.load('./assets/images/player/p2_01.png').convert_alpha()
            self.player_walk_1 = pygame.image.load('./assets/images/player/p2_02.png').convert_alpha()
            self.player_walk_2 = pygame.image.load('./assets/images/player/p2_03.png').convert_alpha()
            # self.image = pygame.image.load("./v1/p1_01.png").convert_alpha()
        else:
            self.player_still = pygame.image.load('./assets/images/player/p1_01.png').convert_alpha()
            self.player_walk_1 = pygame.image.load('./assets/images/player/p1_02.png').convert_alpha()
            self.player_walk_2 = pygame.image.load('./assets/images/player/p1_03.png').convert_alpha()
        # self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.player_walk_1 = pygame.transform.rotozoom(self.player_walk_1, 0, 0.7)
        self.player_walk_2 = pygame.transform.rotozoom(self.player_walk_2, 0, 0.7)
        self.player_still = pygame.transform.rotozoom(self.player_still, 0, 0.7)
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_index = 0

        self.image = self.player_still

        self.rect = self.image.get_rect(topleft=pos)

        self.torch = Torch(pos, groups)
        self.player2 = player2
        self.lives = LIVES
        self.score = 0
        self.key_picked = False

        # player movement
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

        self.collision_sprites = collision_sprites
        self.collectible_sprites = collectible_sprites

        # player keys
        if player2:
            self.MOVE_LEFT = K_LEFT
            self.MOVE_RIGHT = K_RIGHT
            self.MOVE_UP = K_UP
            self.MOVE_DOWN = K_DOWN

        else:
            self.MOVE_LEFT = K_a
            self.MOVE_RIGHT = K_d
            self.MOVE_UP = K_w
            self.MOVE_DOWN = K_s

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[self.MOVE_RIGHT]:
            self.direction.x = 1
        elif keys[self.MOVE_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[self.MOVE_UP]:
            self.direction.y = -1
        elif keys[self.MOVE_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

    def animate(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.image = self.player_still
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def collectible_collisions(self):
        for sprite in self.collectible_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                self.score += 1
                sprite.kill()

    def key_collisions(self):
        if self.rect.colliderect(self.key.rect) and not self.key_picked:
            print("key picked")
            self.key_picked = True
            self.key.kill()

    def display_details(self):
        font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        player_name = font.render('Player 1', False, 'white')
        player_rect = player_name.get_rect(midleft=(16, (ROWS*CELL_SIZE*TILE_HEIGHT) + 8))
        hearts_rect = []
        heart = pygame.image.load("./assets/images/heart.png").convert_alpha()
        heart = pygame.transform.rotozoom(heart, 0, 0.75)
        for i in range(0,self.lives):
            hearts_rect.append(heart.get_rect(topleft = (16 + (i*12), (ROWS*CELL_SIZE*TILE_HEIGHT) + 14) ))

        coin = pygame.image.load("./assets/images/coin.png").convert_alpha()
        coin_rect = coin.get_rect(topleft=(16, (ROWS * CELL_SIZE * TILE_HEIGHT) + 24))

        score_font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        score_msg = score_font.render(f'{self.score}', False, 'white')
        score_rect = score_msg.get_rect(topleft=(30, (ROWS * CELL_SIZE * TILE_HEIGHT) + 26))

        if self.player2:
            player_name = font.render('Player 2', False, 'white')
            player_rect = player_name.get_rect(midright=(SCREEN_WIDTH - 16, (ROWS*CELL_SIZE*TILE_HEIGHT) + 5))
            for i in range(0, self.lives):
                hearts_rect[i] = heart.get_rect(topright=(SCREEN_WIDTH - 16 - (i * 12), (ROWS * CELL_SIZE * TILE_HEIGHT) + 14))
            coin_rect = coin.get_rect(topright=(SCREEN_WIDTH - 16, (ROWS * CELL_SIZE * TILE_HEIGHT) + 24))
            score_rect = score_msg.get_rect(topright=(SCREEN_WIDTH - 30, (ROWS * CELL_SIZE * TILE_HEIGHT) + 26))

        pygame.display.get_surface().blit(player_name, player_rect)
        for i in range(0, self.lives):
            pygame.display.get_surface().blit(heart, hearts_rect[i])
        pygame.display.get_surface().blit(coin, coin_rect)
        pygame.display.get_surface().blit(score_msg, score_rect)


    def update(self):
        self.input()

        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()

        self.rect.y += self.direction.y * self.speed
        self.vertical_collisions()
        self.collectible_collisions()
        self.key_collisions()
        self.animate()

        self.torch.rect = self.image.get_rect(midtop=(self.rect.x + 2, self.rect.y))
        self.torch.animate()

        self.display_details()
        # font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        # score_msg = font.render(f'Player 1 Score: {self.score}', False, 'white')
        # msg_rect = score_msg.get_rect(midleft=(10, SCREEN_HEIGHT - 10))
        # if self.player2:
        #     score_msg = font.render(f'Player 2 Score: {self.score}', False, 'white')
        #     msg_rect = score_msg.get_rect(midright=(SCREEN_WIDTH -10, SCREEN_HEIGHT - 10))
        #
        # pygame.display.get_surface().blit(score_msg, msg_rect)
