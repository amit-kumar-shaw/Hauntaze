import math
from settings import *
from utilities import import_frames

class Eye(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites, player_weapon_sprites):
        super().__init__(groups)

        path = f'./assets/images/enemy/eye/'
        self.frames = {'fly': [], 'attack': [], 'hit': [], 'dead': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=0.8)

        self.animation_index = 0
        self.status = 'fly'

        self.image = self.frames[self.status][self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2()
        self.direction.x = 1
        self.speed = 1
        self.tog = True
        self.collision_sprites = collision_sprites
        self.player_weapon_sprites = player_weapon_sprites

        self.player1_active = False
        self.player2_active = False

        self.target = None
        self.attack_end_time = 0

        self.lives = 5

        self.timer = 5
        self.movement_update()


    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                self.movement_update()

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                self.movement_update()

    def movement_update(self):

        self.direction.x *= -1


    def animate(self):

        status = self.frames[self.status]

        # loop over frame index
        self.animation_index += 0.07
        if self.animation_index >= len(status):
            self.animation_index = 0
            if self.status == 'attack':
                self.attack_end_time = pygame.time.get_ticks()
            self.status = 'fly'

        self.image = status[int(self.animation_index)]
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)

    def weapon_collisions(self):
        for sprite in self.player_weapon_sprites.sprites():
            if sprite.rect.colliderect(self.rect) and sprite.status == 'attack' and self.status == 'fly':
                if pygame.sprite.collide_mask(self, sprite):
                    self.lives -= 1
                    self.status = 'hit'
                    self.movement_update()
                    self.animation_index = 0
                    if self.lives == 0:
                        self.kill()
                        if self.player1_active:
                            PLAYER1_SPRITE.sprite.key_active = True
                        if self.player2_active:
                            PLAYER2_SPRITE.sprite.key_active = True

    def player_nearby(self):
        if self.player1_active and math.dist(PLAYER1_SPRITE.sprite.rect.center, self.rect.center) < 30:
            self.target = PLAYER1_SPRITE.sprite
            return True
        if self.player2_active and math.dist(PLAYER2_SPRITE.sprite.rect.center, self.rect.center) < 30:
            self.target = PLAYER2_SPRITE.sprite
            return True
        return False

    def attack(self):
        pass
        # if self.target.rect.center[0] < self.rect.center[0]:
        #     self.direction.x = - 1
        # else:
        #     self.direction.x = 1
        # if self.target.rect.center[1] < self.rect.center[1]:
        #     self.direction.y = - 1
        # else:
        #     self.direction.y = 1

    def update(self):

        self.animate()
        if self.rect.x < 150 and self.status == 'fly':
            self.direction.x = 1
        if self.rect.x > 480 and self.status == 'fly':
            self.direction.x = -1

        if self.tog:
            self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        if self.tog:
            self.rect.y += self.direction.y * self.speed
        self.vertical_collisions()
        self.weapon_collisions()

        if self.status == 'fly' and self.player_nearby() and pygame.time.get_ticks() - self.attack_end_time > 2000:
            self.status = 'attack'
            self.animation_index = 0

        if self.status == 'attack':
            self.attack()

        self.tog = not self.tog

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Boss(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites, player_weapon_sprites, type):
        super().__init__(groups)

        self.type = type
        path = f'./assets/images/enemy/'

        if type == 'boss2':
            path += f'mushroom/'
        elif type == 'boss3':
            path += f'executioner/'

        self.frames = {'idle': [], 'attack': [], 'hit': [], 'dead': [], 'run': []}

        for status in self.frames.keys():
            full_path = path + status
            self.frames[status] = import_frames(full_path, scale=0.8)

        self.animation_index = 0
        self.status = 'run'

        self.image = self.frames[self.status][self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2()
        self.direction.x = 1
        if type == 'boss3':
            self.direction.y = 1
        self.is_flipped = False
        self.speed = 1
        self.tog = True
        self.collision_sprites = collision_sprites
        self.player_weapon_sprites = player_weapon_sprites

        self.player1_active = False
        self.player2_active = False

        self.target = None
        self.attack_end_time = 0

        self.old_status = None
        self.old_direction = None

        self.lives = 2

        self.timer = 5
        self.movement_update()


    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                self.movement_update()

        if self.rect.left < 130 and self.status == 'run':
            self.is_flipped = False
            self.change_direction()
            # self.direction.x = 1
        if self.rect.right > 470 and self.status == 'run':
            self.is_flipped = True
            self.change_direction()
            # self.direction.x = -1

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                self.movement_update()

        if self.rect.top < 110 and self.status == 'run':
            self.direction.y = 1
        if self.rect.bottom > 200 and self.status == 'run':
            self.direction.y = -1

    def movement_update(self):

        self.direction.x *= -1
        self.is_flipped = not self.is_flipped


    def animate(self):

        status = self.frames[self.status]

        # loop over frame index
        self.animation_index += 0.07
        if self.animation_index >= len(status):
            self.animation_index = 0

            if self.status == 'attack':
                self.attack_end_time = pygame.time.get_ticks()
                self.status = 'run'
                self.change_direction()
            if self.status == 'idle':
                self.status = 'attack'
            if self.status == 'hit':
                self.status = self.old_status
            if self.status == 'dead':
                self.kill()


        self.image = status[int(self.animation_index)]
        if self.is_flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.is_flipped:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        else:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)

    def weapon_collisions(self):
        for sprite in self.player_weapon_sprites.sprites():
            if sprite.rect.colliderect(self.rect) and sprite.status == 'attack' and (self.status == 'run' or self.status == 'idle'):
                if pygame.sprite.collide_mask(self, sprite):
                    self.lives -= 1
                    self.old_status = self.status
                    self.status = 'hit'
                    self.animation_index = 0
                    if self.lives == 0:
                        self.status = 'dead'
                        self.animation_index = 0
                        if self.player1_active:
                            PLAYER1_SPRITE.sprite.key_active = True
                        if self.player2_active:
                            PLAYER2_SPRITE.sprite.key_active = True


    def player_nearby(self):
        if self.player1_active and math.dist(PLAYER1_SPRITE.sprite.rect.center, self.rect.center) < 30:
            # self.target = PLAYER1_SPRITE.sprite
            if self.rect.center[0] - PLAYER1_SPRITE.sprite.rect.center[0] > 0:
                self.is_flipped = True
            else:
                self.is_flipped = False
            return True
        if self.player2_active and math.dist(PLAYER2_SPRITE.sprite.rect.center, self.rect.center) < 30:
            # self.target = PLAYER2_SPRITE.sprite
            if self.rect.x - PLAYER2_SPRITE.sprite.rect.x > 0:
                self.is_flipped = True
            else:
                self.is_flipped = False
            return True
        return False

    def change_direction(self):
        if self.status == 'idle':
            self.direction.x = 0
            if self.type == 'boss3':
                self.direction.y = 0
        elif self.status == 'run':
            if self.type == 'boss3':
                self.direction.y = 1
            if self.is_flipped:
                self.direction.x = -1
            else:
                self.direction.x = 1

    def update(self):

        self.animate()


        if self.tog and self.status == 'run':
            self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        if self.type == 'boss3':
            if self.tog and self.status == 'run':
                self.rect.y += self.direction.y * self.speed
            self.vertical_collisions()
        self.weapon_collisions()

        if self.status == 'run' and pygame.time.get_ticks() - self.attack_end_time > 2000:
            if self.player_nearby():
                self.status = 'idle'
                self.animation_index = 0
                self.change_direction()

        self.tog = not self.tog

    def draw(self, screen):
        screen.blit(self.image, self.rect)
