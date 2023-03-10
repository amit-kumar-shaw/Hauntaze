"""
Constants for the game
"""
import pygame
from pygame.locals import *

# screen
FPS = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360

# walls
TILE_SIZE = 16
TILE_WIDTH = 16
TILE_HEIGHT = 16

LAST_SURVIVAL_LEVEL = 50

# map
COLUMNS = 8
ROWS = 4
CELL_SIZE = 5

# player
PLAYER_SPEED = 1
VISIBILITY_RADIUS = 45
PLAYER_LIVES = 3
INVINSIBILITY_DURATION = 2500
ATTACK_DELAY = 500
PLAYER1_SPRITE = pygame.sprite.GroupSingle()
PLAYER2_SPRITE = pygame.sprite.GroupSingle()

GHOST_VISIBILITY = 30


BOSS1_LIVES = 5
BOSS2_LIVES = 7
BOSS3_LIVES = 10

# colors
BG_COLOR = 'black'
PLAYER_COLOR = '#C4F7FF'
TILE_COLOR = '#612903'
COVER_COLOR = (0, 0, 0, 255)

TITLE_COLOR = (230, 14, 14)

# UI Surface
UI_SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - (ROWS * CELL_SIZE * TILE_HEIGHT)))
UI_SURFACE.fill('black')

# Keyboard Controls
CONFIRM = K_RETURN
COIN_KEYBOARD = K_SPACE
PAUSE = K_ESCAPE

PLAYER1_MOVE_LEFT = K_a
PLAYER1_MOVE_RIGHT = K_d
PLAYER1_MOVE_UP = K_w
PLAYER1_MOVE_DOWN = K_s
PLAYER1_ATTACK = K_q
PLAYER1_LIFE = K_e
PLAYER1_DEATH = K_r

PLAYER2_MOVE_LEFT = K_j
PLAYER2_MOVE_RIGHT = K_l
PLAYER2_MOVE_UP = K_i
PLAYER2_MOVE_DOWN = K_k
PLAYER2_ATTACK = K_u
PLAYER2_LIFE = K_o
PLAYER2_DEATH = K_p

# Joystick controls
LEFT_RIGHT_AXIS = 0
UP_DOWN_AXIS = 1
BLACK_BUTTON = 0
RED_BUTTON = 1
BLUE_BUTTON = 2
YELLOW_BUTTON = 3
START_BUTTON = 4
COIN_BUTTON = 5
AXIS_THRESHOLD = 0.9
