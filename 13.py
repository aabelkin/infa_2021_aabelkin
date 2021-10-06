import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 500))
white = (255, 255, 255)

def background(rect_color, ground_color, back_color):
    rect(screen, back_color, (0, 0, 400, 0), 500)
    rect(screen, ground_color, (0, 400, 400, 0), 400)
    polygon(screen, rect_color, [(0, 0), (50, 0), (50, 300), (0, 300)])
    polygon(screen, rect_color, [(100, 0), (190, 0), (190, 400), (100, 400)])
    polygon(screen, rect_color, [(230, 0), (260, 0), (260, 250), (230, 250)])
    polygon(screen, rect_color, [(320, 0), (360, 0), (360, 300), (320, 300)])

# цвета
rect_color = (250, 250, 0)
ground_color = (139, 139, 100)
back_color = (0, 250, 0)

needle_color = (65, 58, 58)
body_color = (65, 58, 39)
apple1_color = (239, 187, 0)
apple2_color = (239, 187, 0)
apple3_color = (255, 0, 0)
stipe_color = white
hat_color = (250, 0, 0)

def mushroom(x, y, width, stipe_color, hat_color):
    """ x, y - координаты верхней левой точки
        width - ширина гриба
        stipe_color - цвет ножки
        hat_color - цвет шляпки
    """
    k = width / 50
    ellipse(screen, stipe_color, (x+15*k, y+10*k, 20*k, 50*k))
    ellipse(screen, (139, 139, 255), (x+15*k, y+10*k, 20*k, 50*k),int(k+0.5) )
    ellipse(screen, hat_color, (x, y, 50*k, 20*k))
    ellipse(screen, (139, 139, 255), (x, y, 50*k, 20*k),int(k+0.5) )
    ellipse(screen, white, (x+10*k, y+10*k, 5*k, 2*k))
    ellipse(screen, white, (x+8*k, y+6*k, 5*k, 2*k))
    ellipse(screen, white, (x+20*k, y+6*k, 5*k, 2*k))
    ellipse(screen, white, (x+39*k, y+5*k, 7*k, 2*k))
    ellipse(screen, white, (x+30*k, y+7*k, 5*k, 2*k))
    ellipse(screen, white, (x+35*k, y+10*k, 5*k, 2*k))
    
def rad_to_deg(angle):
    """ Радианы в градусы.
    """
    return angle / 180 * math.pi

def needle(x, y, width, height, angle, color):
    angle = rad_to_deg(angle)
    polygon(screen, color, [(x, y),
                            (x - width / 2 * math.sin(angle) - height * math.cos(angle), y - width / 2 * math.cos(angle) + height * math.sin(angle)),
                            (x + width / 2 * math.sin(angle) - height * math.cos(angle), y + width / 2 * math.cos(angle) + height * math.sin(angle))])
    polygon(screen, (0, 0, 0), [(x, y),
                            (x - width / 2 * math.sin(angle) - height * math.cos(angle), y - width / 2 * math.cos(angle) + height * math.sin(angle)),
                            (x + width / 2 * math.sin(angle) - height * math.cos(angle), y + width / 2 * math.cos(angle) + height * math.sin(angle))], 1)

def hedgehog(x, y, width):
    """ x, y - координаты верхней левой точки
        width - ширина ёжика
    """
    
    def hedgehog_body(k, body_color):
        ellipse(screen, body_color, (x-10*k, y+50*k, 30*k, 20*k))
        ellipse(screen,(255, 255, 255) , (x-10*k, y+50*k, 30*k, 20*k), int(k+0.5))
        ellipse(screen, body_color, (x+120*k, y+60*k, 25*k, 20*k))
        ellipse(screen,(255, 255, 255) , (x+120*k, y+60*k, 25*k, 20*k), int(k+0.5))
        ellipse(screen, body_color, (x, y, 150*k, 90*k))
        ellipse(screen, (255, 255, 255), (x, y, 150*k, 90*k), int(k+0.5) )
        ellipse(screen, body_color, (x+130*k, y+30*k, 60*k, 40*k))
        circle(screen, (0, 0,0), (x+150*k, y+45*k), 3*k)
        circle(screen, (255, 255,255), (x+150*k, y+45*k), 3*k, int(k+0.5))
        circle(screen, (0, 0,0), (x+165*k, y+43*k), 3*k)
        circle(screen, (255, 255,255), (x+165*k, y+43*k), 3*k, int(k+0.5))
        circle(screen, (0, 0,0), (x+190*k, y+48*k), 2*k)
        circle(screen, (255, 255,255), (x+190*k, y+48*k), 2*k, int(k+0.5))
    
        ellipse(screen, (255, 255, 255), (x+130*k, y+30*k, 60*k, 40*k), int(k+0.5))
        ellipse(screen, body_color, (x+10*k, y+75*k, 30*k, 20*k))
        ellipse(screen,(255, 255, 255) , (x+10*k, y+75*k, 30*k, 20*k), int(k+0.5))
        ellipse(screen, body_color, (x+100*k, y+75*k, 25*k, 20*k))
        ellipse(screen,(255, 255, 255) , (x+100*k, y+75*k, 25*k, 20*k), int(k+0.5))

    def apples(apple1_color, apple2_color, apple3_color):
        circle(screen, apple1_color, (x+20*k, y+20*k), 15*k)
        circle(screen, (255, 255, 255), (x+20*k, y+20*k), 15*k, int(k+0.5))
        circle(screen, apple2_color, (x+27*k, y+27*k), 15*k)
        circle(screen, (255, 255, 255), (x+27*k, y+27*k), 15*k, int(k+0.5))
        circle(screen, apple3_color, (x+110*k, y+10*k), 17*k)
        circle(screen,(255, 255, 255) , (x+110*k, y+10*k), 17*k, int(0.5+k))

    k = width / 190
    hedgehog_body(k, body_color)
    for i in range(0, 20):
        needle(x+10*k+k*13*i/2, y-15*k+k*randint(-30, -10), 15 * k, 50 * k, 90 + 2*(10 - i), needle_color)
    mushroom(x+39*k, y, k*50, stipe_color, hat_color)
    apples(apple1_color, apple2_color, apple3_color)
    for i in range(0, 10):
        needle(x+10*k+k*12*i, y+k*randint(-30, 10), 15 * k, 80 * k, 90 + 2*(10-i), needle_color)

background(rect_color, ground_color, back_color)
hedgehog(200, 300, 200)
hedgehog(140, 200, 120)
hedgehog(-40, 390, 140)
hedgehog(330, 200, 120)
mushroom(200, 450, 30, stipe_color, hat_color)
mushroom(240, 490, 40, stipe_color, hat_color)
mushroom(260, 460, 30, stipe_color, hat_color)
mushroom(290, 495, 25, stipe_color, hat_color)
mushroom(320, 450, 35, stipe_color, hat_color)
mushroom(360, 480, 30, stipe_color, hat_color)
mushroom(380, 439, 40, stipe_color, hat_color)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
