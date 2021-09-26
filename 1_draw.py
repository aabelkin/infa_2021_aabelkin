import pygame
from pygame.draw import *
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
rect(screen, (255, 255, 255), (0, 0, 400, 400))

def anglerect(x, y, a, b, angle):
    x1 = x - a * math.sin(angle)
    y1 = y - a * math.cos(angle)
    x2 = x1 + b * math.cos(angle)
    y2 = y1 - b * math.sin(angle)
    x3 = x2 + a * math.sin(angle)
    y3 = y2 + a * math.cos(angle)
    polygon(screen, black, ((x, y), (x1, y1), (x2, y2), (x3, y3)))

yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
circle(screen, yellow, (200, 200), 100)
circle(screen, red, (150, 170), 20)
circle(screen, black, (150, 170), 20, 1)
circle(screen, red, (250, 170), 15)
circle(screen, black, (250, 170), 15, 1)
circle(screen, black, (150, 170), 8)
circle(screen, black, (250, 170), 8)
rect(screen, black, (150, 250, 100, 10))
anglerect(118, 130, 10, 60, -0.5)
anglerect(230, 163, 15, 50, 0.5)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
