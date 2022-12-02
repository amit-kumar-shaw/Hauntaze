import pygame
from settings import *


class UI:
    def __init__(self, player1, player2, level):
        self.player1_playing = player1
        self.player2_playing = player2
        self.level = level

    def update(self):
        font = pygame.font.Font('./assets/fonts/1.ttf', 10)
        if self.player1_playing:
            player_name = font.render('Player 1', False, 'white')
            player_rect = player_name.get_rect(midleft=(16, 8))
            hearts_rect = []
            heart = pygame.image.load("./assets/images/heart.png").convert_alpha()
            heart = pygame.transform.rotozoom(heart, 0, 0.75)
            key = pygame.image.load("./assets/images/key/3.png").convert_alpha()
            # key = pygame.transform.rotozoom(key, 0, 0.75)
            key_rect = key.get_rect(bottomleft=player_rect.bottomright)
            for i in range(0, self.level.player1.lives):
                hearts_rect.append(heart.get_rect(topleft=(16 + (i * 12), 14)))

            coin = pygame.image.load("./assets/images/coin.png").convert_alpha()
            coin_rect = coin.get_rect(topleft=(16, 24))

            score_font = pygame.font.Font('./assets/fonts/1.ttf', 10)
            score_msg = score_font.render(f'{self.level.player1.score}', False, 'white')
            score_rect = score_msg.get_rect(topleft=(30, 26))

            UI_SURFACE.blit(player_name, player_rect)

            if self.level.player1.key_picked:
                UI_SURFACE.blit(key, key_rect)
            for i in range(0, self.level.player1.lives):
                UI_SURFACE.blit(heart, hearts_rect[i])
            UI_SURFACE.blit(coin, coin_rect)
            UI_SURFACE.blit(score_msg, score_rect)

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
        level = font.render('LEVEL 0', False, 'white')
        level_rect = level.get_rect(center=(SCREEN_WIDTH // 2, 15))
        UI_SURFACE.blit(level, level_rect)

        font = pygame.font.Font('./assets/fonts/4.ttf', 16)
        msg = font.render('ESC: Pause', False, 'white')
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, 35))
        UI_SURFACE.blit(msg, msg_rect)

        # # TODO: Remove later. display FPS
        # font = pygame.font.Font('./assets/fonts/4.ttf', 16)
        # fps_msg = font.render(f'FPS: {float("{:.2f}".format(pygame.time.Clock().get_fps()))}', False, 'white')
        # msg_rect = fps_msg.get_rect(center=(SCREEN_WIDTH // 2 + 50, 35))
        # UI_SURFACE.blit(fps_msg, msg_rect)

        pygame.display.get_surface().blit(UI_SURFACE, (0, (ROWS * CELL_SIZE * TILE_HEIGHT)))
        UI_SURFACE.fill('black')
