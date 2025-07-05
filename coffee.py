import pygame
import sys

pygame.init()
pygame.mixer.init()

# Set up screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coffee Station")

# Load images
background = pygame.image.load("images/coffee/coffee_background.PNG").convert()
coffee_machine = pygame.image.load("images/coffee/coffee_machine.png").convert_alpha()
cup_empty = pygame.image.load("images/coffee/cup_empty.png").convert_alpha()
cup_medium = pygame.image.load("images/coffee/cup_medium.png").convert_alpha()
cup_full = pygame.image.load("images/coffee/cup_full.png").convert_alpha()

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

    cup_stage = "empty"  # can be "empty", "medium", or "full"
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

        # Background + static elements
        screen.fill((210, 180, 140))
        screen.blit(background, (0, 0))
        screen.blit(text, (50, 20))
        screen.blit(coffee_machine, (50, 150))

        # Draw cup based on stage
        if cup_stage == "empty":
            screen.blit(cup_empty, (130, 280))
        elif cup_stage == "medium":
            screen.blit(cup_medium, (130, 280))
        elif cup_stage == "full":
            screen.blit(cup_full, (130, 280))

        # Draw Fill button
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect)
            if clicked and not brewing and cup_stage == "empty":
                brew_sound.play()
                brewing = True
                brew_start_time = pygame.time.get_ticks()
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        # Brewing progress logic
        if brewing:
            elapsed = (pygame.time.get_ticks() - brew_start_time) / 1000

            if elapsed >= 2 and cup_stage == "empty":
                cup_stage = "medium"
            if elapsed >= brew_length:
                brewing = False
                cup_stage = "full"

        pygame.display.flip()
        clock.tick(60)

# Run for testing
if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()
    sys.exit()
