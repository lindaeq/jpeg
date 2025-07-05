import pygame
import sys

pygame.init()
pygame.mixer.init()  # <-- Fixed: ensure mixer is initialized before loading sound

# Set up screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coffee Station")

# Load images
background = pygame.image.load("images/background.png").convert()
coffee_machine = pygame.image.load("images/coffee_machine.png").convert_alpha()
cup_empty = pygame.image.load("images/cup_empty.JPG").convert_alpha()
cup_full = pygame.image.load("images/cup_full.JPG").convert_alpha()

# Load sound
brew_sound = pygame.mixer.Sound("sounds/brew_sound.mp3")
brew_length = brew_sound.get_length()

def run(screen):
    font = pygame.font.SysFont(None, 40)
    text = font.render("COFFEE: Press ESC to return to Cafe", True, (0, 0, 0))
    button_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Button setup
    button_color = (100, 160, 100)
    hover_color = (120, 180, 120)
    button_rect = pygame.Rect(500, 300, 150, 60)
    button_text = button_font.render("Fill", True, (255, 255, 255))

    cup_filled = False
    brewing = False
    brew_start_time = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "cafe"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        # Draw background and UI
        screen.fill((210, 180, 140))
        screen.blit(background, (0, 0))
        screen.blit(text, (50, 20))
        screen.blit(coffee_machine, (50, 150))

        # Draw cup
        if cup_filled:
            screen.blit(cup_full, (130, 280))
        else:
            screen.blit(cup_empty, (130, 280))

        # Draw Fill button
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect)
            if clicked and not brewing and not cup_filled:
                brew_sound.play()
                brewing = True
                brew_start_time = pygame.time.get_ticks()
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        # Draw button text
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        # Finish brewing
        if brewing:
            elapsed = (pygame.time.get_ticks() - brew_start_time) / 1000
            if elapsed >= brew_length:
                brewing = False
                cup_filled = True

        pygame.display.flip()
        clock.tick(60)

# Run for testing
if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()
    sys.exit()
