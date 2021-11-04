import math
import random

import pygame
from pygame.draw import *


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy
        self.vy -= 1
        if self.x + self.r >= WIDTH or self.x - self.r <= 0:
            self.vx *= -1
        if self.y + self.r >= HEIGHT - 100 or self.y - self.r <= 0:
            self.vy *= -1
            

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.length = 40
        self.width = 10
        self.x = WIDTH / 2
        self.y = 390
        self.r = 60
        self.go = 0
        self.v = 3

    def fire1_start(self, event):
        self.f2_on = 1

    def fire1_end(self, event):
        """Выстрел мячом.5

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event.pos[0] - self.x > 0:
            self.an = math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        elif event.pos[0] - self.x < 0:
            self.an = math.pi + math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        else:
            if self.y - event.pos[1] >= 0:
                self.an = math.pi / 2
            else:
                self.an = -math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        circle(screen, GREEN, (self.x, self.y + 40 + HEIGHT - 600), self.r)
        circle(screen, BLACK, (self.x, self.y + 40 + HEIGHT - 600), self.r, 1)
        rect(screen, GREEN, (self.x - 70, self.y + 40 + HEIGHT - 600, 140, self.r))
        rect(screen, BLACK, (self.x - 70, self.y + 40 + HEIGHT - 600, 140, self.r), 1)
        circle(screen, (190, 190, 190), (self.x - 50, self.y + 80 + HEIGHT - 600), 30)
        circle(screen, BLACK, (self.x - 50, self.y + 80 + HEIGHT - 600), 30, 1)
        circle(screen, (190, 190, 190), (self.x + 50, self.y + 80 + HEIGHT - 600), 30)
        circle(screen, BLACK, (self.x + 50, self.y + 80 + HEIGHT - 600), 30, 1)
        a = self.length + self.f2_power
        b = self.width / 2
        polygon(screen, self.color, ((self.x - b * math.sin(self.an),
                                                      self.y - b * math.cos(self.an)),
                                                      (self.x + b * math.sin(self.an),
                                                      self.y + b * math.cos(self.an)),
                                                      (self.x + b * math.sin(self.an) + a * math.cos(self.an),
                                                      self.y + b * math.cos(self.an) - a * math.sin(self.an)),
                                                      (self.x - b * math.sin(self.an) + a * math.cos(self.an),
                                                      self.y - b * math.cos(self.an) - a * math.sin(self.an))))
        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move(self, keys):
        if keys[pygame.K_a]:
            self.go = -1
        if keys[pygame.K_d]:
            self.go = 1
        self.x += self.go * self.v


class Target:
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()
    def __init__(self):
        self.points = 0
        self.live = 1
        self.vx = 5
        self.vy = 5

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = random.randint(600, 750)
        y = self.y = random.randint(200, 450)
        r = self.r = random.randint(2, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x >= WIDTH - self.r or self.x <= self.r:
            self.vx *= -1
        if self.y >= HEIGHT - self.r or self.y <= self.r:
            self.vy *= -1


pygame.init()
global screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun()
target1 = Target()
target2 = Target()
target1.new_target()
target2.new_target()
finished = False

FONT = pygame.font.Font(None, 50)

while not finished:
    screen.fill(WHITE)
    rect(screen, (0, 102, 0), (0, HEIGHT - 100, WIDTH, 100))


    gun.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()

    score_display = FONT.render(str(target1.points + target2.points), True, (0, 0, 0))
    screen.blit(score_display, (10, 10))
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire1_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                gun.fire1_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    keys = pygame.key.get_pressed()
    gun.move(keys)

    target1.move()
    target2.move()
    for b in balls:
        b.move()
        for target in target1, target2:
            if b.hittest(target) and target.live:
                #target.live = 0
                target.hit()
                target.new_target()
    gun.power_up()

pygame.quit()
