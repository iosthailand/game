import pygame

# Game Configuration
TITLE = "Pygame RPG Professional"
# Display settings
WIDTH = 800
HEIGHT = 600
FPS = 60
BGCOLOR = (30, 30, 30)
# Use SCALED for automatic resizing and keeping aspect ratio
# Use RESIZABLE to allow window resizing
FLAGS = pygame.SCALED | pygame.RESIZABLE 

# Tile settings
TILESIZE = 32
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Player settings
PLAYER_SPEED = 300
PLAYER_SIZE = 48 # Slightly larger than tile for better visibility

# Layer settings
PLAYER_LAYER = 2
TILE_LAYER = 1
