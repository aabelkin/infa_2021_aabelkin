import pygame
from pygame.draw import *
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 550))
rect(screen, (255, 255, 255), (0, 0, 400, 550))

def draw_background():
    rect(screen, (192, 192, 192), (0, 0, 400, 245))
    ellipse(screen, (70, 70, 70), (0, 0, 500, 50))
    rect(screen, (100, 100, 100), (55, 5, 80, 250))
    rect(screen, (40, 40, 40), (150, 15, 80, 250))
    rect(screen, (24, 24, 24), (90, 50, 80, 250))
    rect(screen, (50, 50, 50), (315, 5, 80, 250))
    rect(screen, (90, 90, 90), (270, 60, 80, 250))
    rect(screen, (184, 197, 201), (0, 100, 400, 245))
    rect(screen, (82, 108, 113), (0, 350, 400, 200))
    rect(screen, (148, 169, 174), (5, 105, 80, 250))
    rect(screen, (148, 174, 169), (100, 115, 80, 250))
    rect(screen, (184, 201, 197), (70, 150, 80, 250))
    rect(screen, (220, 228, 227), (315, 105, 80, 250))
    rect(screen, (111, 146, 139), (290, 160, 80, 250))
    ellipse(screen, (169, 187, 187), (110, 100, 500, 50))
    ellipse(screen, (169, 187, 187), (50, 200, 200, 60))

# машинка
def draw_car(x0, y0, width, direction='right'):
    i = width / 150
    if direction == 'right':
        ellipse(screen, (0, 0, 0), (x0, y0 + 40 * i, 20 * i, 5 * i))
        rect(screen, (0, 205, 255), (x0 + 25 * i, y0, 60 * i, 20 * i))
        rect(screen, (214, 246, 255), (x0 + 30 * i, y0 + 5 * i, 20 * i, 15 * i))
        rect(screen, (214, 246, 255), (x0 + 60 * i, y0 + 5 * i, 20 * i, 15 * i))
    else:
        ellipse(screen, (0, 0, 0), (x0 + 130 * i, y0 + 40 * i, 20 * i, 5 * i))
        rect(screen, (0, 205, 255), (x0 + 65 * i, y0, 60 * i, 20 * i))
        rect(screen, (214, 246, 255), (x0 + 70 * i, y0 + 5 * i, 20 * i, 15 * i))
        rect(screen, (214, 246, 255), (x0 + 100 * i, y0 + 5 * i, 20 * i, 15 * i))
    rect(screen, (0, 205, 255), (x0 + 10 * i, y0 + 20 * i, 130 * i, 30 * i))
    ellipse(screen, (0, 0, 0), (x0 + 20 * i, y0 + 35 * i, 30 * i, 25 * i))
    ellipse(screen, (0, 0, 0), (x0 + 100 * i, y0 + 35 * i, 30 * i, 25 * i))

draw_background()
draw_car(30, 400, 60, 'left')
draw_car(100, 410, 60, 'left')
draw_car(50, 440, 150, 'right')
draw_car(190, 460, 200, 'left')
draw_car(210, 390, 60, 'right')
draw_car(280, 410, 60, 'left')

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
