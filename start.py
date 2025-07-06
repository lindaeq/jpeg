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
    font = pygame.font.SysFont(None, 48)  # You can still keep this if needed elsewhere
    # Use pixel font for button text
    pixel_font = pygame.font.Font("fonts/pixel.ttf", 36)
    clock = pygame.time.Clock()

    button_color = (180, 80, 80)
    hover_color = (200, 100, 100)

    # Button at bottom center with margin 40px
    button_width, button_height = 200, 60
    button_x = (SCREEN_WIDTH - button_width - 700)
    button_y = SCREEN_HEIGHT - button_height - 40
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    button_text = pixel_font.render("Go to Cafe", True, (255, 255, 255))

    cursor_offset_x = 0
    cursor_offset_y = 0

    frame_timer = 0
    frame_delay = 500  # milliseconds between background frames
    current_frame = 0
    backgrounds = [background, background1]

    while True:
        dt = clock.tick(60)  # milliseconds since last frame
        frame_timer += dt

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return "cafe"

        # Switch background frame every frame_delay milliseconds
        if frame_timer >= frame_delay:
            current_frame = (current_frame + 1) % len(backgrounds)
            frame_timer = 0

        # Draw current background frame
        screen.blit(backgrounds[current_frame], (0, 0))

        # Draw button with hover effect
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        # Draw custom cursor on top
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
