import pygame
import random

pygame.mixer.init()

click_sound = pygame.mixer.Sound("sounds/click.mp3")
trash_click_sound = pygame.mixer.Sound("sounds/trash_click.mp3")
quack_sound = pygame.mixer.Sound("sounds/quack.mp3")

# Load trash image
trash_img = pygame.image.load("images/click_screen/trashbag.jpg")
trash_img = pygame.transform.scale(trash_img, (30, 30))

def run(screen, mouse_normal=None, mouse_clicked=None):
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Define central spawn box
    box_margin_x = 100
    box_margin_bottom = 100
    box_margin_top = 150

    box_width = screen.get_width() - 2 * box_margin_x
    box_height = screen.get_height() - box_margin_bottom - box_margin_top
    box_x = box_margin_x
    box_y = box_margin_top
    spawn_area = pygame.Rect(box_x, box_y, box_width, box_height)

    # Trash setup
    num_trash = random.randint(5, 10)
    trash_items = []
    for _ in range(num_trash):
        x = random.randint(spawn_area.left, spawn_area.right - 30)
        y = random.randint(spawn_area.top, spawn_area.bottom - 30)
        rect = pygame.Rect(x, y, 30, 30)
        trash_items.append({"rect": rect, "img": trash_img})

    trash_collected = 0
    button_visible = False
    button_rect = pygame.Rect(650, 80, 120, 40)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # ✅ Correct cursor logic

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "cafe"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check trash
                for trash in trash_items[:]:
                    if trash["rect"].collidepoint(mouse_pos):
                        trash_items.remove(trash)
                        trash_click_sound.play()
                        trash_collected += 1
                        break

                # Check sort button
                if button_visible and button_rect.collidepoint(mouse_pos):
                    return "trash"

        if trash_collected == num_trash:
            button_visible = True

        screen.fill((200, 200, 250))
        pygame.draw.rect(screen, (180, 180, 220), spawn_area, 2)

        # Instructions
        text = font.render("Click Trash! Press ESC to return", True, (0, 0, 0))
        screen.blit(text, (100, 30))

        # Trash counter
        counter_text = small_font.render(f"Trash: {trash_collected}/{num_trash}", True, (0, 0, 0))
        screen.blit(counter_text, (650, 30))

        # Trash items
        for trash in trash_items:
            screen.blit(trash["img"], trash["rect"])

        # Sort Trash button
        if button_visible:
            pygame.draw.rect(screen, (0, 200, 0), button_rect)
            button_text = small_font.render("Sort Trash", True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)

        # ✅ Custom mouse cursor
        if mouse_normal and mouse_clicked:
            if mouse_pressed:
                screen.blit(mouse_clicked, mouse_pos)
            else:
                screen.blit(mouse_normal, mouse_pos)

        pygame.display.flip()
        clock.tick(60)
