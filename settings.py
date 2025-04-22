import math

# game settings
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

#player settings
PLAYER_POS = 7, 3 # mini_map
PLAYER_ANGLE = 0
PLAYER_ROT_SPEED = 0.002
PLAYER_SPEED = 0.004

# raycasting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

# projection
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS