import pygame
from start import run as run_start
from cafe import run as run_cafe
from coffee import run as run_coffee
from trash import run as run_trash
from click_screen import run as run_click

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Café Game")

# Load cursor images once
try:
    mouse_normal = pygame.image.load("images/mouse_normal.png").convert_alpha()
    mouse_clicked = pygame.image.load("images/mouse_clicked.png").convert_alpha()
except pygame.error as e:
    print(f"Error loading cursor images: {e}")
    pygame.quit()
    exit()

pygame.mouse.set_visible(False)  # Hide system cursor

# Set initial screen
current_screen = "start"
running = True

# Main game loop
while running:
    if current_screen == "start":
        current_screen = run_start(screen, mouse_normal, mouse_clicked)
    elif current_screen == "cafe":
        current_screen = run_cafe(screen, mouse_normal, mouse_clicked)
    elif current_screen == "coffee":
        current_screen = run_coffee(screen, mouse_normal, mouse_clicked)
    elif current_screen == "trash":
        current_screen = run_trash(screen, mouse_normal, mouse_clicked)
    elif current_screen == "click":
        current_screen = run_click(screen, mouse_normal, mouse_clicked)
    elif current_screen == "quit":
        running = False
    else:
        print(f"Unknown screen: {current_screen}")
        running = False

pygame.quit()
