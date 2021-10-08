import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()

screen_width = 1200
screen_height = 900
FPS = 30
screen = pygame.display.set_mode((screen_width, screen_height))

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
    balls += [[x, y, r, angle, speed, color]]

def new_ball():
    global x, y, r
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def draw_ball(x, y, r, angle, speed, color):
    x += speed * math.cos(angle)
    y += speed * math.sin(angle)
    circle(screen, color, (x, y), r)
    return (x, y, r)

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
        x, y, r = draw_ball(*balls[i])
        balls[i][0:3] = x, y, r
        if x - r <= 0 or x + r >= screen_width:
            pass
        if y - r <= 0 or y + r >= screen_height:
            pass
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
