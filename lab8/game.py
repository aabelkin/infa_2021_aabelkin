import math
from random import randint
import pygame
from pygame.draw import *

FPS = 100

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1200
HEIGHT = 800

class Triangle:
    """ Снаряд 2 вида - треугольник. """
    def __init__(self):
        self.x = 0
        self.y = 0        
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.a = 26
        self.b = 20
        self.incline = math.asin((self.b / 2) / (self.a))
        self.time = 0
        self.an = 0
        self.hit = 0

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
                self.an =  -math.pi / 2
                
        polygon(screen, self.color, ((self.x, self.y),
                                     (self.x - self.a * math.cos(self.incline + self.an),
                                      self.y + self.a * math.sin(self.incline + self.an)),
                                     (self.x - self.a * math.cos(self.incline - self.an),
                                      self.y + self.a * math.sin(self.incline - self.an)),
                                     (self.x, self.y)))
        
        polygon(screen, (255, 0, 0), [(self.x, self.y), (self.x - self.a * math.cos(self.incline + self.an), self.y + self.a * math.sin(self.incline + self.an)),
                                           (self.x - self.a * math.cos(self.incline - self.an), self.y + self.a * math.sin(self.incline - self.an)), (self.x, self.y)], 2)

    def hittest(self, obj):
        if (obj.r)**2 >= ((self.x - obj.x)**2 + (self.y - obj.y)**2):
            return True
        
        else:
            return False


class Buckshot:
    """ Развыв снаряда 1 вида на более мелкие снаряды. """
    def __init__(self):
        self.hit = 0
        self.x = []
        self.y = []
        self.r = 4
        self.color = GAME_COLORS[randint(0, 4)]
        self.v = 15
        self.vx = []
        self.vy = []
        self.n = 8
        for i in range(0, self.n):
            self.vx += [self.v * math.cos(2 * math.pi * i/ self.n)]
            self.vy += [self.v * math.sin(2 * math.pi * i/ self.n)]
        self.time = 0

    def move(self):
        dt = 3 / FPS
        for i in range(0, self.n):
            self.vy[i] = self.vy[i] + 100*dt
            self.x[i] += self.vx[i] * dt
            self.y[i] += self.vy[i] * dt 
            if (self.x[i] + self.r >= WIDTH) or (self.x[i] - self.r <= 0):
                self.vx[i] = - self.vx[i]
            if (self.y[i] + self.r >= (HEIGHT - 100)) and (self.vy[i] >= 0):
                self.vy[i] = - self.vy[i]
        self.time += dt

    def draw(self):
        for i in range (0, self.n):
            circle(screen, self.color, (self.x[i], self.y[i]), self.r)

    def hittest(self, obj):
        for i in range(0, self.n):
            if (self.r + obj.r) ** 2 >= (self.x[i] - obj.x) ** 2 + (self.y[i] - obj.y) ** 2:
                self.hit = 1
        if self.hit == 1:
            self.hit = 0
            return True       
        return False


class Ball:
    """ Сраняд 1 вида - шарик. """
    def __init__(self):
        self.x = 40
        self.y = 450
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[randint(0, 4)]
        self.time = 0

    def move(self):
        dt = 3 / FPS
        self.vy = self.vy + 136*dt
        self.x += self.vx * dt
        self.y += self.vy * dt 
        self.time += dt
        if (self.x + self.r >= WIDTH) or (self.x - self.r <= 0):
            self.vx = - self.vx
        if (self.y + self.r >= (HEIGHT - 100)) and (self.vy >= 0):
            self.vy = - self.vy

        if self.time >= 3:
            new_buckshot = Buckshot()
            for i in range (0, new_buckshot.n):               
                new_buckshot.x += [self.x]
                new_buckshot.y += [self.y]
            buckshots.append(new_buckshot)
            balls.remove(self)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        if (self.r + obj.r)**2 >= (self.x - obj.x)**2 + (self.y - obj.y)**2:
            return True       
        else:
            return False


class Gun:
    """ Танк с пушкой. """
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY
        self.x = WIDTH / 2
        self.y = 390
        self.v = 3
        self.r = 60
        self.go = 0

    def targetting(self, event):
        if event.pos[0] - self.x > 0:
            self.angle = math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        elif event.pos[0] - self.x < 0:
            self.angle = math.pi + math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        else:
            if self.y - event.pos[1] >= 0:
                self.angle = math.pi / 2
            else:
                self.angle =  - math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def move_start(self, event):
        if event.key == pygame.K_a:
            self.go = -1
        if event.key == pygame.K_d:
            self.go = 1
    
    def move(self, keys):
        if keys[pygame.K_a]:
            self.go = -1
        if keys[pygame.K_d]:
            self.go = 1
        self.x += self.go * self.v

    def move_end(self, event):
        if (event.key == pygame.K_a) or (event.key == pygame.K_d):
            self.go = 0 

    def draw(self):
        circle(screen, GREEN, (self.x, self.y + 40 + HEIGHT - 600), self.r)
        circle(screen, BLACK, (self.x, self.y + 40 + HEIGHT - 600), self.r, 1)
        rect(screen, GREEN, (self.x - 70, self.y + 40 + HEIGHT - 600, 140, self.r))
        rect(screen, BLACK, (self.x - 70, self.y + 40 + HEIGHT - 600, 140, self.r), 1)
        circle(screen, (190, 190, 190), (self.x - 50, self.y + 80 + HEIGHT - 600), 30)
        circle(screen, BLACK, (self.x - 50, self.y + 80 + HEIGHT - 600), 30, 1)
        circle(screen, (190, 190, 190), (self.x + 50, self.y + 80 + HEIGHT - 600), 30)
        circle(screen, BLACK, (self.x + 50, self.y + 80 + HEIGHT - 600), 30, 1)
        polygon(screen, self. color, [(self.x, self.y + HEIGHT - 600), (self.x + self.f2_power * math.cos(self.angle), self.y - self.f2_power * math.sin(self.angle) + HEIGHT - 600),
                                           (self.x + self.f2_power * math.cos(self.angle) - 5 * math.sin(self.angle), self.y  + HEIGHT - 600 - self.f2_power * math.sin(self.angle) - 5 * math.cos(self.angle)),
                                           (self.x - 5 * math.sin(self.angle), self.y - 5 * math.cos(self.angle) + HEIGHT - 600), (self.x, self.y + HEIGHT - 600)])
        polygon(screen, BLACK, [(self.x, self.y + HEIGHT - 600), (self.x + self.f2_power * math.cos(self.angle), self.y - self.f2_power * math.sin(self.angle) + HEIGHT - 600),
                                           (self.x + self.f2_power * math.cos(self.angle) - 5 * math.sin(self.angle), self.y  + HEIGHT - 600 - self.f2_power * math.sin(self.angle) - 5 * math.cos(self.angle)),
                                           (self.x - 5 * math.sin(self.angle), self.y - 5 * math.cos(self.angle) + HEIGHT - 600), (self.x, self.y + HEIGHT - 600)], 2)

    def fire1_start(self, event):
        self.f2_on = 1

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def fire1_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.x = self.x
        new_ball.y = self.y  + HEIGHT - 600
        new_ball.vx = self.f2_power * math.cos(self.angle) * 4
        new_ball.vy = - self.f2_power * math.sin(self.angle) * 4
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        
    def fire2_end(self, event):
        new_triangle = Triangle()
        new_triangle.x = self.x
        new_triangle.y = self.y + HEIGHT - 600
        new_triangle.vx = self.f2_power * math.cos(self.angle) * 4
        new_triangle.vy = - self.f2_power * math.sin(self.angle) * 4
        triangles.append(new_triangle)
        self.f2_on = 0
        self.f2_power = 10        


class Helicopter:
    """ Цели 1 вида - красные шары по бокам. """
    def __init__(self):
        self.r = 50
        self.x = 100
        self.y = randint(141 + self.r, HEIGHT - 101 - self.r - 160)
        self.v = randint(-100, 100)
        if abs(self.v) < 40:
            self.v = 100 - abs(self.v)
        self.color = RED

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def move(self):
        dt = 5 / FPS
        self.y += self.v * dt
        if (self.y - self.r <= 140) or (self.y + self.r >= HEIGHT - 100 - 160):
            self.v = -self.v       

    def create_helicopter(self):
        self.y = randint(141 + self.r, HEIGHT - 101 - self.r - 160)
        self.v = randint(-100, 100)
        if abs(self.v) < 40:
            self.v = 100 - abs(self.v)


class Plane:
    """ Цели 2 вида - шары, летающие сверху по горизонтали. """
    def __init__(self):
        self.time = 0
        self.color = (128, 128, 128)
        self.r = 40
        self.y = 50
        self.x = randint(282 + self.r, WIDTH - 152 - self.r)
        self.v = randint(-100, 100)
        if self.v == 0:
            self.v = 100

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r, 2)

    def move(self):
        dt = 5 / FPS
        self.time += dt
        self.x += self.v * dt
        if (self.x - self.r - 281 <= 0) or (self.x + self.r >= WIDTH - 151):
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
        self.x = randint(282 + self.r, WIDTH - 152 - self.r)
        self.v = randint(-100, 100)
        if self.v == 0:
            self.v = 100      

class Airship:
    """ Аэростат - верхний шарик. Он может стрелять в танк. """ 
    def __init__(self):
        self.r = 30
        self.time = 0
        self.color = (192, 192, 192)
        self.y = 60
        self.x = WIDTH - 152 - self.r
        self.v = -90

    def move(self):
        dt = 5 / FPS
        self.time += dt
        self.x += self.v * dt
        if (self.x - self.r - 281 <= 0) or (self.x + self.r >= WIDTH - 151):
            self.v = -self.v

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r, 2)
            
    def fire(self, event):
        if (event.key == pygame.K_SPACE) and (self.time >= 7):
            new_bomb = Bomb()
            new_bomb.x = self.x
            new_bomb.y = self.y + self.r
            new_bomb.vx = self.v
            bombs.append(new_bomb)
            self.time = 0
    
class Bomb:
    """ Бомбочки, сбрасываемые аэростатом и целями 2 вида. """
    def __init__(self):
        self.x = 100
        self.y = 80
        self.r = 5
        self.color = BLACK
        self.vx = 0
        self.vy = 50

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def move(self):
        dt = 5 / FPS
        self.y += self.vy * dt
        self.x += self.vx * dt

        if (self.x >= WIDTH - self.r) or (self.x <= self.r):
            self.vx = -self.vx

    def hit(self, obj):
        if (self.r + obj.r) ** 2 >= (self.x - obj.x) ** 2 + (-self.y + 40 + HEIGHT - 600 + obj.y ) ** 2:
            return True
        else:
            return False

    def clash(self):
        new_bang = Bang()
        new_bang.x = self.x
        new_bang.y = self.y
        bangs.append(new_bang)
        bombs.remove(self)
            
class Bang:
    """ Взрыв бомбочки при касании с землей. """
    def __init__(self):
        self.x = 0
        self.y = 0
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
f1 = pygame.font.Font(None, 140)
f2 = pygame.font.Font(None, 40)
f3 = pygame.font.Font(None, 100)
global screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

health_tank = 2
health_airship = 2

clock = pygame.time.Clock()

bullet = 0
points = 0
balls = []
triangles = []
helicopters = []
planes = []
bombs = []
buckshots = []
bangs = []
  
new_helicopter_1 = Helicopter()
new_helicopter_1.x = 100
new_helicopter_2 = Helicopter()
new_helicopter_2.x = WIDTH - 100
helicopters += [new_helicopter_1] + [new_helicopter_2]

gun = Gun()
airship = Airship()

new_plane_1 = Plane()
new_plane_1.y = 160
new_plane_2 = Plane()
new_plane_2.y = 270
planes += [new_plane_1] + [new_plane_2]
    
finished = False

while not finished:
    screen.fill((204, 255, 255))
    rect(screen, (102, 51, 0), (0, HEIGHT - 100, WIDTH, 100))
    rect(screen, (0, 102, 0), (0, HEIGHT - 100, WIDTH, 40))
    rect(screen, (0, 0, 0), (-10, HEIGHT - 100, WIDTH + 10, 40), 3)
    text1 = f1.render(str(health_tank), True,
                    (100, 0, 0))
    screen.blit(text1, (80, 40))
    text2 = f1.render(str(health_airship), True,
                    (100, 0, 0))
    screen.blit(text2, (WIDTH - 210, 40))
    
    text3 = f2.render('Здоровье танка' , True,
                  (100, 0, 0))
    screen.blit(text3, (15, 5))

    text4 = f2.render('Здоровье аэростата', True,
                  (100, 0, 0))
    screen.blit(text4, (WIDTH - 290, 5))

    gun.draw()

    airship.move()
    airship.draw()
    
    for h in helicopters:
        h.move()
        h.draw()

    for p in planes:
        p.move()
        p.draw()

    for b in balls:
        b.move()
        b.draw()

    for t in triangles:
        t.move()
        t.draw()

    for bm in bombs:
        bm.move()
        if bm.hit(gun):
            bm.clash()
            health_tank = health_tank - 1
        if (bm.y >= (HEIGHT - 100)):
            bm.clash()
        bm.draw()

    for bg in bangs:
        bg.draw()

    for bs in buckshots:
        bs.move()
        bs.draw()

    pygame.display.update()
        

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        else:
            if event.type == pygame.KEYUP:
               gun.move_end(event)
            if event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire1_start(event)
            if event.type == pygame.KEYDOWN:              
                airship.fire(event)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gun.fire1_end(event)
                if event.button == 3:
                    gun.fire2_end(event)

    keys = pygame.key.get_pressed()
    gun.move(keys)

    for t in triangles:
        for h in helicopters:
            if t.hittest(h):
                h.create_helicopter()
                triangles.remove(t)
        for p in planes:
            if t.hittest(p):
                p.create_plane()
                triangles.remove(t)
        if t.hittest(airship):
            health_airship = health_airship - 1
            triangles.remove(t)
            
    for b in balls:
        for h in helicopters:           
            if b.hittest(h):
                h.create_helicopter()
                balls.remove(b)
        for p in planes:
            if b.hittest(p):
                p.create_plane()
                balls.remove(b)
        if b.hittest(airship):
            health_airship = health_airship - 1
            balls.remove(b)
            
    for bs in buckshots:
        for h in helicopters:
            if bs.hittest(h):
                h.create_helicopter()
        for p in planes:
            if bs.hittest(p):
                p.create_plane()
        if bs.hittest(airship):
            health_airship = health_airship - 1
            buckshots.remove(bs)
            
        if bs.time >= 3:
            buckshots.remove(bs)

    gun.power_up()

    if (health_tank <= 0) or (health_airship <= 0):
        finished = True

finished = False

while not finished:
    screen.fill(BLACK)
    text5 = f3.render('ПОБЕДИТЕЛЬ' , True,
                  (255, 255, 255))
    screen.blit(text5, (350, 300))

    if health_tank <= 0:
        text6 = f3.render('АЭРОСТАТ' , True,
                      (255, 255, 255))
        screen.blit(text6, (400, 400))
    elif health_airship <= 0:
        text6 = f3.render('ТАНК' , True,
                      (255, 255, 255))
        screen.blit(text6, (490, 400))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
