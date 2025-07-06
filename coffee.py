import pygame
import sys

pygame.init()
pygame.mixer.init()

click_sound = pygame.mixer.Sound("sounds/click.mp3")
trash_click_sound = pygame.mixer.Sound("sounds/trash_click.mp3")
quack_sound = pygame.mixer.Sound("sounds/quack.mp3")

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coffee Station")

# Load images
background = pygame.image.load("images/coffee/coffee_background.PNG").convert()
coffee_machine = pygame.image.load("images/coffee/coffee_machine.png").convert_alpha()
cup_empty = pygame.image.load("images/coffee/cup_empty.png").convert_alpha()
cup_medium = pygame.image.load("images/coffee/cup_medium.png").convert_alpha()
cup_full = pygame.image.load("images/coffee/cup_full.png").convert_alpha()
exit_button = pygame.image.load("images/coffee/button.png").convert_alpha()

# Load button images (enabled and disabled versions)
button_place_cup_img = pygame.image.load("images/coffee/button_place_cup.png").convert_alpha()
button_pour_img = pygame.image.load("images/coffee/button_pour.png").convert_alpha()
button_serve_img = pygame.image.load("images/coffee/button_serve.png").convert_alpha()

button_place_cup_disabled = pygame.image.load("images/coffee/button_2_place_cup.png").convert_alpha()
button_pour_disabled = pygame.image.load("images/coffee/button_2_pour.png").convert_alpha()
button_serve_disabled = pygame.image.load("images/coffee/button_2_serve.png").convert_alpha()

# Sound
brew_sound = pygame.mixer.Sound("sounds/brew_sound.mp3")
brew_length = brew_sound.get_length()

# Font for counter
font = pygame.font.SysFont(None, 36)

def run(screen, coffee_served=0, coffee_icons=None):
    if coffee_icons is None:
        coffee_icons = []

    clock = pygame.time.Clock()

    # Button positions
    button_x = 500
    button_y_start = 175
    button_spacing = 105

    # Button rects
    place_cup_rect = button_place_cup_img.get_rect(topleft=(button_x, button_y_start))
    pour_rect = button_pour_img.get_rect(topleft=(button_x, button_y_start + button_spacing))
    serve_rect = button_serve_img.get_rect(topleft=(button_x, button_y_start + 2 * button_spacing))

    # Exit button
    exit_button_pos = (860, 60)
    exit_button_rect = pygame.Rect(exit_button_pos, exit_button.get_size())

    cup_stage = None  # None, "empty", "medium", "full"
    brewing = False
    brew_start_time = 0

    full_cup_icon = pygame.transform.scale(cup_full, (40, 40))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", coffee_served, coffee_icons
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "cafe", coffee_served, coffee_icons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        screen.fill((210, 180, 140))
        screen.blit(background, (0, 0))

        # Draw cup
        if cup_stage == "empty":
            screen.blit(cup_empty, (209, 310))
        elif cup_stage == "medium":
            screen.blit(cup_medium, (209, 310))
        elif cup_stage == "full":
            screen.blit(cup_full, (209, 310))

        # Exit button
        screen.blit(exit_button, exit_button_pos)
        if exit_button_rect.collidepoint(mouse_pos) and clicked:
            return "cafe", coffee_served, coffee_icons

        # Button states
        place_cup_enabled = True
        pour_enabled = (cup_stage == "empty" and not brewing)
        serve_enabled = (cup_stage == "full" and not brewing)

        def draw_button(enabled_img, disabled_img, rect, enabled):
            if enabled:
                if rect.collidepoint(mouse_pos):
                    bright_img = enabled_img.copy()
                    bright_img.fill((30, 30, 30, 0), special_flags=pygame.BLEND_RGB_ADD)
                    screen.blit(bright_img, rect.topleft)
                else:
                    screen.blit(enabled_img, rect.topleft)
            else:
                screen.blit(disabled_img, rect.topleft)

        draw_button(button_place_cup_img, button_place_cup_disabled, place_cup_rect, place_cup_enabled)
        draw_button(button_pour_img, button_pour_disabled, pour_rect, pour_enabled)
        draw_button(button_serve_img, button_serve_disabled, serve_rect, serve_enabled)

        if clicked:
            if place_cup_rect.collidepoint(mouse_pos) and place_cup_enabled:
                if cup_stage is None:
                    cup_stage = "empty"
                    click_sound.play()
            elif pour_rect.collidepoint(mouse_pos) and pour_enabled:
                click_sound.play()
                brew_sound.play()
                brewing = True
                brew_start_time = pygame.time.get_ticks()
            elif serve_rect.collidepoint(mouse_pos) and serve_enabled:
                click_sound.play()
                cup_stage = None
                coffee_served += 1
                icon_spacing = 45
                icon_y = SCREEN_HEIGHT - 60
                icon_x = 80 - (coffee_served * icon_spacing)
                coffee_icons.append((icon_x, icon_y))

        if brewing:
            elapsed = (pygame.time.get_ticks() - brew_start_time) / 1000
            if elapsed >= 2 and cup_stage == "empty":
                cup_stage = "medium"
            if elapsed >= brew_length:
                brewing = False
                cup_stage = "full"

        for pos in coffee_icons:
            screen.blit(full_cup_icon, pos)

        counter_text = font.render(f"Coffee: {coffee_served}", True, (0, 0, 0))
        screen.blit(counter_text, (90, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

# For standalone testing
if __name__ == "__main__":
    result, _, _ = run(screen)
    print("Returned:", result)
    pygame.quit()
    sys.exit()