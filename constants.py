# Constants module
# Contains all the constants used by the other modules

# To find the image and sound paths
from os import path

CLASSICAL_TIME = 5400
RAPID_TIME = 1800
BLITZ_TIME = 300
BULLET_TIME = 60
DIMENSIONS = (800, 800)
PIECE_DIMENSIONS = (DIMENSIONS[0] // 8 - 10, DIMENSIONS[0] // 8 - 10)
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHARCOAL = (34, 32, 33)
GHOST_WHITE = (248, 248, 255)
BACKGROUND = (196, 164, 132)
DARK_BOARD = (184, 139, 74)
LIGHT_BOARD = (227, 193, 111)
DARK_HIGHLIGHT = (186, 185, 250)
LIGHT_HIGHLIGHT = (230, 230, 255)
SPECIAL_HIGHLIGHT = (255, 255, 255)
CHECK_HIGHLIGHT = (243, 63, 66)
MENU_COLOR = (207, 185, 151)
BOX_COLOR = (128, 96, 29)
IMAGE_PATH = path.join(path.dirname(__file__), 'images/')
SOUND_PATH = path.join(path.dirname(__file__), 'sounds/')
