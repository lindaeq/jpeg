import pygame
import sys

pygame.init()
pygame.font.init()  # Initialize the font module

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Screen")

# Load images
start_background = pygame.image.load("images/start/background.png")

def run(screen):
    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Button setup
    button_color = (180, 80, 80)
    hover_color = (200, 100, 100)
    button_rect = pygame.Rect(50, 300, 200, 60)
    button_text = button_font.render("Go to Cafe", True, (255, 255, 255))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        # Fill screen and draw background
        screen.fill((200, 230, 255))
        screen.blit(start_background, (0, 0))

        # Draw button
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect)
            if clicked:
                return "cafe"
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        # Draw button text centered
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()
    sys.exit()
