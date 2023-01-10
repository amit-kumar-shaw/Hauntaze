import pygame


class GameSound(object):

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./assets/Audio/Magic Escape Room.mp3')
        pygame.mixer.music.set_volume(0.5)
        self.menu = pygame.mixer.Sound('./assets/Audio/horror_menu.ogg')
        self.menu.set_volume(0.8)

    @staticmethod
    def playbackgroundmusic():
        pygame.mixer.music.play(-1)

    def play_insert_coin(self):
        sound = pygame.mixer.Sound('./assets/Audio/handleCoins.ogg')
        sound.set_volume(0.7)
        sound.play()

    def play_mode_select(self):
        sound = pygame.mixer.Sound('./assets/Audio/select_004.ogg')
        sound.set_volume(0.7)
        sound.play()

    def play_confirmation(self):
        sound = pygame.mixer.Sound('./assets/Audio/confirmation_004.ogg')
        sound.set_volume(0.7)
        sound.play()

    # def play_menu_sound(self):
    #     sound = pygame.mixer.Sound('./assets/Audio/horror_menu.ogg')
    #     sound.set_volume(0.7)
    #     sound.play(loops=-1)

class PlayerSound(object):

    def __init__(self):
        pygame.mixer.init()
        self.enemy_collision = pygame.mixer.Sound('./assets/Audio/enemy_collision.mp3')
        self.enemy_collision.set_volume(0.7)
        self.coin_collection = pygame.mixer.Sound('./assets/Audio/enemy_collision.mp3')
        self.coin_collection.set_volume(0.7)
        self.key_collection = pygame.mixer.Sound('./assets/Audio/enemy_collision.mp3')
        self.key_collection.set_volume(0.7)
        self.sword = pygame.mixer.Sound('./assets/Audio/player/sword.ogg')
        self.sword.set_volume(0.7)
        self.flamethrower = pygame.mixer.Sound('./assets/Audio/player/flamethrower.ogg')
        self.flamethrower.set_volume(0.7)

    def play_enemy_collision(self):
        sound = pygame.mixer.Sound('./assets/Audio/enemy_collision.mp3')
        sound.set_volume(0.7)
        sound.play()
        # self.enemy_collision.play()

    def play_coin_collection(self):
        sound = pygame.mixer.Sound('./assets/Audio/collect_coin.ogg')
        sound.set_volume(0.7)
        sound.play()
        # self.coin_collection.play()

    def play_key_collection(self):
        sound = pygame.mixer.Sound('./assets/Audio/Find_key.mp3')
        sound.set_volume(0.7)
        sound.play()


class EnemySound(object):

    def __init__(self):
        pygame.mixer.init()
        self.poof = pygame.mixer.Sound('./assets/Audio/enemy/poof.ogg')
        self.poof.set_volume(0.7)


class TransitionSound(object):

    def __init__(self):
        pygame.mixer.init()
        self.player_move = pygame.mixer.Sound('./assets/Audio/footstep07.ogg')
        self.player_move.set_volume(0.1)
        self.typing = pygame.mixer.Sound('./assets/Audio/typing.ogg')
        self.typing.set_volume(0.1)
        self.appear = pygame.mixer.Sound('./assets/Audio/appear.ogg')
        self.appear.set_volume(0.3)

class MenuSound(object):

    def __init__(self):
        pygame.mixer.init()
        self.menu = pygame.mixer.Sound('./assets/Audio/horror_menu.ogg')
        self.menu.set_volume(0.8)
        self.insert_coin = pygame.mixer.Sound('./assets/Audio/handleCoins.ogg')
        self.insert_coin.set_volume(0.8)
        self.select = pygame.mixer.Sound('./assets/Audio/select_004.ogg')
        self.select.set_volume(0.8)
        self.confirm = pygame.mixer.Sound('./assets/Audio/confirmation_004.ogg')
        self.confirm.set_volume(0.8)
