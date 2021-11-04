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

class Triangle:
    def __init__(self):
        self.x = 0
        self.y = 0        
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.a = 26
        self.b = 20
        self.incline = math.asin((self.b / 2) / (self.a))
        self.an = 0
        self.hit = 0
        self.time = 0

    def move(self):
        if self.hit == 0:           
            dt = 3 / FPS
            self.vy = self.vy + 136*dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.time += dt
            if self.y >= (HEIGHT - 100):
                self.hit = 1

    def draw(self):
        if self.vx > 0:
            self.an = math.atan((self.vy) / (self.vx))
        elif self.vx < 0:
            self.an = math.pi + math.atan((self.vy) / (self.vx))
        else:
            if self.vy >= 0:
                self.an = math.pi / 2
            else:
                self.an = -math.pi / 2
                
        polygon(screen, self.color, ((self.x, self.y),
                                     (self.x - self.a * math.cos(self.incline + self.an),
                                      self.y + self.a * math.sin(self.incline + self.an)),
                                     (self.x - self.a * math.cos(self.incline - self.an),
                                      self.y + self.a * math.sin(self.incline - self.an))))
        
        polygon(screen, (255, 0, 0), ((self.x, self.y),
                                      (self.x - self.a * math.cos(self.incline + self.an),
                                       self.y + self.a * math.sin(self.incline + self.an)),
                                      (self.x - self.a * math.cos(self.incline - self.an),
                                       self.y + self.a * math.sin(self.incline - self.an)),
                                      (self.x, self.y)), 2)
 

    def hittest(self, obj):
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

    def fire2_end(self, event):
        new_triangle = Triangle()
        new_triangle.x = self.x
        new_triangle.y = self.y + HEIGHT - 600
        new_triangle.vx = self.f2_power * math.cos(self.an) * 4
        new_triangle.vy = - self.f2_power * math.sin(self.an) * 4
        triangles.append(new_triangle)
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
        self.vx = 5
        self.vy = 5

    def new_target(self):
        """ Инициализация новой цели. """
        r = self.r = random.randint(20, 50)
        x = self.x = random.randint(2 * self.r, WIDTH - 2 * self.r)
        y = self.y = random.randint(2 * self.r, 300)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= WIDTH or self.x <= self.r:
            self.vx *= -1
        if self.y + self.r >= HEIGHT - 100 or self.y <= self.r:
            self.vy *= -1

class Plane:
    def __init__(self):
        self.time = 0
        self.color = (128, 128, 128)
        self.r = 40
        self.y = 50
        self.x = random.randint(10 + self.r, WIDTH - 200 - self.r)
        self.v = random.randint(-50, 50)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r, 2)

    def move(self):
        dt = 5 / FPS
        self.time += dt
        self.x += self.v * dt
        if (self.x <= self.r) or (self.x + self.r >= WIDTH):
            self.v = -self.v

        if self.time >= 10:
            new_bomb = Bomb()
            new_bomb.x = self.x
            new_bomb.y = self.y + self.r
            new_bomb.vx = self.v
            bombs.append(new_bomb)
            self.time = 0

    def create_plane(self):
        self.time = 0
        self.x = random.randint(282 + self.r, WIDTH - 152 - self.r)
        self.v = random.randint(-100, 100)
        if self.v == 0:
            self.v = 100

class Bomb:
    def __init__(self):
        self.x = 100
        self.y = 80
        self.r = 5
        self.color = BLACK
        self.vx = 0
        self.vy = 50

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        dt = 5 / FPS
        self.y += self.vy * dt
        self.x += self.vx * dt

        if (self.x >= WIDTH - self.r) or (self.x <= self.r):
            self.vx = -self.vx

    def hit(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False

    def clash(self):
        new_bang = Bang(self.x, self.y)
        bangs.append(new_bang)
        bombs.remove(self)

class Bang:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 30
        self.color = (255, 128, 0)
        self.time = 0

    def draw(self):
        dt = 10 / FPS
        if self.time <= 1:
            circle(screen, self.color, (self.x, self.y), self.r * self.time)
            self.time += dt
        else:
            bangs.remove(self)

pygame.init()
global screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
triangles = []
planes = []
bombs = []

clock = pygame.time.Clock()
gun = Gun()
target1 = Target()
target2 = Target()
target1.new_target()
target2.new_target()
finished = False

FONT = pygame.font.Font(None, 50)

new_plane_1 = Plane()
new_plane_1.y = 160
new_plane_2 = Plane()
new_plane_2.y = 270
planes += [new_plane_1] + [new_plane_2]

while not finished:
    screen.fill(WHITE)
    rect(screen, (0, 102, 0), (0, HEIGHT - 100, WIDTH, 100))

    gun.draw()
    target1.draw()
    target2.draw()

    score_display = FONT.render(str(target1.points + target2.points), True, (0, 0, 0))
    screen.blit(score_display, (10, 10))

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire1_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                gun.fire1_end(event)
            if event.button == 3:
                gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    keys = pygame.key.get_pressed()
    gun.move(keys)

    target1.move()
    target2.move()
    for b in balls:
        b.move()
        b.draw()
        for target in target1, target2:
            if b.hittest(target):
                target.hit()
                target.new_target()

    for t in triangles:
        t.move()
        t.draw()
    for p in planes:
        p.move()
        p.draw()
    pygame.display.update()
    gun.power_up()

pygame.quit()
