import pygame
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Load and play background jazz music ONCE
pygame.mixer.music.load("sounds/jazz.wav")
pygame.mixer.music.play(-1)  # Loop forever

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Screen")

mouse_normal = pygame.image.load("images/mouse_normal.png").convert_alpha()
mouse_clicked = pygame.image.load("images/mouse_clicked.png").convert_alpha()
pygame.mouse.set_visible(False)

# Load both background frames
background = pygame.image.load("images/start/background.png").convert()
background1 = pygame.image.load("images/start/background1.png").convert()

def run(screen, mouse_normal, mouse_clicked):
    pixel_font = pygame.font.Font("fonts/pixel.ttf", 36)
    clock = pygame.time.Clock()

    cursor_offset_x = 0
    cursor_offset_y = 0

    frame_timer = 0
    frame_delay = 500  # milliseconds between background frames
    current_frame = 0
    backgrounds = [background, background1]

    # Centered horizontally, 50px lower than original button

    while True:
        dt = clock.tick(60)
        frame_timer += dt

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                return "cafe"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return "cafe"

        # Switch background frame
        if frame_timer >= frame_delay:
            current_frame = (current_frame + 1) % len(backgrounds)
            frame_timer = 0

        # Draw background
        screen.blit(backgrounds[current_frame], (0, 0))

        # Draw prompt text
        # Custom mouse
        if mouse_pressed:
            screen.blit(mouse_clicked, (mouse_pos[0] - cursor_offset_x, mouse_pos[1] - cursor_offset_y))
        else:
            screen.blit(mouse_normal, (mouse_pos[0] - cursor_offset_x, mouse_pos[1] - cursor_offset_y))

        pygame.display.flip()


if __name__ == "__main__":
    result = run(screen, mouse_normal, mouse_clicked)
    print("Returned:", result)
    pygame.quit()
    sys.exit()
