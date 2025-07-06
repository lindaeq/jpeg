import pygame
import time
import random
import coffee
import game_state

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()
pygame.font.init()
pygame.mixer.init()

click_sound = pygame.mixer.Sound("sounds/click.mp3")
sparkle_sound = pygame.mixer.Sound("sounds/sparkle.mp3")
raccoon_sound = pygame.mixer.Sound("sounds/raccoon_sound.mp3")
register_sound = pygame.mixer.Sound("sounds/register.mp3")  # NEW

pygame.mouse.set_visible(False)  # Hide system mouse cursor

def run(screen, mouse_normal=None, mouse_clicked=None):
    background1 = pygame.image.load("images/cafe/cafe.png").convert()
    background2 = pygame.image.load("images/cafe/cafe1.png").convert()

    trash_can_img = pygame.image.load("images/cafe/trash_can.png").convert_alpha()
    coffee_button_img = pygame.image.load("images/cafe/button_coffee_machine.png").convert_alpha()
    register_img = pygame.image.load("images/cafe/register.png").convert_alpha()  # NEW

    raccoon_img1 = pygame.image.load("images/cafe/raccoon.png").convert_alpha()
    raccoon_img2 = pygame.image.load("images/cafe/raccoon1.png").convert_alpha()
    raccoon_img3 = pygame.image.load("images/cafe/raccoon2.png").convert_alpha()
    raccoon_images = [raccoon_img1, raccoon_img2, raccoon_img3]

    dialogue_img = pygame.image.load("images/cafe/dialogue.png").convert_alpha()
    full_coffee_img = pygame.image.load("images/cafe/cup_full.png").convert_alpha()
    sparkle_img = pygame.image.load("images/cafe/sparkle.png").convert_alpha()

    scale_factor = 0.5
    full_coffee_img = pygame.transform.smoothscale(
        full_coffee_img,
        (int(full_coffee_img.get_width() * scale_factor), int(full_coffee_img.get_height() * scale_factor))
    )

    font = pygame.font.Font("fonts/pixel.ttf", 60)
    clock = pygame.time.Clock()

    trash_rect = trash_can_img.get_rect(topleft=(7.5, (SCREEN_HEIGHT - trash_can_img.get_height()) // 2 - 28))
    coffee_button_pos = (675, SCREEN_HEIGHT - coffee_button_img.get_height() - 120)
    coffee_button_rect = coffee_button_img.get_rect(topleft=coffee_button_pos)
    register_pos = (SCREEN_WIDTH // 2 - register_img.get_width() // 2-94, SCREEN_HEIGHT - register_img.get_height()-127)
    register_rect = register_img.get_rect(topleft=register_pos)

    coffee_served = 0
    full_cup_icon, counter_font = coffee.get_coffee_assets()

    if not hasattr(game_state, "coffee_offer_number") or game_state.coffee_offer_number is None:
        game_state.coffee_offer_number = random.choice([1, 2, 3])
    if not hasattr(game_state, "raccoon_sliding_out"):
        game_state.raccoon_sliding_out = False

    raccoon_x = (SCREEN_WIDTH // 2) - 100
    raccoon_y = SCREEN_HEIGHT // 4 - 25
    raccoon_target_x = SCREEN_WIDTH * 0.57 - raccoon_img1.get_width() // 2
    raccoon_speed = 8

    raccoon_arrived = False
    dialogue_visible = False
    dialogue_timer_started = False
    dialogue_start_time = 0

    coffee_delivered = 0
    dragging_coffee = False
    drag_offset = (0, 0)
    dragged_coffee_pos = None
    dragged_coffee_index = None

    coffee_start_x = 25
    coffee_icon_height = full_cup_icon.get_height()
    coffee_icon_spacing = 10
    coffee_start_y = SCREEN_HEIGHT - 15

    steam_frame_interval = 500
    last_steam_switch = pygame.time.get_ticks()
    current_background = background1

    sparkle_active = False
    sparkle_start_time = 0
    sparkle_pos = (0, 0)

    pygame.mixer.music.load("sounds/jazz.wav")
    pygame.mixer.music.play(-1)

    current_raccoon_img = random.choice(raccoon_images)

    while True:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if now - last_steam_switch >= steam_frame_interval:
            current_background = background2 if current_background == background1 else background1
            last_steam_switch = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "start"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if trash_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    return "click"
                elif coffee_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    result, new_coffee_served, _ = coffee.run(screen, coffee_served, [], mouse_normal, mouse_clicked)
                    if result == "quit":
                        return "quit"
                    coffee_served = new_coffee_served
                    dragged_coffee_pos = None
                    dragged_coffee_index = None
                elif register_rect.collidepoint(event.pos):  # NEW
                    register_sound.play()
                else:
                    pile_rects = []
                    for i in range(coffee_served):
                        pos_x = coffee_start_x
                        pos_y = coffee_start_y - (coffee_icon_height + coffee_icon_spacing) * i - coffee_icon_height
                        rect = full_coffee_img.get_rect(topleft=(pos_x, pos_y))
                        pile_rects.append(rect)
                    for i, rect in enumerate(pile_rects):
                        if rect.collidepoint(event.pos) and coffee_served > 0:
                            click_sound.play()
                            dragging_coffee = True
                            dragged_coffee_pos = (rect.x, rect.y)
                            drag_offset = (event.pos[0] - rect.x, event.pos[1] - rect.y)
                            dragged_coffee_index = i
                            break
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging_coffee:
                    dragging_coffee = False
                    raccoon_rect = current_raccoon_img.get_rect(topleft=(raccoon_x, raccoon_y))
                    coffee_rect = full_coffee_img.get_rect(topleft=dragged_coffee_pos)
                    if raccoon_rect.colliderect(coffee_rect):
                        coffee_delivered += 1
                        coffee_served -= 1
                        sparkle_pos = (
                            raccoon_rect.centerx - sparkle_img.get_width() // 2,
                            raccoon_rect.top - sparkle_img.get_height() // 2,
                        )
                        sparkle_active = True
                        sparkle_start_time = pygame.time.get_ticks()
                        sparkle_sound.play()
                        dragged_coffee_pos = None
                        dragged_coffee_index = None
                    else:
                        dragged_coffee_pos = None
                        dragged_coffee_index = None

        if dragging_coffee and dragged_coffee_pos is not None:
            dragged_coffee_pos = (mouse_pos[0] - drag_offset[0], mouse_pos[1] - drag_offset[1])

        if not raccoon_arrived and not game_state.raccoon_sliding_out:
            raccoon_x += raccoon_speed
            if raccoon_x >= raccoon_target_x:
                raccoon_x = raccoon_target_x
                raccoon_arrived = True
                raccoon_sound.play()
                dialogue_timer_started = True
                dialogue_start_time = pygame.time.get_ticks()

        if game_state.raccoon_sliding_out:
            raccoon_x += raccoon_speed
            if raccoon_x > SCREEN_WIDTH:
                game_state.raccoon_sliding_out = False
                raccoon_arrived = False
                coffee_delivered = 0
                dialogue_visible = False
                dialogue_timer_started = False
                game_state.coffee_offer_number = random.choice([1, 2, 3])
                coffee_served = 0
                dragged_coffee_pos = None
                dragged_coffee_index = None
                raccoon_x = (SCREEN_WIDTH // 2) - 100
                dialogue_start_time = 0
                current_raccoon_img = random.choice(raccoon_images)

        screen.blit(current_background, (0, 0))

        # Trash
        if trash_rect.collidepoint(mouse_pos):
            bright_trash = trash_can_img.copy()
            bright_trash.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_trash, trash_rect.topleft)
        else:
            screen.blit(trash_can_img, trash_rect.topleft)

        # Coffee button
        if coffee_button_rect.collidepoint(mouse_pos):
            bright_button = coffee_button_img.copy()
            bright_button.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_button, coffee_button_rect.topleft)
        else:
            screen.blit(coffee_button_img, coffee_button_rect.topleft)

        # Register
        if register_rect.collidepoint(mouse_pos):
            bright_register = register_img.copy()
            bright_register.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_register, register_rect.topleft)
        else:
            screen.blit(register_img, register_rect.topleft)

        # Coffee pile
        for i in range(coffee_served):
            if dragging_coffee and i == dragged_coffee_index:
                continue
            pos_x = coffee_start_x
            pos_y = coffee_start_y - (coffee_icon_height + coffee_icon_spacing) * i - coffee_icon_height
            screen.blit(full_cup_icon, (pos_x, pos_y))

        # Raccoon
        screen.blit(current_raccoon_img, (raccoon_x, raccoon_y))

        if dragging_coffee and dragged_coffee_pos is not None:
            screen.blit(full_cup_icon, dragged_coffee_pos)

        raccoon_rect = current_raccoon_img.get_rect(topleft=(raccoon_x, raccoon_y))
        highlight_raccoon = False
        if dragging_coffee and dragged_coffee_pos is not None:
            dragged_coffee_rect = full_coffee_img.get_rect(topleft=dragged_coffee_pos)
            if raccoon_rect.colliderect(dragged_coffee_rect):
                highlight_raccoon = True
        if highlight_raccoon:
            bright_raccoon = current_raccoon_img.copy()
            bright_raccoon.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_raccoon, (raccoon_x, raccoon_y))

        if dialogue_timer_started and not dialogue_visible and not game_state.raccoon_sliding_out:
            if pygame.time.get_ticks() - dialogue_start_time >= 500:
                dialogue_visible = True

        if dialogue_visible and not game_state.raccoon_sliding_out:
            dialogue_rect = dialogue_img.get_rect(topright=(SCREEN_WIDTH - 20, 0))
            screen.blit(dialogue_img, dialogue_rect)
            icon_x = dialogue_rect.left + 60
            icon_y = dialogue_rect.centery - full_coffee_img.get_height() // 2 + 5
            screen.blit(full_coffee_img, (icon_x, icon_y))
            if game_state.coffee_offer_number is not None:
                number_text = font.render(f"X {game_state.coffee_offer_number}", True, (0, 0, 0))
                text_x = icon_x + full_coffee_img.get_width() + 15
                text_y = icon_y + full_coffee_img.get_height() // 2 - number_text.get_height() // 2
                screen.blit(number_text, (text_x, text_y))

        if (
            raccoon_arrived
            and game_state.coffee_offer_number is not None
            and coffee_delivered >= game_state.coffee_offer_number
        ):
            game_state.raccoon_sliding_out = True
            dialogue_visible = False

        if mouse_normal and mouse_clicked:
            if mouse_pressed:
                screen.blit(mouse_clicked, mouse_pos)
            else:
                screen.blit(mouse_normal, mouse_pos)

        if sparkle_active:
            if now - sparkle_start_time <= 1000:
                screen.blit(sparkle_img, sparkle_pos)
            else:
                sparkle_active = False

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    mouse_normal = pygame.image.load("images/mouse_normal.png").convert_alpha()
    mouse_clicked = pygame.image.load("images/mouse_clicked.png").convert_alpha()
    pygame.mouse.set_visible(False)
    result = run(screen, mouse_normal, mouse_clicked)
    print("Returned:", result)
    pygame.quit()
