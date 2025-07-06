import pygame
import random
import game_state

pygame.init()
pygame.font.init()

# Load assets
trash_background = pygame.image.load("images/trash/trash_background.png")
trash1_img = pygame.image.load("images/trash/trash1.png")
trash2_img = pygame.image.load("images/trash/trash2.JPG")
trash3_img = pygame.image.load("images/trash/trash3.jpg")
trash_icon_img = pygame.image.load("images/trash/trash_icon.png").convert_alpha()

TRASH_IMAGES = {
    "trash1": trash1_img,
    "trash2": trash2_img,
    "trash3": trash3_img
}

TRASH_SIZE = (50, 50)
for key in TRASH_IMAGES:
    TRASH_IMAGES[key] = pygame.transform.scale(TRASH_IMAGES[key], TRASH_SIZE)

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def run(screen, mouse_normal=None, mouse_clicked=None):
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    trash_icon_rect = trash_icon_img.get_rect(topleft=(900, 20))
    max_trash = game_state.raccoons_served + 2  # Dynamic max_trash based on game_state
    round_start_score = game_state.score

    # Bin setup
    bin_width, bin_height = 175, 50
    screen_width, screen_height = screen.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2 - 80

    recycle_bin = pygame.Rect(center_x - bin_width // 2 + 20, center_y - bin_height // 2, bin_width, bin_height)
    compost_bin = pygame.Rect(recycle_bin.left - 150 - bin_width + 55, center_y - bin_height // 2, bin_width, bin_height)
    waste_bin = pygame.Rect(recycle_bin.right + 150 + 40 - 100, center_y - bin_height // 2, bin_width, bin_height)

    trash_items = []
    dragging_item = None

    button_font = pygame.font.SysFont(None, 50)
    button_text = button_font.render("Back to Cafe", True, (255, 255, 255))
    button_rect = pygame.Rect((screen_width // 2) - 100, 500, 200, 60)

    def brighten_image(surface):
        bright = surface.copy()
        bright.fill((30, 30, 30, 0), special_flags=pygame.BLEND_RGB_ADD)
        return bright

    while True:
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

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        pieces_sorted_this_round = game_state.score - round_start_score

        icon_clear = all(
            not t["rect"].colliderect(trash_icon_rect) or t.get("returning") or "remove_timer" in t
            for t in trash_items
        )

        active_trash_count = sum(1 for t in trash_items if not t.get("returning") and "remove_timer" not in t)

        # Spawn new trash piece
        if clicked and trash_icon_rect.collidepoint(mouse_pos) and pieces_sorted_this_round + active_trash_count < max_trash and icon_clear:
            trash_type = random.choice(["trash1", "trash2", "trash3"])
            spawn_x, spawn_y = trash_icon_rect.centerx, trash_icon_rect.bottom + 10
            new_trash = {
                "rect": pygame.Rect(spawn_x - 25, spawn_y - 25, 50, 50),
                "type": trash_type,
                "dragging": True,
                "returning": False
            }
            trash_items.append(new_trash)
            dragging_item = new_trash

        # Dragging logic
        if dragging_item and dragging_item["dragging"]:
            dragging_item["rect"].center = mouse_pos

        # Drop logic
        if released and dragging_item:
            t = dragging_item
            trash_type = t["type"]
            rect = t["rect"]
            correct = (
                (trash_type == "trash1" and rect.colliderect(compost_bin)) or
                (trash_type == "trash2" and rect.colliderect(recycle_bin)) or
                (trash_type == "trash3" and rect.colliderect(waste_bin))
            )
            if correct:
                trash_items.remove(t)
                game_state.score += 1
            else:
                t["dragging"] = False
                t["returning"] = True
            dragging_item = None

        # Return animation for wrong drops
        for t in trash_items[:]:
            if t.get("returning"):
                tx, ty = trash_icon_rect.center
                cx, cy = t["rect"].center
                dx, dy = tx - cx, ty - cy
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist < 5:
                    t["rect"].x, t["rect"].y = -100, -100
                    t["remove_timer"] = pygame.time.get_ticks() + 100
                else:
                    speed = 15
                    t["rect"].centerx += int(speed * dx / dist)
                    t["rect"].centery += int(speed * dy / dist)

        now = pygame.time.get_ticks()
        for t in trash_items:
            if t.get("returning") and t["rect"].x < -80 and t["rect"].y < -80:
                t["remove_timer"] = now + 50

        trash_items[:] = [t for t in trash_items if not ("remove_timer" in t and now >= t["remove_timer"])]

        # Back to Cafe button logic
        if clicked and pieces_sorted_this_round == max_trash and button_rect.collidepoint(mouse_pos):
            return "cafe"

        # --- Draw section ---
        screen.blit(trash_background, (0, 0))

        # Draw score
        score_label = font.render(f"Points: {game_state.score}", True, (0, 0, 0))
        screen.blit(score_label, (trash_icon_rect.x - 20, trash_icon_rect.bottom + 5))

        # Draw trash icon image (with optional hover effect)
        icon_img = brighten_image(trash_icon_img) if trash_icon_rect.collidepoint(mouse_pos) else trash_icon_img
        screen.blit(icon_img, trash_icon_rect.topleft)

        # Function for bin hover color
        def get_bin_color(bin_rect):
            if dragging_item and dragging_item["rect"].colliderect(bin_rect):
                return (80, 80, 80)
            if bin_rect.collidepoint(mouse_pos):
                return (150, 150, 150)
            return (0, 0, 0)

        pygame.draw.rect(screen, get_bin_color(recycle_bin), recycle_bin)
        pygame.draw.rect(screen, get_bin_color(compost_bin), compost_bin)
        pygame.draw.rect(screen, get_bin_color(waste_bin), waste_bin)

        # Draw trash items
        for t in trash_items:
            if "remove_timer" in t:
                continue
            img = TRASH_IMAGES[t["type"]]
            screen.blit(img, t["rect"])

        # Draw "Back to Cafe" button
        if pieces_sorted_this_round == max_trash:
            pygame.draw.rect(screen, (0, 150, 0), button_rect)
            screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Custom mouse cursor
        if mouse_normal and mouse_clicked:
            screen.blit(mouse_clicked if mouse_pressed else mouse_normal, mouse_pos)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()
