import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Fonts
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 40)

# Clock
clock = pygame.time.Clock()

background = pygame.image.load("assets/bg.png")
