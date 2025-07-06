import pygame

def run(screen):
    # Load background image
    background = pygame.image.load("images/cafe/cafe.png").convert()
    
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return "coffee"
                if event.key == pygame.K_t:
                    return "trash"
                if event.key == pygame.K_k:
                    return "click"
                if event.key == pygame.K_ESCAPE:
                    return "start"

        # Draw background
        screen.blit(background, (0, 0))

        # Optional: show instruction text
        text = font.render("Press C (Coffee), T (Trash), or K (Click). ESC to return.", True, (0, 0, 0))
        screen.blit(text, (50, 30))

        pygame.display.flip()
        clock.tick(60)
