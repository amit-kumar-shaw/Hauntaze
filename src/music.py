import pygame


class GameSound(object):

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./assets/Audio/Magic Escape Room.mp3')
        pygame.mixer.music.set_volume(0.5)
        # sound = pygame.mixer.Sound('./assets/Audio/insert_coin.mp3')

    @staticmethod
    def playbackgroundmusic():
        pygame.mixer.music.play(-1)

    def play_insert_coin(self):
        sound = pygame.mixer.Sound('./assets/Audio/handleCoins.ogg')
        sound.set_volume(0.7)
        sound.play()


class PlayerSound(object):

    def __init__(self):
        pygame.mixer.init()
        # pygame.mixer.music.load('./assets/Audio/Magic Escape Room.mp3')
        # pygame.mixer.music.set_volume(0.5)
        # sound = pygame.mixer.Sound('./assets/Audio/doorOpen_4.mp3')
        # self.coin_collection = pygame.mixer.Sound('./assets/Audio/collect coins2.mp3')
        # self.coin_collection.set_volume(0.7)
        # self.enemy_collision = pygame.mixer.Sound('./assets/Audio/Find_key.mp3')
        # self.enemy_collision.set_volume(0.7)

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

