import random

import pygame, sys
from src.settings import *
# from level import Level
# from ui import UI
from src.music import GameSound
# from menu import Menu
from src.game import Game
from src.pyvidplayer import Video

import os

os.chdir('..')

# Pygame setup
pygame.init()
flags = pygame.SCALED #| pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption('Hauntaze')
clock = pygame.time.Clock()
# start = False
# level_loaded = False
# level = Level(player1=True, player2=True)
sound = GameSound()
sound.playbackgroundmusic()
# menu = Menu()
# ui = None
game = Game()
vid = Video('./assets/test_video.mp4')
vid.set_size((640, 360))

def intro():
    while True:
        vid.draw(screen, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                game.run()
while True:
    # event loop
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if keys[pygame.K_RETURN] and (menu.is_player1_ready or menu.is_player2_ready):
        #     start = True

    #screen.fill(BG_COLOR)
    intro()

    # TODO: Remove later. display FPS
    font = pygame.font.Font('./assets/fonts/4.ttf', 16)
    fps_msg = font.render(f'FPS: {float("{:.2f}".format(clock.get_fps()))}', False, 'white')
    # print(clock.get_fps())
    msg_rect = fps_msg.get_rect(center=(SCREEN_WIDTH // 2 + 200, 20))
    UI_SURFACE.blit(fps_msg, msg_rect)
    game.fps = f'FPS: {float("{:.2f}".format(clock.get_fps()))}'
    # if start:
    #     if not level_loaded:
    #         level = Level(player1=menu.is_player1_ready, player2=menu.is_player2_ready)
    #         ui = UI(menu.is_player1_ready, menu.is_player2_ready, level)
    #         level_loaded = True
    #     level.run()
    #     ui.update()
    #     # display fps
    #     font = pygame.font.Font('./assets/fonts/1.ttf', 10)
    #     fps_msg = font.render(f'FPS: {float("{:.2f}".format(clock.get_fps()))}', False, 'white')
    #     msg_rect = fps_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
    #     screen.blit(fps_msg, msg_rect)
    # else:
    #     menu.update()

    # drawing logic
    pygame.display.update()
    clock.tick(FPS)
