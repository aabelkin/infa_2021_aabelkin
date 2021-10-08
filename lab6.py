import pygame
from pygame.draw import *
from random import randint, random
import math
pygame.init()

FONT = pygame.font.Font(None, 50)
screen_width = 1200
screen_height = 800
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

r_balls_min = 10
r_balls_max = 100
number_of_balls = 5

score = 0
balls = []
game_time = 60
time = 0

def create_ball(balls):
    x = randint(r_balls_max, screen_width - r_balls_max)
    y = randint(r_balls_max, screen_height - r_balls_max)
    r = randint(r_balls_min, r_balls_max)
    angle = random() * 2 * math.pi
    speed = randint(5, 10)
    color = COLORS[randint(0, 5)]
    balls += [[x, y, r, angle, speed, color]]

for ball in range(number_of_balls):
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

def information_display():
    score_display = FONT.render(str(score), True, (255, 255, 255))
    screen.blit(score_display, (10, 30))
    time_display = FONT.render(str(int(time)), True, (255, 255, 255))
    screen.blit(time_display, (screen_width - 60, 30))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    time += 1 / FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse = event.pos[0]
            y_mouse = event.pos[1]
            for i in range(number_of_balls):
                x, y, r = balls[i][0:3]
                if (x - x_mouse) ** 2 + (y - y_mouse) ** 2 <= r ** 2:
                    score += 1
                    balls.pop(i)
                    create_ball(balls)
    for i in range(number_of_balls):
        x, y, r, angle = draw_ball(*balls[i])
        angle = x_reflection(x, r, angle)
        angle = y_reflection(y, r, angle)
        balls[i][0:4] = x, y, r, angle
    information_display()
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()
