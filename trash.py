import pygame

def run(screen):
    font = pygame.font.SysFont(None, 40)
    text = font.render("TRASH: Press ESC to return to Cafe", True, (0, 0, 0))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "cafe"

        screen.fill((200, 200, 200))
        screen.blit(text, (50, 200))
        pygame.display.flip()
        clock.tick(60)
