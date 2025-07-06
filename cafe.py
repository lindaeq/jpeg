import pygame
import time
import random
import coffee  # Make sure this is the correct filename

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)  # Hide system mouse cursor

def run(screen, mouse_normal=None, mouse_clicked=None):
    background = pygame.image.load("images/cafe/cafe.png").convert()
    trash_can_img = pygame.image.load("images/cafe/trash_can.png").convert_alpha()
    coffee_button_img = pygame.image.load("images/cafe/button_coffee_machine.png").convert_alpha()
    raccoon_img = pygame.image.load("images/cafe/raccoon.png").convert_alpha()
    dialogue_img = pygame.image.load("images/cafe/dialogue.png").convert_alpha()
    full_coffee_img = pygame.image.load("images/cafe/cup_full.png").convert_alpha()

    scale_factor = 0.5
    original_width = full_coffee_img.get_width()
    original_height = full_coffee_img.get_height()
    scaled_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    full_coffee_img = pygame.transform.smoothscale(full_coffee_img, scaled_size)

    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    trash_rect = trash_can_img.get_rect(topleft=(0, (SCREEN_HEIGHT - trash_can_img.get_height()) // 2 - 25))
    coffee_button_pos = (675, SCREEN_HEIGHT - coffee_button_img.get_height() - 120)
    coffee_button_rect = coffee_button_img.get_rect(topleft=coffee_button_pos)

    coffee_served = 0
    coffee_icons = []

    full_cup_icon, counter_font = coffee.get_coffee_assets()

    raccoon_x = -raccoon_img.get_width()
    raccoon_y = SCREEN_HEIGHT // 4 - 25
    raccoon_target_x = SCREEN_WIDTH * 2/3 - raccoon_img.get_width() // 2 - 100
    raccoon_speed = 8
    raccoon_arrived = False
    dialogue_visible = False
    dialogue_timer_started = False
    dialogue_start_time = 0
    coffee_offer_number = None

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # True if left mouse button is held

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "start"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if trash_rect.collidepoint(event.pos):
                    return "click"
                elif coffee_button_rect.collidepoint(event.pos):
                    result, coffee_served, coffee_icons = coffee.run(
                        screen, coffee_served, coffee_icons, mouse_normal, mouse_clicked
                    )
                    if result == "quit":
                        return "quit"

        screen.blit(background, (0, 0))

        # Trash can
        if trash_rect.collidepoint(mouse_pos):
            bright_trash = trash_can_img.copy()
            bright_trash.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_trash, trash_rect.topleft)
        else:
            screen.blit(trash_can_img, trash_rect.topleft)

        # Coffee machine
        if coffee_button_rect.collidepoint(mouse_pos):
            bright_button = coffee_button_img.copy()
            bright_button.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_button, coffee_button_rect.topleft)
        else:
            screen.blit(coffee_button_img, coffee_button_rect.topleft)

        # Draw coffee icons
        for pos in coffee_icons:
            screen.blit(full_cup_icon, pos)

        # Draw coffee counter
        counter_text = counter_font.render(f"Coffee: {coffee_served}", True, (0, 0, 0))
        screen.blit(counter_text, (90, SCREEN_HEIGHT - 30))

        # Animate raccoon
        if not raccoon_arrived:
            raccoon_x += raccoon_speed
            if raccoon_x >= raccoon_target_x:
                raccoon_x = raccoon_target_x
                raccoon_arrived = True
                dialogue_timer_started = True
                dialogue_start_time = pygame.time.get_ticks()
        screen.blit(raccoon_img, (raccoon_x, raccoon_y))

        # Show dialogue after delay
        if dialogue_timer_started and not dialogue_visible:
            if pygame.time.get_ticks() - dialogue_start_time >= 500:
                dialogue_visible = True
                coffee_offer_number = random.choice([1, 2, 3])

        if dialogue_visible:
            dialogue_rect = dialogue_img.get_rect(topright=(SCREEN_WIDTH - 20, 0))
            screen.blit(dialogue_img, dialogue_rect)

            icon_x = dialogue_rect.left + 60
            icon_y = dialogue_rect.centery - full_coffee_img.get_height() // 2
            screen.blit(full_coffee_img, (icon_x, icon_y))

            if coffee_offer_number is not None:
                number_text = font.render(f"X {coffee_offer_number}", True, (0, 0, 0))
                text_x = icon_x + full_coffee_img.get_width() + 15
                text_y = icon_y + full_coffee_img.get_height() // 2 - number_text.get_height() // 2
                screen.blit(number_text, (text_x, text_y))

        # Instruction text
        instruction = font.render("Click Trash or Coffee Machine. ESC to return.", True, (0, 0, 0))
        screen.blit(instruction, (50, 30))

        # Draw custom cursor
        if mouse_normal and mouse_clicked:
            if mouse_pressed:
                screen.blit(mouse_clicked, mouse_pos)
            else:
                screen.blit(mouse_normal, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    mouse_normal = pygame.image.load("images/mouse_normal.png").convert_alpha()
    mouse_clicked = pygame.image.load("images/mouse_clicked.png").convert_alpha()
    pygame.mouse.set_visible(False)

    result = run(screen, mouse_normal, mouse_clicked)
    print("Returned:", result)
    pygame.quit()
