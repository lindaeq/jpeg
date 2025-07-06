import pygame
import random
import game_state

pygame.init()
pygame.font.init()

# Load assets
trash_background = pygame.image.load("images/trash/trash_background.png")
trash1_img = pygame.image.load("images/trash/trash1.jpg")
trash2_img = pygame.image.load("images/trash/trash2.JPG")
trash3_img = pygame.image.load("images/trash/trash3.jpg")

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

    trash_icon = pygame.Rect(900, 20, 50, 50)
    # score = 0  ❌ Removed to avoid shadowing game_state.score
    max_trash = 9
    sorted_count = 0

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
        mouse_pressed = pygame.mouse.get_pressed()[0]  # ✅ Custom cursor logic

        # ✅ Relaxed icon_clear logic
        icon_clear = all(
            not t["rect"].colliderect(trash_icon) or t.get("returning") or "remove_timer" in t
            for t in trash_items
        )

        active_trash_count = sum(1 for t in trash_items if not t.get("returning") and "remove_timer" not in t)

        if clicked and trash_icon.collidepoint(mouse_pos) and active_trash_count + sorted_count < max_trash and icon_clear:
            trash_type = random.choice(["trash1", "trash2", "trash3"])
            spawn_x, spawn_y = trash_icon.centerx, trash_icon.bottom + 10
            new_trash = {
                "rect": pygame.Rect(spawn_x - 25, spawn_y - 25, 50, 50),
                "type": trash_type,
                "dragging": True,
                "returning": False
            }
            trash_items.append(new_trash)
            dragging_item = new_trash

        if dragging_item and dragging_item["dragging"]:
            dragging_item["rect"].center = mouse_pos

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
                sorted_count += 1
                game_state.score += 1
            else:
                t["dragging"] = False
                t["returning"] = True
            dragging_item = None

        for t in trash_items[:]:
            if t["returning"]:
                tx, ty = trash_icon.center
                cx, cy = t["rect"].center
                dx, dy = tx - cx, ty - cy
                dist = (dx**2 + dy**2)**0.5
                if dist < 5:
                    t["rect"].x, t["rect"].y = -100, -100
                    t["remove_timer"] = pygame.time.get_ticks() + 100
                else:
                    speed = 15
                    t["rect"].centerx += int(speed * dx / dist)
                    t["rect"].centery += int(speed * dy / dist)

        # ✅ Emergency cleanup for stuck trash
        now = pygame.time.get_ticks()
        for t in trash_items:
            if t.get("returning") and t["rect"].x < -80 and t["rect"].y < -80:
                t["remove_timer"] = now + 50

        trash_items[:] = [t for t in trash_items if not ("remove_timer" in t and now >= t["remove_timer"])]

        if clicked and sorted_count == max_trash and button_rect.collidepoint(mouse_pos):
            return "cafe"

        # --- Draw ---
        screen.blit(trash_background, (0, 0))

        score_label = font.render(f"Points: {game_state.score}", True, (0, 0, 0))
        screen.blit(score_label, (trash_icon.x - 20, trash_icon.bottom + 5))

        # Trash icon
        pygame.draw.rect(screen, (100, 100, 100), trash_icon)
        pygame.draw.line(screen, (0, 0, 0), trash_icon.topleft, trash_icon.bottomright, 2)
        pygame.draw.line(screen, (0, 0, 0), trash_icon.topright, trash_icon.bottomleft, 2)

        # Bin highlight
        def get_bin_color(bin_rect):
            if dragging_item and dragging_item["rect"].colliderect(bin_rect):
                return (80, 80, 80)
            return (0, 0, 0)

        pygame.draw.rect(screen, get_bin_color(recycle_bin), recycle_bin)
        pygame.draw.rect(screen, get_bin_color(compost_bin), compost_bin)
        pygame.draw.rect(screen, get_bin_color(waste_bin), waste_bin)

        for t in trash_items:
            if "remove_timer" in t:
                continue
            img = TRASH_IMAGES[t["type"]]
            screen.blit(img, t["rect"])

        if sorted_count == max_trash:
            pygame.draw.rect(screen, (0, 150, 0), button_rect)
            screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # ✅ Draw custom mouse cursor
        if mouse_normal and mouse_clicked:
            if mouse_pressed:
                screen.blit(mouse_clicked, mouse_pos)
            else:
                screen.blit(mouse_normal, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()