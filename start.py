import pygame

# images
background = pygame.image.load("images/background.png")

def run(screen):
    font = pygame.font.SysFont(None, 48)

    button_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Button setup
    button_color = (180, 80, 80)
    hover_color = (200, 100, 100)
    button_rect = pygame.Rect(50, 300, 200, 60)
    button_text = button_font.render("Go to Cafe", True, (255, 255, 255))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        # Fill screen
        screen.fill((200, 230, 255))

        # Draw button
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect)
            if clicked:
                return "cafe"
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        pygame.display.flip()
        clock.tick(60)
