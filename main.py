import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Event Logger")

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            print(event)  # Python 3 requires parentheses for print

    screen.fill((120, 120, 120))
    pygame.display.flip()

pygame.quit()
