import pygame

cafe_background = pygame.image.load("images/cafe.png")

def run(screen):
    font = pygame.font.SysFont(None, 40)
    text = font.render("CAFE: Press C for coffee, T for trash", True, (0, 0, 0))
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

        screen.blit(cafe_background, (0,0))
        

        pygame.display.flip()
        clock.tick(60)
