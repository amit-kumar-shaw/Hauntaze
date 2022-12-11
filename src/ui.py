import pygame
from settings import *


class UI:
    def __init__(self, player1, player2, level):
        self.player1_playing = player1
        self.player2_playing = player2
        self.level = level
        self.current_level = None

        font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        coin = pygame.image.load("./assets/images/coin.png").convert_alpha()
        heart = pygame.image.load("./assets/images/heart.png").convert_alpha()
        self.heart = pygame.transform.rotozoom(heart, 0, 0.75)

        if player1:
            self.p1_surf = pygame.Surface((100, SCREEN_HEIGHT - (ROWS * CELL_SIZE * TILE_HEIGHT)))
            self.p1_surf.fill('black')

            player_name = font.render('Player 1', False, 'white')
            player_rect = player_name.get_rect(midleft=(0, 8))
            self.p1_surf.blit(player_name, player_rect)

            coin_rect = coin.get_rect(topleft=(0, 24))
            self.p1_surf.blit(coin, coin_rect)

            self.key1 = pygame.image.load("./assets/images/key/3.png").convert_alpha()
            self.key_rect = self.key1.get_rect(bottomleft=player_rect.bottomright)

            self.p1_score = -1

        if player2:
            self.p2_surf = pygame.Surface((100, SCREEN_HEIGHT - (ROWS * CELL_SIZE * TILE_HEIGHT)))
            self.p2_surf.fill('black')

    def update(self):
        font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        if self.player1_playing:
            UI_SURFACE.blit(self.p1_surf, (16, 0))
            # player_name = font.render('Player 1', False, 'white')
            # player_rect = player_name.get_rect(midleft=(16, 8))
            hearts_rect = []
            # heart = pygame.image.load("./assets/images/heart.png").convert_alpha()
            # heart = pygame.transform.rotozoom(heart, 0, 0.75)
            # key = pygame.image.load("./assets/images/key/3.png").convert_alpha()
            # # key = pygame.transform.rotozoom(key, 0, 0.75)
            # key_rect = key.get_rect(bottomleft=player_rect.bottomright)
            for i in range(0, self.level.player1.lives):
                # hearts_rect.append(self.heart.get_rect(topleft=(16 + (i * 12), 14)))
                UI_SURFACE.blit(self.heart, self.heart.get_rect(topleft=(16 + (i * 12), 14)))

            # coin = pygame.image.load("./assets/images/coin.png").convert_alpha()
            # coin_rect = coin.get_rect(topleft=(16, 24))

            score_font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            if self.level.player1.score > self.p1_score:
                self.p1_score_msg = score_font.render(f'{self.level.player1.score}', False, 'white')
            score_rect = self.p1_score_msg.get_rect(topleft=(30, 26))

            # UI_SURFACE.blit(player_name, player_rect)

            if self.level.player1.key_picked:
                UI_SURFACE.blit(self.key1, self.key_rect)
            # for i in range(0, self.level.player1.lives):
            #     UI_SURFACE.blit(self.heart, hearts_rect[i])
            # UI_SURFACE.blit(coin, coin_rect)
            UI_SURFACE.blit(self.p1_score_msg, score_rect)

        if self.player2_playing:
            key = pygame.image.load("./assets/images/key/1.png").convert_alpha()
            # key = pygame.transform.rotozoom(key, 0, 0.75)
            player_name = font.render('Player 2', False, 'white')
            player_rect = player_name.get_rect(midright=(SCREEN_WIDTH - 16, 8))
            hearts_rect = []
            heart = pygame.image.load("./assets/images/heart.png").convert_alpha()
            heart = pygame.transform.rotozoom(heart, 0, 0.75)
            key_rect = key.get_rect(bottomright=player_rect.bottomleft)
            for i in range(0, self.level.player2.lives):
                hearts_rect.append(heart.get_rect(topright=(SCREEN_WIDTH - 16 - (i * 12), 14)))
            coin = pygame.image.load("./assets/images/coin.png").convert_alpha()
            coin_rect = coin.get_rect(topright=(SCREEN_WIDTH - 16, 24))
            score_font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            score_msg = score_font.render(f'{self.level.player2.score}', False, 'white')
            score_rect = score_msg.get_rect(topright=(SCREEN_WIDTH - 30, 26))

            UI_SURFACE.blit(player_name, player_rect)
            if self.level.player2.key_picked:
                UI_SURFACE.blit(key, key_rect)
            for i in range(0, self.level.player2.lives):
                UI_SURFACE.blit(heart, hearts_rect[i])
            UI_SURFACE.blit(coin, coin_rect)
            UI_SURFACE.blit(score_msg, score_rect)

        font = pygame.font.Font('./assets/fonts/1.ttf', 16)
        level = font.render(f'LEVEL {self.current_level}', False, 'white')
        level_rect = level.get_rect(center=(SCREEN_WIDTH // 2, 15))
        UI_SURFACE.blit(level, level_rect)

        font = pygame.font.Font('./assets/fonts/4.ttf', 16)
        msg = font.render('ESC: Pause', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, 35))
        UI_SURFACE.blit(msg, msg_rect)

        # # TODO: Remove later. display FPS
        font = pygame.font.Font('./assets/fonts/4.ttf', 16)
        # fps_msg = font.render(f'FPS: {float("{:.2f}".format(pygame.time.Clock().get_fps()))}', False, 'white')
        fps_msg = font.render(self.fps, False, 'white')
        msg_rect = fps_msg.get_rect(center=(SCREEN_WIDTH // 2 + 170, 20))
        UI_SURFACE.blit(fps_msg, msg_rect)

        pygame.display.get_surface().blit(UI_SURFACE, (0, (ROWS * CELL_SIZE * TILE_HEIGHT)))
        UI_SURFACE.fill('black')
