import pygame


class GameSound(object):

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./assets/Audio/Magic Escape Room.mp3')
        pygame.mixer.music.set_volume(0.5)

    @staticmethod
    def playbackgroundmusic():
        pygame.mixer.music.play(-1)