import pygame


class GameSound(object):

    def __init__(self):
        pygame.mixer.init()
        # pygame.mixer.music.load('./assets/Audio/Magic Escape Room.mp3')
        # pygame.mixer.music.set_volume(0.5)
        # self.menu = pygame.mixer.Sound('./assets/Audio/game/menu.ogg')
        # self.menu.set_volume(1)
        # self.background1 = pygame.mixer.Sound('./assets/Audio/game/tower1.ogg')
        # self.background1.set_volume(0.8)
        # self.background2 = pygame.mixer.Sound('./assets/Audio/game/tower2.ogg')
        # self.background2.set_volume(0.8)
        # self.background3 = pygame.mixer.Sound('./assets/Audio/game/tower3.ogg')
        # self.background3.set_volume(0.8)
        self.menu = './assets/Audio/game/menu.ogg'
        self.background1 = './assets/Audio/game/tower1.ogg'
        self.background2 = './assets/Audio/game/tower2.ogg'
        self.background3 = './assets/Audio/game/tower3.ogg'

    def play_background(self, location):
        pygame.mixer.music.load(location)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def stop_background(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    # @staticmethod
    # def playbackgroundmusic():
    #     pygame.mixer.music.play(-1)

    # def play_insert_coin(self):
    #     sound = pygame.mixer.Sound('./assets/Audio/handleCoins.ogg')
    #     sound.set_volume(0.7)
    #     sound.play()
    #
    # def play_mode_select(self):
    #     sound = pygame.mixer.Sound('./assets/Audio/select_004.ogg')
    #     sound.set_volume(0.7)
    #     sound.play()
    #
    # def play_confirmation(self):
    #     sound = pygame.mixer.Sound('./assets/Audio/confirmation_004.ogg')
    #     sound.set_volume(0.7)
    #     sound.play()

    # def play_menu_sound(self):
    #     sound = pygame.mixer.Sound('./assets/Audio/horror_menu.ogg')
    #     sound.set_volume(0.7)
    #     sound.play(loops=-1)

class PlayerSound(object):

    def __init__(self):
        pygame.mixer.init()
        self.enemy_collision = pygame.mixer.Sound('./assets/Audio/player/enemy_collision.ogg')
        self.enemy_collision.set_volume(0.7)
        self.coin_collection = pygame.mixer.Sound('./assets/Audio/player/collect_coin.ogg')
        self.coin_collection.set_volume(0.7)
        self.key_collection = pygame.mixer.Sound('./assets/Audio/player/find_key.ogg')
        self.key_collection.set_volume(0.7)
        self.sword = pygame.mixer.Sound('./assets/Audio/player/sword.ogg')
        self.sword.set_volume(0.7)
        self.flamethrower = pygame.mixer.Sound('./assets/Audio/player/flamethrower.ogg')
        self.flamethrower.set_volume(0.7)
        self.die = pygame.mixer.Sound('./assets/Audio/player/die.ogg')
        self.die.set_volume(0.7)
        self.level_up = pygame.mixer.Sound('./assets/Audio/player/level_up.ogg')
        self.level_up.set_volume(0.7)
        self.revive = pygame.mixer.Sound('./assets/Audio/player/revive.ogg')
        self.revive.set_volume(0.7)
        self.trap = pygame.mixer.Sound('./assets/Audio/player/trap.ogg')
        self.trap.set_volume(0.7)
        self.special_item = pygame.mixer.Sound('./assets/Audio/player/special.ogg')
        self.special_item.set_volume(1)
        self.life_up = pygame.mixer.Sound('./assets/Audio/player/life_up.ogg')
        self.life_up.set_volume(0.7)


class EnemySound(object):

    def __init__(self):
        pygame.mixer.init()
        self.poof = pygame.mixer.Sound('./assets/Audio/enemy/poof.ogg')
        self.poof.set_volume(1)
        self.boss1_die = pygame.mixer.Sound('./assets/Audio/enemy/boss1_die.ogg')
        self.boss1_die.set_volume(0.7)
        self.boss2_die = pygame.mixer.Sound('./assets/Audio/enemy/boss2_die.ogg')
        self.boss2_die.set_volume(0.7)
        self.boss3_die = pygame.mixer.Sound('./assets/Audio/enemy/boss3_die.ogg')
        self.boss3_die.set_volume(0.7)
        self.boss1_attack = pygame.mixer.Sound('./assets/Audio/enemy/bite.ogg')
        self.boss1_attack.set_volume(0.7)
        self.boss2_attack = pygame.mixer.Sound('./assets/Audio/enemy/slap.ogg')
        self.boss2_attack.set_volume(0.7)
        self.boss3_attack = pygame.mixer.Sound('./assets/Audio/enemy/slash.ogg')
        self.boss3_attack.set_volume(0.7)
        self.hit = pygame.mixer.Sound('./assets/Audio/enemy/hit.ogg')
        self.hit.set_volume(0.4)


class TransitionSound(object):

    def __init__(self):
        pygame.mixer.init()
        self.player_move = pygame.mixer.Sound('./assets/Audio/transition/footstep07.ogg')
        self.player_move.set_volume(0.1)
        self.typing = pygame.mixer.Sound('./assets/Audio/transition/typing.ogg')
        self.typing.set_volume(0.1)
        self.appear = pygame.mixer.Sound('./assets/Audio/transition/appear.ogg')
        self.appear.set_volume(0.3)

class MenuSound(object):

    def __init__(self):
        pygame.mixer.init()
        self.menu = pygame.mixer.Sound('./assets/Audio/menu/horror_menu.ogg')
        self.menu.set_volume(0.8)
        self.insert_coin = pygame.mixer.Sound('./assets/Audio/menu/handleCoins.ogg')
        self.insert_coin.set_volume(0.8)
        self.select = pygame.mixer.Sound('./assets/Audio/menu/select_004.ogg')
        self.select.set_volume(0.8)
        self.confirm = pygame.mixer.Sound('./assets/Audio/menu/confirmation_004.ogg')
        self.confirm.set_volume(0.8)
