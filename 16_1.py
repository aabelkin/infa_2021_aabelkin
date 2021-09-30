import pygame
from pygame.draw import *
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 550))
rect(screen, (255, 255, 255), (0, 0, 400, 550))

def draw_background():
    rect(screen, (184, 197, 201), (0, 0, 400, 345))
    rect(screen, (82, 108, 113), (0, 350, 400, 200))
    rect(screen, (148, 169, 174), (5, 5, 80, 350))
    rect(screen, (148, 174, 169), (100, 15, 80, 350))
    rect(screen, (184, 201, 197), (70, 50, 80, 350))
    rect(screen, (220, 228, 227), (315, 5, 80, 350))
    rect(screen, (111, 146, 139), (290, 60, 80, 350))
    ellipse(screen, (169, 187, 187), (110, 0, 500, 50))
    ellipse(screen, (169, 187, 187), (50, 100, 300, 60))

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
draw_car(150, 450, 200)
ellipse(screen, (108, 134, 129), (70, 450, 70, 30))
ellipse(screen, (108, 134, 129), (50, 410, 60, 25))
ellipse(screen, (108, 134, 129), (30, 390, 50, 20))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
