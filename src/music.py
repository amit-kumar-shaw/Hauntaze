import pygame


class GameSound(object):

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./assets/Audio/Magic Escape Room.mp3')
        pygame.mixer.music.set_volume(0.5)

    @staticmethod
    def playbackgroundmusic():
        pygame.mixer.music.play(-1)


class PlayerSound(object):

    def __init__(self):
        pygame.mixer.init()
        # pygame.mixer.music.load('./assets/Audio/Magic Escape Room.mp3')
        # pygame.mixer.music.set_volume(0.5)

    def play_enemy_collision(self):
        pygame.mixer.music.load('./assets/Audio/enemy_collision.mp3')
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

    def play_coin_collection(self):
        pygame.mixer.music.load('./assets/Audio/collect_coins.mp3')
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()