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

    def play_enemy_collision(self):
        sound = pygame.mixer.Sound('./assets/Audio/enemy_collision.mp3')
        sound.set_volume(0.7)
        sound.play()
        # self.enemy_collision.play()

    def play_coin_collection(self):
        sound = pygame.mixer.Sound('./assets/Audio/collect coins2.mp3')
        sound.set_volume(0.7)
        sound.play()
        # self.coin_collection.play()

    def play_key_collection(self):
        sound = pygame.mixer.Sound('./assets/Audio/Find_key.mp3')
        sound.set_volume(0.7)
        sound.play()