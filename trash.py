import pygame

def run(screen):
    pygame.init()
    font = pygame.font.SysFont(None, 40)
    text = font.render("TRASH: Press ESC to return to Cafe", True, (0, 0, 0))
    clock = pygame.time.Clock()

    # Trash icon location (fixed)
    trash_icon = pygame.Rect(700, 20, 50, 50)

    # Trash pieces
    trash_items = []

    # Bins
    compost_bin = pygame.Rect(100, 500, 100, 80)
    recycle_bin = pygame.Rect(300, 500, 100, 80)
    waste_bin = pygame.Rect(500, 500, 100, 80)

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

        # Dragging a new trash piece from the icon
        if clicked and trash_icon.collidepoint(mouse_pos):
            new_trash = {
                "rect": pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, 50),
                "dragging": True,
                "returning": False
            }
            trash_items.append(new_trash)
            dragging_item = new_trash

        # Update dragging
        if dragging_item and dragging_item["dragging"]:
            dragging_item["rect"].center = mouse_pos

        # On release
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

        # Update returning trash items
        for trash in trash_items[:]:  # copy the list to avoid modifying while looping
            if trash["returning"]:
                # Move it toward the trash icon
                tx, ty = trash_icon.center
                cx, cy = trash["rect"].center
                dx = tx - cx
                dy = ty - cy
                dist = (dx**2 + dy**2)**0.5

                if dist < 5:
                    # Move it off-screen and schedule removal
                    trash["rect"].x = -100
                    trash["rect"].y = -100
                    trash["remove_timer"] = pygame.time.get_ticks() + 100  # remove after 100ms
                else:
                    speed = 15
                    trash["rect"].centerx += int(speed * dx / dist)
                    trash["rect"].centery += int(speed * dy / dist)

        # Final cleanup of trash pieces whose remove_timer has expired
        now = pygame.time.get_ticks()
        trash_items[:] = [
            trash for trash in trash_items
            if not ("remove_timer" in trash and now >= trash["remove_timer"])
        ]

        # Draw
        screen.fill((200, 200, 200))
        screen.blit(text, (50, 20))

        # Trash items
        for trash in trash_items:
            if "remove_timer" in trash:
                continue  # Don't draw items scheduled for removal
            pygame.draw.rect(screen, (120, 120, 120), trash["rect"])

        # Draw trash icon *after* trash items so it stays on top
        pygame.draw.rect(screen, (100, 100, 100), trash_icon)
        pygame.draw.line(screen, (0, 0, 0), trash_icon.topleft, trash_icon.bottomright, 2)
        pygame.draw.line(screen, (0, 0, 0), trash_icon.topright, trash_icon.bottomleft, 2)


        # Bins
        pygame.draw.rect(screen, (0, 255, 0), compost_bin)
        pygame.draw.rect(screen, (0, 0, 255), recycle_bin)
        pygame.draw.rect(screen, (255, 0, 0), waste_bin)

        # Labels
        compost_label = font.render("Compost", True, (0, 0, 0))
        recycle_label = font.render("Recycle", True, (0, 0, 0))
        waste_label = font.render("Waste", True, (0, 0, 0))
        screen.blit(compost_label, (compost_bin.x + 5, compost_bin.y + 25))
        screen.blit(recycle_label, (recycle_bin.x + 5, recycle_bin.y + 25))
        screen.blit(waste_label, (waste_bin.x + 5, waste_bin.y + 25))

        pygame.display.flip()
        clock.tick(60)
