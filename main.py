import pygame
from start import run as run_start
from cafe import run as run_cafe
from coffee import run as run_coffee
from trash import run as run_trash

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Café Game")

# Set starting screen
current_screen = "start"
running = True

# Main game loop
while running:
    if current_screen == "start":
        current_screen = run_start(screen)
    elif current_screen == "cafe":
        current_screen = run_cafe(screen)
    elif current_screen == "coffee":
        current_screen = run_coffee(screen)
    elif current_screen == "trash":
        current_screen = run_trash(screen)
    elif current_screen == "quit":
        running = False

# Quit game cleanly
pygame.quit()
