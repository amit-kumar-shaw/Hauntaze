import math
import random
import sys
import pygame
import map_generator
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from traps import Spike
from enemy_boss import Boss
from collectible import Collectible
from key import Key
from door import Door
from weapon import Weapon
from sounds import GameSound
from player_ghost import Ghost


class Level:
    """ run complete playing logic """

    def __init__(self, story_mode, player1_active, player1, player2_active, player2, level, multiplayer=False,
                 joystick_1=None, joystick_2=None):

        self.joystick_1 = joystick_1
        self.joystick_2 = joystick_2

        self.screen = pygame.display.get_surface()

        self.completed = False
        self.failed = False

        self.animation_index = 0

        self.story_mode = story_mode
        self.current_level = level
        self.multiplayer = multiplayer

        self.death_stone_activated = False

        self.is_boss_level = False
        self.boss = None

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.trap_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.key1_sprite = pygame.sprite.GroupSingle()
        self.key2_sprite = pygame.sprite.GroupSingle()
        self.door1_sprite = pygame.sprite.GroupSingle()
        self.door2_sprite = pygame.sprite.GroupSingle()
        self.weapon_sprite = pygame.sprite.Group()
        self.weapon1_sprite = pygame.sprite.GroupSingle()
        self.weapon2_sprite = pygame.sprite.GroupSingle()

        self.level_width = SCREEN_WIDTH if not story_mode else 576

        # create level surface
        self.level_window = pygame.Surface((self.level_width, (ROWS * CELL_SIZE * TILE_HEIGHT)))

        # create cover surface for limited visibility
        self.cover_surf = pygame.Surface((self.level_width, (ROWS * CELL_SIZE * TILE_HEIGHT)),
                                         pygame.SRCALPHA).convert_alpha()
        self.cover_surf.fill(COVER_COLOR)
        self.cover_surf.set_colorkey((255, 255, 255))

        # create map surface
        self.map_surf = pygame.Surface((self.level_width, (ROWS * CELL_SIZE * TILE_HEIGHT)))

        # create cropped surfaces for players and ghost
        self.cropped_surf1 = pygame.Surface((VISIBILITY_RADIUS * 2, VISIBILITY_RADIUS * 2))
        self.cropped_surf2 = pygame.Surface((VISIBILITY_RADIUS * 2, VISIBILITY_RADIUS * 2))
        self.cropped_surf3 = pygame.Surface((GHOST_VISIBILITY * 2, GHOST_VISIBILITY * 2))
        self.cropped_rect1 = self.cropped_surf1.get_rect()
        self.cropped_rect2 = self.cropped_surf2.get_rect()
        self.cropped_rect3 = self.cropped_surf3.get_rect()

        self.player1_active = player1_active
        self.player2_active = player2_active
        self.player1 = player1
        self.player2 = player2

        self.coins = []
        self.enemies = []

        # Ghost
        self.ghost_active = False
        self.ghost = None

        self.sound = GameSound()
        self.background_music_on = False
        self.background_music = None
        self.continue_text = pygame.image.load("./assets/images/transitions/continue.png").convert_alpha()
        self.exit = pygame.image.load("./assets/images/transitions/exit.png").convert_alpha()
        self.main_menu = pygame.image.load("./assets/images/menu/main_menu.png").convert_alpha()

        # setup level based on game mode
        if story_mode:
            self.story_setup()
        else:
            self.survival_setup()

    def survival_setup(self):
        """ setup survival mode level """

        # fetch survival mode data
        from level_design import SURVIVAL_DATA
        data = SURVIVAL_DATA[self.current_level - 1]

        coins = data['coins'] if not self.multiplayer else data['coins'] * 2
        need_coins = False
        personal_items = 3 if not self.multiplayer else 6
        need_personal_item = False
        personal_cells = []
        bats = data['bats']
        slime = data['slime']
        skull = data['skull']
        enemies = bats + slime + skull
        need_enemy = False
        enemy_type = None
        torch = data['torch']
        need_torch = False
        mask = data['mask']
        need_mask = False
        web = data['web']
        need_web = False
        web1 = False
        spikes = data['spikes']
        need_spikes = False

        # auto generate random map
        level_map, player_cells, other_cells = map_generator.generate(COLUMNS, ROWS, CELL_SIZE)

        # lay out walls and floors
        for col_index in range(ROWS * CELL_SIZE):
            for row_index in range(COLUMNS * CELL_SIZE):
                y = col_index * TILE_HEIGHT
                x = row_index * TILE_WIDTH
                if level_map[(row_index, col_index)] == '.':
                    Tile((x, y), [self.visible_sprites], self.current_level, wall=False)
                if level_map[(row_index, col_index)] == '#':
                    Tile((x, y), [self.visible_sprites, self.collision_sprites], self.current_level, wall=True)
                if level_map[(row_index, col_index)] == 'A':
                    Tile((x, y), [self.visible_sprites], self.current_level, wall=False)
                if level_map[(row_index, col_index)] == 'B':
                    Tile((x, y), [self.visible_sprites], self.current_level, wall=False)

        # draw tiles on map surface
        self.visible_sprites.draw(self.map_surf)

        other_cells = random.sample(other_cells, 30)

        personal_index = None
        coin_index = None
        enemy_index = None
        torch_index = None
        mask_index = None
        web_index = None
        spike_index = None

        # randomly select cells for each item
        for index, cell in enumerate(other_cells):
            items = 0
            if personal_items != 0 and index % int(30 / personal_items) == 0:
                need_personal_item = True
                personal_index = items
                items += 1
            if coins != 0 and index % int(30 / coins) == 0:
                need_coins = True
                coin_index = items
                items += 1
            if enemies != 0 and index % int(30 / enemies) == 0:
                need_enemy = True
                enemy_index = items
                items += 1
                if bats != 0:
                    enemy_type = 'bat'
                    bats -= 1
                elif slime != 0:
                    enemy_type = 'slime'
                    slime -= 1
                elif skull != 0:
                    enemy_type = 'skull'
                    skull -= 1
            if torch != 0 and index % int(30 / torch) == 0:
                need_torch = True
                torch_index = items
                items += 1
            if mask != 0 and index % int(30 / mask) == 0:
                need_mask = True
                mask_index = items
                items += 1
            if web != 0 and index % int(30 / web) == 0:
                need_web = True
                web_index = items
                items += 1
                web1 = not web1
            if spikes != 0 and index % int(30 / spikes) == 0:
                need_spikes = True
                spike_index = items
                items += 1

            cells = random.sample(list(cell.room), items)
            if need_personal_item:
                need_personal_item = False
                personal_cells.append(cells[personal_index])
            if need_coins:
                need_coins = False
                self.coins.append(
                    Collectible(tuple(TILE_SIZE * x for x in cells[coin_index]),
                                [self.visible_sprites, self.collectible_sprites],
                                type='coin'))
            if need_enemy:
                need_enemy = False
                self.enemies.append(
                    Enemy(tuple(TILE_SIZE * x for x in cells[enemy_index]),
                          [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                          self.collision_sprites, self.weapon_sprite, type=enemy_type))
            if need_torch:
                need_torch = False
                Collectible(tuple(TILE_SIZE * x for x in cells[torch_index]),
                            [self.visible_sprites, self.collectible_sprites],
                            type='torch')
            if need_mask:
                need_mask = False
                Collectible(tuple(TILE_SIZE * x for x in cells[mask_index]),
                            [self.visible_sprites, self.collectible_sprites],
                            type='mask2')
            if need_web:
                need_web = False
                Collectible(tuple(TILE_SIZE * x for x in cells[web_index]),
                            [self.visible_sprites, self.collectible_sprites],
                            type='web1' if web1 else 'web2')
            if need_spikes:
                need_spikes = False
                Spike(tuple(TILE_SIZE * x for x in cells[spike_index]),
                      [self.visible_sprites, self.trap_sprites])

        # update some properties, key, door, and weapon for player 1
        if self.player1_active:
            self.player1.rect.topleft = tuple(TILE_SIZE * x for x in player_cells[0])
            self.player1.attach_torch()
            self.player1.collision_sprites = self.collision_sprites
            self.player1.collectible_sprites = self.collectible_sprites
            self.player1.enemy_sprites = self.enemy_sprites
            self.player1.trap_sprites = self.trap_sprites

            self.player1.key = Key(tuple(TILE_SIZE * x for x in personal_cells[0]), self.key1_sprite)
            self.player1.door = Door(tuple(TILE_SIZE * x for x in personal_cells[1]), self.door1_sprite)
            if data['weapon_type'] is not None:
                self.player1.weapon = Weapon(tuple(TILE_SIZE * x for x in personal_cells[2]),
                                             [self.weapon_sprite, self.weapon1_sprite], self.collision_sprites,
                                             type=data['weapon_type'])

        # update some properties, key, door, and weapon for player 2
        if self.player2_active:
            self.player2.rect.topleft = tuple(TILE_SIZE * x for x in player_cells[1])
            self.player2.attach_torch()
            self.player2.collision_sprites = self.collision_sprites
            self.player2.collectible_sprites = self.collectible_sprites
            self.player2.enemy_sprites = self.enemy_sprites
            self.player2.trap_sprites = self.trap_sprites

            self.player2.key = Key(tuple(TILE_SIZE * x for x in personal_cells[3]), self.key2_sprite)
            self.player2.door = Door(tuple(TILE_SIZE * x for x in personal_cells[4]), self.door2_sprite)
            if data['weapon_type'] is not None:
                self.player2.weapon = Weapon(tuple(TILE_SIZE * x for x in personal_cells[5]),
                                             [self.weapon_sprite, self.weapon1_sprite], self.collision_sprites,
                                             type=data['weapon_type'])

        # set background music
        if self.current_level <= 15:
            self.background_music = self.sound.background1
        elif 15 < self.current_level <= 35:
            self.background_music = self.sound.background2
        elif 35 < self.current_level <= 50:
            self.background_music = self.sound.background3

    def story_setup(self):
        """ setup story mode for the level"""

        from level_design import STORY_DATA

        # load level data
        data = STORY_DATA[self.current_level - 1]

        # set background music
        if self.current_level <= 5:
            self.background_music = self.sound.background1
        elif 5 < self.current_level <= 10:
            self.background_music = self.sound.background2
        elif 10 < self.current_level <= 15:
            self.background_music = self.sound.background3

        # check if it's a boss level
        if self.current_level % 5 == 0:
            self.is_boss_level = True

        # get the hint to display on UI
        self.caption = data['caption']

        # get the map
        level_map = data['map']

        # lay out walls and floors
        for row_index, row in enumerate(level_map):
            for col_index, col in enumerate(row):
                x = col_index * 16
                y = row_index * 16
                if col == '#':
                    Tile((x, y), [self.visible_sprites, self.collision_sprites], self.current_level, wall=True,
                         storymode=True)
                else:
                    Tile((x, y), [self.visible_sprites], self.current_level, wall=False, storymode=True)

        # draw the walls and floors on map surface
        self.visible_sprites.draw(self.map_surf)

        # update some properties, key, door, and weapon for player 1
        if self.player1_active:
            self.player1.rect.topleft = tuple(TILE_SIZE * x for x in data['player1'])
            self.player1.revival_position = self.player1.rect.topleft
            self.player1.attach_torch()
            self.player1.collision_sprites = self.collision_sprites
            self.player1.collectible_sprites = self.collectible_sprites
            self.player1.enemy_sprites = self.enemy_sprites
            self.player1.trap_sprites = self.trap_sprites
            if self.is_boss_level:
                self.player1.key_active = False

            self.player1.key = Key(tuple(TILE_SIZE * x for x in data['key1']), self.key1_sprite)
            self.player1.door = Door(tuple(TILE_SIZE * x for x in data['door1']), self.door1_sprite)
            if len(data['weapon1']):
                self.player1.weapon = Weapon(tuple(TILE_SIZE * x for x in data['weapon1']),
                                             [self.weapon_sprite, self.weapon1_sprite], self.collision_sprites,
                                             type=data['weapon_type'])

            torch_cells = data['torch1']
            for _, cell in enumerate(torch_cells):
                Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                            type='torch')

        # update some properties, key, door, and weapon for player 2
        if self.player2_active:
            self.player2.rect.topleft = tuple(TILE_SIZE * x for x in data['player2'])
            self.player2.revival_position = self.player2.rect.topleft
            self.player2.attach_torch()
            self.player2.collision_sprites = self.collision_sprites
            self.player2.collectible_sprites = self.collectible_sprites
            self.player2.enemy_sprites = self.enemy_sprites
            self.player2.trap_sprites = self.trap_sprites
            if self.is_boss_level:
                self.player2.key_active = False

            self.player2.key = Key(tuple(TILE_SIZE * x for x in data['key2']), self.key2_sprite)
            self.player2.door = Door(tuple(TILE_SIZE * x for x in data['door2']), self.door2_sprite)
            if len(data['weapon2']):
                self.player2.weapon = Weapon(tuple(TILE_SIZE * x for x in data['weapon2']),
                                             [self.weapon_sprite, self.weapon2_sprite], self.collision_sprites,
                                             type=data['weapon_type'])

            torch_cells = data['torch2']
            for _, cell in enumerate(torch_cells):
                Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                            type='torch')

        web_cells = data['web1']
        for _, cell in enumerate(web_cells):
            Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                        type='web1')
        web_cells = data['web2']
        for _, cell in enumerate(web_cells):
            Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                        type='web2')

        mask_cells = data['mask1']
        for _, cell in enumerate(mask_cells):
            Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                        type='mask1')
        mask_cells = data['mask2']
        for _, cell in enumerate(mask_cells):
            Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                        type='mask2')

        if self.player1_active:
            coin_cells = data['coins1']
            for _, cell in enumerate(coin_cells):
                self.coins.append(
                    Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                                type='coin'))
        if self.player2_active:
            coin_cells = data['coins2']
            for _, cell in enumerate(coin_cells):
                self.coins.append(
                    Collectible(tuple(TILE_SIZE * x for x in cell), [self.visible_sprites, self.collectible_sprites],
                                type='coin'))

        spike_cells = data['spikes']
        for _, cell in enumerate(spike_cells):
            Spike(tuple(TILE_SIZE * x for x in cell),
                  [self.visible_sprites, self.trap_sprites])

        # draw enemies
        bat_cells = data['bats']
        for _, cell in enumerate(bat_cells):
            self.enemies.append(
                Enemy(tuple(TILE_SIZE * x for x in cell),
                      [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                      self.collision_sprites, self.weapon_sprite, type='bat'))

        slime_cells = data['slime']
        for _, cell in enumerate(slime_cells):
            self.enemies.append(
                Enemy(tuple(TILE_SIZE * x for x in cell),
                      [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                      self.collision_sprites, self.weapon_sprite, type='slime'))

        skull_cells = data['skull']
        for _, cell in enumerate(skull_cells):
            self.enemies.append(
                Enemy(tuple(TILE_SIZE * x for x in cell),
                      [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                      self.collision_sprites, self.weapon_sprite, type='skull'))

        # instantiate boss if boss level
        if self.is_boss_level:
            if self.current_level == 5:
                self.boss = Boss(tuple(TILE_SIZE * x for x in data['boss']),
                                 [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                                 self.collision_sprites, self.weapon_sprite, type='boss1')
            elif self.current_level == 10:
                self.boss = Boss(tuple(TILE_SIZE * x for x in data['boss']),
                                 [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                                 self.collision_sprites, self.weapon_sprite, type='boss2')
            elif self.current_level == 15:
                self.boss = Boss(tuple(TILE_SIZE * x for x in data['boss']),
                                 [self.visible_sprites, self.active_sprites, self.enemy_sprites],
                                 self.collision_sprites, self.weapon_sprite, type='boss3')

            # double boss life in multiplayer
            if self.multiplayer:
                self.boss.lives *= 2
                self.boss.MAX_LIVES = self.boss.lives

    def run(self):
        """ run the level logic"""

        # start background music
        if not self.background_music_on:
            self.sound.play_background(self.background_music)
            self.background_music_on = True

        # update the active sprites
        self.active_sprites.update()

        if self.player1_active:
            PLAYER1_SPRITE.update()

        if self.player2_active:
            PLAYER2_SPRITE.update()

        # draw visible region and enemy indicator
        self.draw_visible_region()

        # draw visible map surface for player 1
        if self.player1_active:
            if self.player1.visibility_radius != VISIBILITY_RADIUS or self.cropped_rect1.width != self.player1.visibility_radius * 2:
                self.cropped_surf1 = pygame.Surface(
                    (self.player1.visibility_radius * 2, self.player1.visibility_radius * 2))
            self.cropped_rect1 = self.cropped_surf1.get_rect(center=self.player1.torch.rect.center)
            self.level_window.blit(self.map_surf, self.cropped_rect1, self.cropped_rect1)

        # draw visible map surface for player 2
        if self.player2_active:
            if self.player2.visibility_radius != VISIBILITY_RADIUS or self.cropped_rect2.width != self.player2.visibility_radius * 2:
                self.cropped_surf2 = pygame.Surface(
                    (self.player2.visibility_radius * 2, self.player2.visibility_radius * 2))
            self.cropped_rect2 = self.cropped_surf2.get_rect(center=self.player2.torch.rect.center)
            self.level_window.blit(self.map_surf, self.cropped_rect2, self.cropped_rect2)

        # draw visible map surface for ghost
        if self.ghost_active:
            if self.story_mode:
                self.cropped_rect3 = self.cropped_surf3.get_rect(center=self.ghost.rect.center)
                self.level_window.blit(self.map_surf, self.cropped_rect3, self.cropped_rect3)

        # draw transparent cover surface
        if self.player1_active:
            self.level_window.blit(self.cover_surf, self.cropped_rect1, self.cropped_rect1)
        if self.player2_active:
            self.level_window.blit(self.cover_surf, self.cropped_rect2, self.cropped_rect2)
        if self.ghost_active and self.story_mode:
            self.level_window.blit(self.cover_surf, self.cropped_rect3, self.cropped_rect3)

        # update collectible sprites
        self.collectible_sprites.update()

        # draw collectible sprites when in visible region
        for sprite in self.collectible_sprites.sprites():
            if (self.player1_active and self.cropped_rect1.contains(sprite)) or (
                    self.player2_active and self.cropped_rect2.contains(sprite)):
                sprite.draw(self.level_window)

        self.trap_sprites.update()

        # draw spikes when in visible region
        for sprite in self.trap_sprites.sprites():
            if (self.player1_active and self.cropped_rect1.contains(sprite)) or (
                    self.player2_active and self.cropped_rect2.contains(sprite)):
                sprite.draw(self.level_window)

        # keys are with boss in boss level
        if self.is_boss_level:
            if self.player1_active:
                self.player1.key.rect = self.player1.key.image.get_rect(midright=self.boss.rect.midtop)
            if self.player2_active:
                self.player2.key.rect = self.player2.key.image.get_rect(midleft=self.boss.rect.midtop)

        # draw key if the player is nearby
        if self.player1_active and math.dist(self.player1.torch.rect.center,
                                             self.player1.key.rect.center) < self.player1.visibility_radius:
            self.key1_sprite.draw(self.level_window)
            self.player1.key.animate()

        if self.player2_active and math.dist(self.player2.torch.rect.center,
                                             self.player2.key.rect.center) < self.player2.visibility_radius:
            self.key2_sprite.draw(self.level_window)
            self.player2.key.animate()

        # draw door if the player is nearby
        if self.player1_active and math.dist(self.player1.torch.rect.center,
                                             self.player1.door.rect.center) < self.player1.visibility_radius:
            self.door1_sprite.draw(self.level_window)

        if self.player2_active and math.dist(self.player2.torch.rect.center,
                                             self.player2.door.rect.center) < self.player2.visibility_radius:
            self.door2_sprite.draw(self.level_window)

        # draw weapon if the player is nearby
        if self.player1_active and self.player1.weapon is not None and math.dist(self.player1.torch.rect.center,
                                                                                 self.player1.weapon.rect.center) < self.player1.visibility_radius:
            self.weapon1_sprite.draw(self.level_window)

        if self.player2_active and self.player2.weapon is not None and math.dist(self.player2.torch.rect.center,
                                                                                 self.player2.weapon.rect.center) < self.player2.visibility_radius:
            self.weapon2_sprite.draw(self.level_window)

        # open door if key collected
        if (self.player1_active and self.player1.key_picked) and not self.player1.door.isOpen:
            self.player1.door.open()
            self.door1_sprite.draw(self.level_window)

        if (self.player2_active and self.player2.key_picked) and not self.player2.door.isOpen:
            self.player2.door.open()
            self.door2_sprite.draw(self.level_window)

        # draw Enemy sprites
        for sprite in self.enemy_sprites.sprites():
            if (self.player1_active and self.cropped_rect1.colliderect(sprite)) or (
                    self.player2_active and self.cropped_rect2.colliderect(sprite)) or (
                    self.ghost_active and self.cropped_rect3.colliderect(sprite)):
                sprite.draw(self.level_window)

        # draw player 1
        if self.player1_active and self.player1.visibility_radius > 1:

            self.level_window.blit(self.player1.torch.image, self.player1.torch.rect)
            if self.player1.weapon_active:
                self.level_window.blit(self.player1.weapon.image, self.player1.weapon.rect)
            PLAYER1_SPRITE.draw(self.level_window)

            # draw web on play if collide with web
            if self.player1.is_slow:
                rect = self.player1.web.get_rect(midtop=self.player1.rect.midtop)
                self.level_window.blit(self.player1.web, rect)

        # draw player 2
        if self.player2_active and self.player2.visibility_radius > 1:

            self.level_window.blit(self.player2.torch.image, self.player2.torch.rect)
            if self.player2.weapon_active:
                self.level_window.blit(self.player2.weapon.image, self.player2.weapon.rect)
            PLAYER2_SPRITE.draw(self.level_window)

            # draw web on play if collide with web
            if self.player2.is_slow:
                rect = self.player2.web.get_rect(midtop=self.player2.rect.midtop)
                self.level_window.blit(self.player2.web, rect)

        # draw revival timer
        if self.player1_active and self.player1.wait_revival:
            self.level_window.blit(self.player1.timer, self.player1.timer_rect)
        if self.player2_active and self.player2.wait_revival:
            self.level_window.blit(self.player2.timer, self.player2.timer_rect)

        # Ghost update
        if self.ghost_active:
            self.ghost.update()
            # draw smoke in survival mode
            if not self.story_mode and self.ghost.visibility_radius > 2:
                self.level_window.blit(self.ghost.smoke.image, self.ghost.smoke.rect)

            if self.ghost.visibility_radius > 2:
                self.level_window.blit(self.ghost.image, self.ghost.rect)

        # Activate Death Stone
        if self.story_mode:
            if self.player1_active and self.player1.death_stone_available and self.player1.death_stone_activated:
                self.kill_all_enemies()
                self.player1.death_stone_activated = False
                self.player1.death_stone_available = False
                if self.player2_active:
                    self.player2.death_stone_activated = False
                    self.player2.death_stone_available = False
            if self.player2_active and self.player2.death_stone_available and self.player2.death_stone_activated:
                self.kill_all_enemies()
                self.player2.death_stone_activated = False
                self.player2.death_stone_available = False
                if self.player1_active:
                    self.player1.death_stone_activated = False
                    self.player1.death_stone_available = False

        self.cover_surf.fill(COVER_COLOR)

        # display game over
        if ((not self.player1_active) and
                (not self.player2_active)):
            self.game_over()

        # level completed msg
        if self.player1_active and self.player1.level_completed and not self.player2_active:
            self.level_completed()

        if self.player2_active and self.player2.level_completed and not self.player1_active:
            self.level_completed()

        if self.player1_active and self.player1.level_completed and self.player2_active and self.player2.level_completed:
            self.level_completed()

        self.check_player_status()

        self.screen.blit(self.level_window, (0, 0))
        self.level_window.fill('black')

    def kill_all_enemies(self):
        """ kill all enemies when death stone activated in story mode """
        self.death_stone_activated = True
        for sprite in self.enemy_sprites.sprites():
            if sprite.type == 'bat' or sprite.type == 'slime' or sprite.type == 'skull':
                sprite.status = 'dead'
                sprite.animation_index = 0

    def check_player_status(self):
        """ check if player is alive and instantiate ghost in multiplayer """

        if self.player1_active and not self.player1.is_alive:
            self.player1_active = False
            if not self.ghost_active and self.multiplayer:
                self.ghost = Ghost(self.player1.rect.topleft, self.story_mode, player2=False, joystick=self.joystick_1)
                self.ghost.partner = self.player2
                self.ghost_active = True
        if self.player2_active and not self.player2.is_alive:
            self.player2_active = False
            if not self.ghost_active and self.multiplayer:
                self.ghost = Ghost(self.player2.rect.topleft, self.story_mode, player2=True, joystick=self.joystick_2)
                self.ghost.partner = self.player1
                self.ghost_active = True

        if self.player1_active and self.player1.is_ghost and not self.ghost_active and self.multiplayer:
            self.ghost = Ghost(self.player1.rect.topleft, self.story_mode, player2=False, joystick=self.joystick_1)
            self.ghost.partner = self.player2
            self.ghost_active = True
        if self.player2_active and self.player2.is_ghost and not self.ghost_active and self.multiplayer:
            self.ghost = Ghost(self.player2.rect.topleft, self.story_mode, player2=True, joystick=self.joystick_2)
            self.ghost.partner = self.player1
            self.ghost_active = True

        if self.is_boss_level:
            self.boss.player1_active = self.player1_active
            self.boss.player2_active = self.player2_active

    def draw_visible_region(self):
        """ draw player visible region and enemy indicator"""

        for i in range(0, 5):
            if self.player1_active:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50 * i)),
                                   (self.player1.torch.rect.centerx, self.player1.torch.rect.centery),
                                   self.player1.visibility_radius * float(1 - (i * i) / 100))
            if self.player2_active:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50 * i)),
                                   (self.player2.torch.rect.centerx, self.player2.torch.rect.centery),
                                   self.player2.visibility_radius * float(1 - (i * i) / 100))
            if self.ghost_active and self.story_mode:
                pygame.draw.circle(self.cover_surf, (0, 0, 0, 200 - (50 * i)),
                                   (self.ghost.rect.centerx, self.ghost.rect.centery),
                                   self.ghost.visibility_radius * float(1 - (i * i) / 100))

        # draw enemy indicator
        for enemy in self.enemy_sprites:

            # display enemy dying animation when death stone activated
            if self.death_stone_activated and enemy.status == 'dead':
                enemy.draw(self.level_window)

            else:
                if (self.player1_active and math.dist(self.player1.torch.rect.center,
                                                      enemy.rect.center) > self.player1.visibility_radius) and not self.player2_active:
                    pygame.draw.circle(self.level_window, 'red', enemy.rect.center, 1)
                if (self.player2_active and math.dist(self.player2.torch.rect.center,
                                                      enemy.rect.center) > self.player2.visibility_radius) and not self.player1_active:
                    pygame.draw.circle(self.level_window, 'red', enemy.rect.center, 1)
                if (self.player1_active and math.dist(self.player1.torch.rect.center,
                                                      enemy.rect.center) > self.player1.visibility_radius) and (
                        self.player2_active and math.dist(self.player2.torch.rect.center,
                                                          enemy.rect.center) > self.player2.visibility_radius):
                    pygame.draw.circle(self.level_window, 'red', enemy.rect.center, 1)

    def game_over(self):
        """ show game over screen """

        # stop background music
        if self.background_music_on:
            self.sound.stop_background()
            self.background_music_on = False

        keys = pygame.key.get_pressed()
        if keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (
                self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON)):
            self.failed = True
        self.animation_index += 0.08

        if self.animation_index >= 2:
            self.animation_index = 0

        msg = 'Game Over'

        # decide winner in survival mode multiplayer
        if not self.story_mode and self.multiplayer:
            msg = 'Player 1 Wins' if self.ghost.player2 else 'Player 2 Wins'

        # title
        font = pygame.font.Font('./assets/fonts/retro_gaming.ttf', 40 + int(self.animation_index))
        title = font.render(msg, False, 'yellow')
        title_rect = title.get_rect(midbottom=(self.level_width // 2 + 1, SCREEN_HEIGHT // 2 + 1))
        self.level_window.blit(title, title_rect)

        title = font.render(msg, False, 'red')
        title_rect = title.get_rect(midbottom=(self.level_width // 2, SCREEN_HEIGHT // 2))
        self.level_window.blit(title, title_rect)

        # Main menu button
        msg_rect = self.main_menu.get_rect(center=(self.level_width // 2, SCREEN_HEIGHT - 100))
        self.level_window.blit(self.main_menu, msg_rect)

    def level_completed(self):
        """ level completed screen"""

        # stop background music
        if self.background_music_on:
            self.sound.stop_background()
            self.background_music_on = False

        self.animation_index += 0.08

        if self.animation_index >= 2: self.animation_index = 0

        msg = 'Level Completed'

        if not self.story_mode and self.current_level == LAST_SURVIVAL_LEVEL:
            msg = 'Congratulations'

        # title
        font = pygame.font.Font('./assets/fonts/retro_gaming.ttf', 40 + int(self.animation_index))
        title = font.render(msg, False, 'red')
        title_rect = title.get_rect(midbottom=(self.level_width // 2 + 1, SCREEN_HEIGHT // 2 + 1))
        self.level_window.blit(title, title_rect)

        title = font.render(msg, False, 'yellow')
        title_rect = title.get_rect(midbottom=(self.level_width // 2, SCREEN_HEIGHT // 2))
        self.level_window.blit(title, title_rect)

        button = self.continue_text

        # Winning Msg
        if not self.story_mode and self.current_level == LAST_SURVIVAL_LEVEL:
            font = pygame.font.Font('./assets/fonts/retro_gaming.ttf', 16)
            resume_msg = font.render('You have completed Hauntaze Survival Mode', False, 'white')
            msg_rect = resume_msg.get_rect(center=(self.level_width // 2, SCREEN_HEIGHT - 140))
            self.level_window.blit(resume_msg, msg_rect)

            button = self.exit

        msg_rect = button.get_rect(center=(self.level_width // 2, SCREEN_HEIGHT - 100))
        self.level_window.blit(button, msg_rect)

        keys = pygame.key.get_pressed()
        if keys[CONFIRM] or (self.joystick_1 is not None and self.joystick_1.get_button(START_BUTTON)) or (
                self.joystick_2 is not None and self.joystick_2.get_button(START_BUTTON)):
            self.completed = True
            self.level_window.fill('black')

            # exit the game if completed survival mode
            if not self.story_mode and self.current_level == LAST_SURVIVAL_LEVEL:
                pygame.quit()
                sys.exit()
