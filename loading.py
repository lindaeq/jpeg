import pygame
import time

def run(screen):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # Fonts
    font = pygame.font.Font("fonts/pixel.ttf", 80)
    small_font = pygame.font.Font("fonts/pixel.ttf", 36)

    # ✅ Load background image
    loading_background = pygame.image.load("images/loading/loading_background.png").convert()

    # Text content
    game_title = "Raccoon Café"
    subtitle = "loading..."

    # Track time
    start_time = pygame.time.get_ticks()

    while True:
        # ✅ Draw background image
        screen.blit(loading_background, (0, 0))

        # Render title and subtitle
    
        pygame.display.flip()
        clock.tick(60)

        # Wait for 3 seconds before transitioning to start screen
        if pygame.time.get_ticks() - start_time > 3000:
            return "start"
