import pygame
import time

def run(screen):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # Fonts (make sure pixel.ttf is in your fonts folder)
    font = pygame.font.Font("fonts/pixel.ttf", 80)
    small_font = pygame.font.Font("fonts/pixel.ttf", 36)

    # Background color and text
    background_color = (255, 230, 200)
    game_title = "Raccoon Café"
    subtitle = "loading..."

    # Track time
    start_time = pygame.time.get_ticks()

    while True:
        screen.fill(background_color)

        # Render title and subtitle
        title_surface = font.render(game_title, True, (0, 0, 0))
        subtitle_surface = small_font.render(subtitle, True, (100, 100, 100))

        screen.blit(title_surface, title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30)))
        screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40)))

        pygame.display.flip()
        clock.tick(60)

        # Wait for 2 seconds before transitioning to start screen
        if pygame.time.get_ticks() - start_time > 3000:
            return "start"

