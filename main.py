import pygame
import loading
import start
import click_screen
import cafe
import trash

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raccoon Café")

pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)

# Load custom cursors
mouse_normal = pygame.image.load("images/mouse_normal.png").convert_alpha()
mouse_clicked = pygame.image.load("images/mouse_clicked.png").convert_alpha()

# Start with the loading screen
current_screen = "loading"

while True:
    if current_screen == "loading":
        current_screen = loading.run(screen)

    elif current_screen == "start":
        current_screen = start.run(screen, mouse_normal, mouse_clicked)

    elif current_screen == "click":
        current_screen = click_screen.run(screen, mouse_normal, mouse_clicked)

    elif current_screen == "cafe":
        current_screen = cafe.run(screen, mouse_normal, mouse_clicked)

    elif current_screen == "trash":
        current_screen = trash.run(screen, mouse_normal, mouse_clicked)

    elif current_screen == "quit":
        break

pygame.quit()
