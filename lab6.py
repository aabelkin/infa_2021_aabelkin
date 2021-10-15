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
target_width = 50
target_speed = 20
target_time = 5

score = 0
balls = []
target = [0, 0]
game_time = 15
time = 0
t_time = 0

def create_ball(balls):
    x = randint(r_balls_max, screen_width - r_balls_max)
    y = randint(r_balls_max, screen_height - r_balls_max)
    r = randint(r_balls_min, r_balls_max)
    angle = random() * 2 * math.pi
    speed = randint(5, 10)
    color = COLORS[randint(0, 5)]
    balls += [[x, y, r, angle, speed, color]]

def create_target(target):
    target[0] = randint(0, screen_width - target_width)
    target[1] = -target_width

for ball in range(number_of_balls):
    create_ball(balls)

create_target(target)

def draw_ball(x, y, r, angle, speed, color):
    x += speed * math.cos(angle)
    y += speed * math.sin(angle)
    circle(screen, color, (x, y), r)
    return (x, y, r, angle)

def draw_target(x, y):
    y += target_speed
    rect(screen, (255, 255, 255), (x, y, target_width, target_width))
    return x, y

def x_reflection(x, r, angle):
    if x - r <= 0 or x + r >= screen_width:
        angle = math.pi - angle
    return angle

def y_reflection(y, r, angle):
    if y - r <= 0 or y + r >= screen_height:
        angle *= -1
    return angle

def display_information():
    score_display = FONT.render(str(score), True, (255, 255, 255))
    screen.blit(score_display, (10, 10))
    time_display = FONT.render(str(int(time)), True, (255, 255, 255))
    screen.blit(time_display, (screen_width - 60, 10))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished and time <= game_time:
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
                    score += r_balls_max // r
                    balls.pop(i)
                    create_ball(balls)
            
            target_x, target_y = target[0:2]
            if target_x <= x_mouse <= target_x + target_width and \
               target_y <= y_mouse <= target_y + target_width:
                score += r_balls_max // r_balls_min * 2
                t_time = 0
                create_target(target)
    
    for i in range(number_of_balls):
        x, y, r, angle = draw_ball(*balls[i])
        angle = x_reflection(x, r, angle)
        angle = y_reflection(y, r, angle)
        balls[i][0:4] = x, y, r, angle
    
    target_x, target_y = draw_target(*target)
    target[0:2] = target_x, target_y

    t_time += 1 / FPS
    if target_y >= screen_height - target_width and t_time >= target_time:
        create_target(target)
        t_time = 0
    
    display_information()
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()
