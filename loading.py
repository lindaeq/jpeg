import pygame
import time

def run(screen):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # Initialize mixer and play jazz music in loop
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/jazz.wav")
    pygame.mixer.music.play(-1)  # Loop forever

    # Load one-shot rain sound
    rain_channel = pygame.mixer.Channel(1)
    rain_sound = pygame.mixer.Sound("sounds/rain.mp3")
    rain_channel.play(rain_sound)

    # Fonts
    font = pygame.font.Font("fonts/pixel.ttf", 80)
    small_font = pygame.font.Font("fonts/pixel.ttf", 36)

    # Load background frames
    loading_bg1 = pygame.image.load("images/loading/loading_background.png").convert()
    loading_bg2 = pygame.image.load("images/loading/loading_background1.png").convert()
    backgrounds = [loading_bg1, loading_bg2]
    current_bg_index = 0

    # Load rain frames
    rain1 = pygame.image.load("images/loading/rain.png").convert_alpha()
    rain2 = pygame.image.load("images/loading/rain1.png").convert_alpha()
    rains = [rain1, rain2]
    current_rain_index = 0

    # Animation timer
    switch_interval = 500  # milliseconds
    last_switch_time = pygame.time.get_ticks()

    # Track time
    start_time = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()

        # Check for keypress to exit early
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                rain_channel.stop()
                return "start"

        # Alternate background and rain every 500 ms
        if now - last_switch_time >= switch_interval:
            current_bg_index = (current_bg_index + 1) % len(backgrounds)
            current_rain_index = (current_rain_index + 1) % len(rains)
            last_switch_time = now

        # Draw background
        screen.blit(backgrounds[current_bg_index], (0, 0))

        # Draw rain on top
        screen.blit(rains[current_rain_index], (0, 0))

        pygame.display.flip()
        clock.tick(60)

        # Wait for 3 seconds then transition
        if now - start_time > 3000:
            rain_channel.stop()
            return "start"
