import pygame
import random

pygame.mixer.init()

click_sound = pygame.mixer.Sound("sounds/click.mp3")
trash_click_sound = pygame.mixer.Sound("sounds/trash_click.mp3")
quack_sound = pygame.mixer.Sound("sounds/quack.mp3")

trash_background = pygame.image.load("images/click_screen/trash_bag.png")

# Load and scale all trash images
TRASH_IMAGES = {
    "trash1": pygame.image.load("images/click_screen/trash1.jpg"),
    "trash2": pygame.image.load("images/click_screen/trash2.png"),
    "trash3": pygame.image.load("images/click_screen/trash3.png")
}

magnify_factor = 1.2
TRASH_SCALED = {}

# Scale all trash images once
for key, img in TRASH_IMAGES.items():
    original_size = img.get_size()
    scaled_size = (int(original_size[0] * magnify_factor), int(original_size[1] * magnify_factor))
    TRASH_SCALED[key] = pygame.transform.scale(img, scaled_size)

trash_width, trash_height = list(TRASH_SCALED.values())[0].get_size()  # Assume same size for collision purposes

def run(screen, mouse_normal=None, mouse_clicked=None):
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.Font("fonts/pixel_2.ttf", 36)
    clock = pygame.time.Clock()

    # Start looping background music
    pygame.mixer.music.load("sounds/buzz.wav")
    pygame.mixer.music.play(-1)

    # Define spawn area
    box_margin_x = 100
    box_margin_bottom = 150
    box_margin_top = 150
    box_width = screen.get_width() - 2 * box_margin_x
    box_height = screen.get_height() - box_margin_bottom - box_margin_top
    spawn_area = pygame.Rect(box_margin_x, box_margin_top, box_width, box_height)

    # Determine total number of trash items
    total_trash_items = random.randint(3, 8)
    types = ["trash1", "trash2", "trash3"]
    counts = [0, 0, 0]

    # Randomly assign total_trash_items into the three categories
    for _ in range(total_trash_items):
        choice = random.choice([0, 1, 2])
        counts[choice] += 1

    trash_items = []
    attempts = 0
    max_attempts = 500
    spacing = 5

    # Spawn trash items with rotation
    for i, count in enumerate(counts):
        trash_type = types[i]
        for _ in range(count):
            while attempts < max_attempts:
                x = random.randint(spawn_area.left, spawn_area.right - trash_width)
                y = random.randint(spawn_area.top, spawn_area.bottom - trash_height)
                new_rect = pygame.Rect(x, y, trash_width, trash_height)

                if not any(new_rect.colliderect(t["rect"].inflate(spacing, spacing)) for t in trash_items):
                    angle = random.randint(0, 360)
                    base_img = TRASH_SCALED[trash_type]
                    rotated_img = pygame.transform.rotate(base_img, angle)
                    rotated_rect = rotated_img.get_rect(center=new_rect.center)
                    trash_items.append({"rect": rotated_rect, "img": rotated_img})
                    break

                attempts += 1

    total_trash = len(trash_items)
    trash_collected = 0
    show_continue_text = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "cafe"
                if show_continue_text:
                    return "trash"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for trash in trash_items[:]:
                    if trash["rect"].collidepoint(mouse_pos):
                        trash_items.remove(trash)
                        trash_click_sound.play()
                        trash_collected += 1
                        break

        if trash_collected == total_trash:
            show_continue_text = True

        screen.blit(trash_background, (0, 0))

        # Trash counter
        counter_text = small_font.render(f"Trash: {trash_collected}/{total_trash}", True, (0, 0, 0))
        screen.blit(counter_text, (650, 30))

        # Trash items
        for trash in trash_items:
            screen.blit(trash["img"], trash["rect"])

        # Continue message
        if show_continue_text:
            continue_text = small_font.render("press any key to continue...", True, (255, 255, 255))
            text_rect = continue_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(continue_text, text_rect)

        # Custom cursor
        if mouse_normal and mouse_clicked:
            screen.blit(mouse_clicked if mouse_pressed else mouse_normal, mouse_pos)

        pygame.display.flip()
        clock.tick(60)
