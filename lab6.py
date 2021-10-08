import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
score = 0
x, y = 100, 100
angle = 45
speed = 10
r = 30
n_balls = 5
balls = []

for ball in range(n_balls):
    x = randint(100, 1100)
    y = randint(100, 800)
    r = randint(10, 100)
    angle = randint(0, 360)
    speed = randint(5, 10)
    color = COLORS[randint(0, 5)]
    balls += [[x, y, angle, speed, color]]

def new_ball():
    global x, y, r
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def draw_ball(x, y, angle, speed, color):
    x += speed * math.cos(angle)
    y += speed * math.sin(angle)
    circle(screen, color, (x, y), r)
    return (x, y)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse = event.pos[0]
            y_mouse = event.pos[1]
            if (x - x_mouse) ** 2 + (y - y_mouse) ** 2 <= r ** 2:
                score += 1
    for i in range(n_balls):
        balls[i][0:2] = draw_ball(*balls[i])
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
