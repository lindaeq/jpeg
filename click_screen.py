import pygame
import random

pygame.mixer.init()

click_sound = pygame.mixer.Sound("sounds/click.mp3")
trash_click_sound = pygame.mixer.Sound("sounds/trash_click.mp3")
quack_sound = pygame.mixer.Sound("sounds/quack.mp3")

trash_background = pygame.image.load("images/click_screen/trash_bag.png")

# Load and magnify trash image
trash_img = pygame.image.load("images/click_screen/trash1.jpg")
magnify_factor = 1.2
original_size = trash_img.get_size()
scaled_size = (int(original_size[0] * magnify_factor), int(original_size[1] * magnify_factor))
trash_img = pygame.transform.scale(trash_img, scaled_size)

trash_width, trash_height = scaled_size

def run(screen, mouse_normal=None, mouse_clicked=None):
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.Font("fonts/pixel.ttf", 36)
    clock = pygame.time.Clock()

    # Start looping background music
    pygame.mixer.music.load("sounds/buzz.wav")  # your background music file
    pygame.mixer.music.play(-1)

    # Spawn box
    box_margin_x = 100
    box_margin_bottom = 150
    box_margin_top = 150

    box_width = screen.get_width() - 2 * box_margin_x
    box_height = screen.get_height() - box_margin_bottom - box_margin_top
    spawn_area = pygame.Rect(box_margin_x, box_margin_top, box_width, box_height)

    num_trash = random.randint(3, 7)
    trash_items = []
    attempts = 0
    max_attempts = 500
    spacing = 5

    while len(trash_items) < num_trash and attempts < max_attempts:
        x = random.randint(spawn_area.left, spawn_area.right - trash_width)
        y = random.randint(spawn_area.top, spawn_area.bottom - trash_height)
        new_rect = pygame.Rect(x, y, trash_width, trash_height)
        if not any(new_rect.colliderect(t["rect"].inflate(spacing, spacing)) for t in trash_items):
            trash_items.append({"rect": new_rect, "img": trash_img})
        attempts += 1

    # ✅ Track original total number of trash items
    total_trash = len(trash_items)

    trash_collected = 0
    button_visible = False
    button_rect = pygame.Rect(450, 200, 200, 100)  # Moved button higher

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "cafe"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for trash in trash_items[:]:
                    if trash["rect"].collidepoint(mouse_pos):
                        trash_items.remove(trash)
                        trash_click_sound.play()
                        trash_collected += 1
                        break
                if button_visible and button_rect.collidepoint(mouse_pos):
                    return "trash"

        # ✅ Check against total_trash, not length of trash_items
        if trash_collected == total_trash:
            button_visible = True

        screen.blit(trash_background, (0, 0))

        # Trash counter
        counter_text = small_font.render(f"Trash: {trash_collected}/{total_trash}", True, (0, 0, 0))
        screen.blit(counter_text, (650, 30))

        # Trash items
        for trash in trash_items:
            screen.blit(trash["img"], trash["rect"])

        # Draw button if visible
        if button_visible:
            pygame.draw.rect(screen, (242, 179, 199), button_rect)
            pygame.draw.rect(screen, (100, 100, 100), button_rect, 2)  # Thin border
            button_text = small_font.render("Sort Trash", True, (0, 0, 0))
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)

        # Custom cursor
        if mouse_normal and mouse_clicked:
            screen.blit(mouse_clicked if mouse_pressed else mouse_normal, mouse_pos)

        pygame.display.flip()
        clock.tick(60)
