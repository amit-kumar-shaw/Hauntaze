import pygame
from settings import *

class Menu():
    def __init__(self, ):
        self.screen = pygame.display.get_surface()

    def update(self):

        self.screen.fill((79,79,79))
        title_font = pygame.font.Font('./assets/fonts/BleedingPixels.ttf', 50)
        title = title_font.render('HAUNTAZE', False, TITLE_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)

        title_font = pygame.font.Font('./assets/fonts/PixelDevilsdeal.ttf', 20)
        title = title_font.render('Press ENTER to start', False, 'white')
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT-50))
        self.screen.blit(title, title_rect)

        # title_font = pygame.font.Font('./assets/fonts/PixelDevilsdeal.ttf', 50)
        # title = title_font.render('HAUNTAZE', False, TITLE_COLOR)
        # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        # self.screen.blit(title, title_rect)
        #
        # title_font = pygame.font.Font('./assets/fonts/PixelRunes.ttf', 50)
        # title = title_font.render('HAUNTAZE', False, TITLE_COLOR)
        # title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 280))
        # self.screen.blit(title, title_rect)