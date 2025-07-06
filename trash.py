import pygame

trash_background = pygame.image.load("images/trash/trash_background.png")
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def run(screen):
    pygame.init()
    font = pygame.font.SysFont(None, 40)
    text = font.render("TRASH: Press ESC to return to Cafe", True, (0, 0, 0))
    clock = pygame.time.Clock()

    trash_icon = pygame.Rect(700, 20, 50, 50)

    # Bin layout setup: recycle in the center, compost 100px left, waste 100px right
    # Bin layout setup: recycle in the center, compost 100px left, waste 100px right
    bin_width, bin_height = 170, 50

    screen_width, screen_height = screen.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2 + 20  # vertical center

    # Bin positions
    recycle_bin = pygame.Rect(center_x - bin_width // 2, center_y - bin_height // 2, bin_width, bin_height)
    compost_bin = pygame.Rect(recycle_bin.left - 90 - bin_width, center_y - bin_height // 2, bin_width, bin_height)
    waste_bin = pygame.Rect(recycle_bin.right + 90, center_y - bin_height // 2, bin_width, bin_height)


    trash_items = []
    dragging_item = None

    while True:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False
        released = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "cafe"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                released = True

        if clicked and trash_icon.collidepoint(mouse_pos):
            new_trash = {
                "rect": pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, 50),
                "dragging": True,
                "returning": False
            }
            trash_items.append(new_trash)
            dragging_item = new_trash

        if dragging_item and dragging_item["dragging"]:
            dragging_item["rect"].center = mouse_pos

        if released and dragging_item:
            trash_rect = dragging_item["rect"]
            if (
                trash_rect.colliderect(compost_bin)
                or trash_rect.colliderect(recycle_bin)
                or trash_rect.colliderect(waste_bin)
            ):
                trash_items.remove(dragging_item)
            else:
                dragging_item["dragging"] = False
                dragging_item["returning"] = True
            dragging_item = None

        for trash in trash_items[:]:
            if trash["returning"]:
                tx, ty = trash_icon.center
                cx, cy = trash["rect"].center
                dx = tx - cx
                dy = ty - cy
                dist = (dx**2 + dy**2)**0.5

                if dist < 5:
                    trash["rect"].x = -100
                    trash["rect"].y = -100
                    trash["remove_timer"] = pygame.time.get_ticks() + 100
                else:
                    speed = 15
                    trash["rect"].centerx += int(speed * dx / dist)
                    trash["rect"].centery += int(speed * dy / dist)

        now = pygame.time.get_ticks()
        trash_items[:] = [
            trash for trash in trash_items
            if not ("remove_timer" in trash and now >= trash["remove_timer"])
        ]

        # --- Drawing ---
        screen.blit(trash_background, (0, 0))
        screen.blit(text, (50, 20))

        for trash in trash_items:
            if "remove_timer" in trash:
                continue
            pygame.draw.rect(screen, (120, 120, 120), trash["rect"])

        pygame.draw.rect(screen, (100, 100, 100), trash_icon)
        pygame.draw.line(screen, (0, 0, 0), trash_icon.topleft, trash_icon.bottomright, 2)
        pygame.draw.line(screen, (0, 0, 0), trash_icon.topright, trash_icon.bottomleft, 2)

        # Draw bins
        pygame.draw.rect(screen, (0, 0, 255), recycle_bin)  # Recycle - blue
        pygame.draw.rect(screen, (0, 255, 0), compost_bin)  # Compost - green
        pygame.draw.rect(screen, (255, 0, 0), waste_bin)    # Waste - red

        # Labels centered under each bin
        recycle_label = font.render("Recycle", True, (0, 0, 0))
        compost_label = font.render("Compost", True, (0, 0, 0))
        waste_label = font.render("Waste", True, (0, 0, 0))
        screen.blit(recycle_label, (recycle_bin.centerx - recycle_label.get_width() // 2, recycle_bin.bottom + 5))
        screen.blit(compost_label, (compost_bin.centerx - compost_label.get_width() // 2, compost_bin.bottom + 5))
        screen.blit(waste_label, (waste_bin.centerx - waste_label.get_width() // 2, waste_bin.bottom + 5))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()
