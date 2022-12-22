import pygame

# screen
FPS = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360

# walls
TILE_SIZE = 16
TILE_WIDTH = 16
TILE_HEIGHT = 16
# TILE_WIDTH = SCREEN_WIDTH/(CELL_X*CELL_SIZE)
# TILE_HEIGHT = SCREEN_HEIGHT/(CELL_Y*CELL_SIZE)

# map
COLUMNS = 7
ROWS = 4
CELL_SIZE = 5

# player
PLAYER_SPEED = 1
VISIBILITY_RADIUS = 45
LIVES = 3
INVINSIBILITY_DURATION = 2500
PLAYER1_SPRITE = pygame.sprite.Group()
PLAYER2_SPRITE = pygame.sprite.Group()

GHOST_VISIBILITY = 30

# colors
BG_COLOR = 'black'
PLAYER_COLOR = '#C4F7FF'
TILE_COLOR = '#612903'
COVER_COLOR = (0, 0, 0, 255)

TITLE_COLOR = (230, 14, 14)

# UI Surface
UI_SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - (ROWS * CELL_SIZE * TILE_HEIGHT)))
UI_SURFACE.fill('black')

STORY_DATA = [
    {
        'player1': (2, 2),
        'player2': (33, 2),
        'key1': (26, 6),
        'key2': (9, 11),
        'door1': (5, 4),
        'door2': (30, 4),
        'map': ['####################################',
                '#..........#.......#......#........#',
                '#.A........#.......#......#......B.#',
                '#..........#.......#......#........#',
                '#....D.....#.......#......#...D....#',
                '#..........#.......#......#........#',
                '#..........#.......#....K..........#',
                '########...#..######...............#',
                '#..........#...........#############',
                '#..........#.......................#',
                '#..........#......#................#',
                '#........K........#...........#....#',
                '#...............########......#....#',
                '#...###########.#.............#....#',
                '#.............#...............#....#',
                '#.............#.......#########....#',
                '#.......#.....#..........#.........#',
                '#.......#.....#..........#.........#',
                '#.......#.....#..........#.........#',
                '####################################']
    }
]