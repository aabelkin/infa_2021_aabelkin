import pygame
from pygame.draw import *
from random import randint, random
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
n_balls = 5
balls = []

def create_ball(balls):
    x = randint(100, 1100)
    y = randint(100, 800)
    r = randint(10, 100)
    angle = random() * 2 * math.pi
    speed = randint(5, 10)
    color = COLORS[randint(0, 5)]
    balls += [[x, y, r, angle, speed, color]]

for ball in range(n_balls):
    create_ball(balls)

def draw_ball(x, y, r, angle, speed, color):
    x += speed * math.cos(angle)
    y += speed * math.sin(angle)
    circle(screen, color, (x, y), r)
    return (x, y, r, angle)

def x_reflection(x, r, angle):
    if x - r <= 0 or x + r >= screen_width:
        angle = math.pi - angle
    return angle

def y_reflection(y, r, angle):
    if y - r <= 0 or y + r >= screen_height:
        angle *= -1
    return angle

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
            for i in range(n_balls):
                x, y, r = balls[i][0:3]
                if (x - x_mouse) ** 2 + (y - y_mouse) ** 2 <= r ** 2:
                    score += 1
                    balls.pop(i)
                    create_ball(balls)
    for i in range(n_balls):
        x, y, r, angle = draw_ball(*balls[i])
        angle = x_reflection(x, r, angle)
        angle = y_reflection(y, r, angle)
        balls[i][0:4] = x, y, r, angle
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
