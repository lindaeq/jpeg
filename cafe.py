import pygame
import coffee  # Make sure this is the correct filename (coffee.py)

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()
pygame.font.init()

def run(screen):
    background = pygame.image.load("images/cafe/cafe.png").convert()
    trash_can_img = pygame.image.load("images/cafe/trash_can.png").convert_alpha()
    coffee_button_img = pygame.image.load("images/cafe/button_coffee_machine.png").convert_alpha()

    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    trash_rect = trash_can_img.get_rect(topleft=(0, (screen.get_height() - trash_can_img.get_height()) // 2 - 25))
    coffee_button_pos = (675, SCREEN_HEIGHT - coffee_button_img.get_height() - 120)
    coffee_button_rect = coffee_button_img.get_rect(topleft=coffee_button_pos)

    coffee_served = 0
    coffee_icons = []

    while True:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "start"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        screen.blit(background, (0, 0))

        if trash_rect.collidepoint(mouse_pos):
            bright_trash = trash_can_img.copy()
            bright_trash.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_trash, trash_rect.topleft)
            if clicked:
                return "click"
        else:
            screen.blit(trash_can_img, trash_rect.topleft)

        if coffee_button_rect.collidepoint(mouse_pos):
            bright_button = coffee_button_img.copy()
            bright_button.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(bright_button, coffee_button_rect.topleft)
            if clicked:
                result, coffee_served, coffee_icons = coffee.run(screen, coffee_served, coffee_icons)
                if result == "quit":
                    return "quit"
        else:
            screen.blit(coffee_button_img, coffee_button_rect.topleft)

        text = font.render("Click Trash or Coffee Machine. ESC to return.", True, (0, 0, 0))
        screen.blit(text, (50, 30))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    result = run(screen)
    print("Returned:", result)
    pygame.quit()