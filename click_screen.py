import pygame
import random

def run(screen):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Trash setup
    num_trash = random.randint(5, 10)
    trash_items = []
    for _ in range(num_trash):
        x = random.randint(50, 700)
        y = random.randint(100, 500)
        rect = pygame.Rect(x, y, 30, 30)
        trash_items.append(rect)

    # Trash counter
    trash_collected = 0

    # Sort Trash button setup
    button_visible = False
    button_rect = pygame.Rect(650, 80, 120, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "cafe"  # Go back to cafe

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Check if clicking trash
                for trash in trash_items[:]:
                    if trash.collidepoint(mouse_pos):
                        trash_items.remove(trash)
                        trash_collected += 1
                        break

                # Check if clicking the button
                if button_visible and button_rect.collidepoint(mouse_pos):
                    return "trash"  # Switch to trash sorting screen

        # If all trash is collected, show the button
        if trash_collected == num_trash:
            button_visible = True

        # Draw screen
        screen.fill((200, 200, 250))  # light blue

        # Instruction text
        text = font.render("Click Trash! Press ESC to return", True, (0, 0, 0))
        screen.blit(text, (100, 30))

        # Trash counter
        counter_text = small_font.render(f"Trash: {trash_collected}/{num_trash}", True, (0, 0, 0))
        screen.blit(counter_text, (650, 30))

        # Draw trash items
        for trash in trash_items:
            pygame.draw.rect(screen, (100, 100, 100), trash)

        # Draw "Sort Trash" button
        if button_visible:
            pygame.draw.rect(screen, (0, 200, 0), button_rect)
            button_text = small_font.render("Sort Trash", True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)

        pygame.display.flip()
        clock.tick(60)