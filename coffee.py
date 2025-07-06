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
exit_button = pygame.image.load("images/coffee/button.png").convert_alpha()  # ⬅️ new button image

# Load sound
brew_sound = pygame.mixer.Sound("sounds/brew_sound.mp3")
brew_length = brew_sound.get_length()

def run(screen):
    font = pygame.font.SysFont(None, 40)
    button_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Fill button setup
    button_color = (100, 160, 100)
    hover_color = (120, 180, 120)
    fill_button_rect = pygame.Rect(500, 300, 150, 60)
    fill_button_text = button_font.render("Fill", True, (255, 255, 255))

    # Exit button setup (using image)
    exit_button_pos = (860, 60)
    exit_button_rect = pygame.Rect(exit_button_pos, exit_button.get_size())

    cup_stage = "empty"
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

        # Draw cup
        if cup_stage == "empty":
            screen.blit(cup_empty, (209, 310))
        elif cup_stage == "medium":
            screen.blit(cup_medium, (209, 310))
        elif cup_stage == "full":
            screen.blit(cup_full, (209, 310))

        # Draw exit button image
        screen.blit(exit_button, exit_button_pos)

        if exit_button_rect.collidepoint(mouse_pos) and clicked:
            return "cafe"

        # Draw fill button
        if fill_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, fill_button_rect)
            if clicked and not brewing and cup_stage == "empty":
                brew_sound.play()
                brewing = True
                brew_start_time = pygame.time.get_ticks()
        else:
            pygame.draw.rect(screen, button_color, fill_button_rect)

        text_rect = fill_button_text.get_rect(center=fill_button_rect.center)
        screen.blit(fill_button_text, text_rect)

        # Brewing progress
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
