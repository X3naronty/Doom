import math
from os import listdir
from os.path import join

# game settings
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# floor 
FLOOR_COLOR = (30, 30, 30)


# sky 
SKY_IMAGE_PATH = join("resources", "textures", "sky.png")

#player settings
PLAYER_POS = 7, 5 # mini_map
PLAYER_ANGLE = 0
PLAYER_ROT_SPEED = 0.002
PLAYER_SPEED = 0.004
PLAYER_SIZE = 60


# mouse 
MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# raycasting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# projection
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS


# textures
TEXTURE_SIZE = 256
TEXTURE_HALF_SIZE = TEXTURE_SIZE // 2
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# walls
TEXTURE_WALL_NUM = 5
TEXTURE_WALL_PATH = join("resources", "textures", "walls")
