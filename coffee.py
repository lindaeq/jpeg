import pygame
import sys
import game_state

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

# Constants for coffee icon stack
ICON_SCALE = 0.4
ICON_MARGIN_BOTTOM = 15
ICON_SPACING = 10

def run(screen, coffee_served=0, coffee_icons=None, mouse_normal=None, mouse_clicked=None):
    if coffee_icons is None:
        coffee_icons = []

    # Ensure coffee_offer_number is set in game_state
    if not hasattr(game_state, "coffee_offer_number") or game_state.coffee_offer_number is None:
        game_state.coffee_offer_number = 1

    clock = pygame.time.Clock()

    button_x = 500
    button_y_start = 175
    button_spacing = 105

    place_cup_rect = button_place_cup_img.get_rect(topleft=(button_x, button_y_start))
    pour_rect = button_pour_img.get_rect(topleft=(button_x, button_y_start + button_spacing))
    serve_rect = button_serve_img.get_rect(topleft=(button_x, button_y_start + 2 * button_spacing))

    exit_button_pos = (860, 60)
    exit_button_rect = pygame.Rect(exit_button_pos, exit_button.get_size())

    cup_stage = None
    brewing = False
    brew_start_time = 0

    animating_cup = False
    anim_cup_pos = pygame.Vector2(209, 310)
    anim_cup_target_x = 25
    anim_cup_speed = 12

    serve_click_count = 0  # Track number of serve clicks

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", coffee_served, coffee_icons
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "cafe", coffee_served, coffee_icons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button_rect.collidepoint(event.pos):
                    return "cafe", coffee_served, coffee_icons
                if place_cup_rect.collidepoint(event.pos) and cup_stage is None:
                    if serve_click_count < game_state.coffee_offer_number:
                        cup_stage = "empty"
                        click_sound.play()
                elif pour_rect.collidepoint(event.pos) and cup_stage == "empty" and not brewing:
                    if serve_click_count < game_state.coffee_offer_number:
                        click_sound.play()
                        brew_sound.play()
                        brewing = True
                        brew_start_time = pygame.time.get_ticks()
                elif serve_rect.collidepoint(event.pos) and cup_stage == "full" and not brewing and not animating_cup:
                    if serve_click_count < game_state.coffee_offer_number:
                        click_sound.play()
                        cup_stage = None
                        coffee_served += 1
                        serve_click_count += 1
                        animating_cup = True
                        anim_cup_pos = pygame.Vector2(209, 310)

        screen.fill((210, 180, 140))
        screen.blit(background, (0, 0))

        # Draw cup (either animating or static)
        if animating_cup:
            icon_height = cup_full.get_height() * ICON_SCALE
            target_y = SCREEN_HEIGHT - ICON_MARGIN_BOTTOM - (icon_height + ICON_SPACING) * coffee_served
            target_pos = pygame.Vector2(anim_cup_target_x, target_y)

            direction = target_pos - anim_cup_pos
            if direction.length() < anim_cup_speed:
                anim_cup_pos = target_pos
                animating_cup = False
                coffee_icons.append((anim_cup_pos.x, anim_cup_pos.y))
            else:
                direction.scale_to_length(anim_cup_speed)
                anim_cup_pos += direction

            screen.blit(cup_full, anim_cup_pos)
        else:
            if cup_stage == "empty":
                screen.blit(cup_empty, (209, 310))
            elif cup_stage == "medium":
                screen.blit(cup_medium, (209, 310))
            elif cup_stage == "full":
                screen.blit(cup_full, (209, 310))

        # Draw exit button
        screen.blit(exit_button, exit_button_pos)

        # Disable buttons if offer number reached
        max_serves_reached = serve_click_count >= game_state.coffee_offer_number

        place_cup_enabled = not max_serves_reached and cup_stage is None
        pour_enabled = (cup_stage == "empty" and not brewing and not max_serves_reached)
        serve_enabled = (cup_stage == "full" and not brewing and not animating_cup and not max_serves_reached)

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

        # Brewing logic
        if brewing:
            elapsed = (pygame.time.get_ticks() - brew_start_time) / 1000
            if elapsed >= 2 and cup_stage == "empty":
                cup_stage = "medium"
            if elapsed >= brew_length:
                brewing = False
                cup_stage = "full"

        # Draw stacked icons
        for pos in coffee_icons:
            scaled_cup = pygame.transform.smoothscale(
                cup_full,
                (int(cup_full.get_width() * ICON_SCALE), int(cup_full.get_height() * ICON_SCALE))
            )
            screen.blit(scaled_cup, pos)


        # Custom cursor
        if mouse_normal and mouse_clicked:
            if mouse_pressed:
                screen.blit(mouse_clicked, mouse_pos)
            else:
                screen.blit(mouse_normal, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

def get_coffee_assets():
    scaled_icon = pygame.transform.smoothscale(
        cup_full,
        (int(cup_full.get_width() * ICON_SCALE), int(cup_full.get_height() * ICON_SCALE))
    )
    font = pygame.font.SysFont(None, 36)
    return scaled_icon, font

if __name__ == "__main__":
    mouse_normal = None
    mouse_clicked = None
    result, _, _ = run(screen, mouse_normal, mouse_clicked)
    print("Returned:", result)
    pygame.quit()
    sys.exit()
