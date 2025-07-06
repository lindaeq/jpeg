import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

trash_icon = pygame.Rect(900, 20, 50, 50)

generated_trash = []
max_trash = 9
font = pygame.font.SysFont(None, 36)
dragging_item = None

running = True
while running:
    clicked = False
    released = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            released = True

    if clicked and trash_icon.collidepoint(mouse_pos) and len(generated_trash) < max_trash:
        spawn_x, spawn_y = trash_icon.centerx, trash_icon.bottom + 10
        new_trash = {
            "rect": pygame.Rect(spawn_x - 25, spawn_y - 25, 50, 50),
            "dragging": True,
            "returning": False
        }
        generated_trash.append(new_trash)
        dragging_item = new_trash

    if dragging_item and dragging_item["dragging"]:
        dragging_item["rect"].center = mouse_pos

    if released and dragging_item:
        dragging_item["dragging"] = False
        dragging_item = None

    screen.fill((240, 240, 240))
    pygame.draw.rect(screen, (80, 80, 80), trash_icon)
    pygame.draw.line(screen, (0, 0, 0), trash_icon.topleft, trash_icon.bottomright, 2)
    pygame.draw.line(screen, (0, 0, 0), trash_icon.topright, trash_icon.bottomleft, 2)

    for t in generated_trash:
        pygame.draw.rect(screen, (150, 50, 50), t["rect"])

    label = font.render(f"Trash count: {len(generated_trash)}", True, (0, 0, 0))
    screen.blit(label, (700, 80))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# For testing as standalone file
if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()
    sys.exit()