#!/usr/bin/env python3

# import pygame
# import math


# pygame.init()

# screen_width = 1200
# screen_height = 500

# win = pygame.display.set_mode((screen_width, screen_height))

# class ball(object):
    # def __init__(self, x, y, r, color):
        # self.x = x
        # self.y = y
        # self.r = r
        # self.color = color

    # def draw(self, win):
        # pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.r)
        # pygame.draw.circle(win, self.color, (self.x, self.y), self.r-1)

    # @staticmethod
    # def ball_path(startx, starty, power, ang, time):
        # angle = ang
        # velx = math.cos(angle) * power
        # vely = math.sin(angle) * power

        # distX = velx * time
        # distY = (vely * time) + ((- 4.9 * (time**2)) / 2)

        # newx = round(distX + startx)
        # newy = round(starty - distY)

        # return (newx, newy)

# def redraw_window():
    # win.fill((64, 64, 64))
    # golfBall.draw(win)
    # pygame.draw.line(win, (255, 255, 255), line[0], line[1])
    # pygame.display.update()

# def find_angle(pos):
    # sX = golfBall.x
    # sY = golfBall.y
    # try:
        # angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    # except:
        # angle = math.pi / 2

    # if pos[1] < sY and pos[0] > sX:
        # angle = abs(angle)
    # elif pos[1] < sY and pos[0] < sX:
        # angle = math.pi - angle
    # elif pos[1] > sY and pos[0] < sX:
        # angle = math.pi + abs(angle)
    # elif pos[1] > sY and pos[0] > sX:
        # angle = (math.pi * 2) - angle

    # return angle


# golfBall = ball(300, 494, 5, (255, 255, 255))



# run = True
# time = 0
# power = 0
# angle = 0
# shoot = False
# clock = pygame.time.Clock()

# if __name__ == '__main__':
    # while run:
        # clock.tick(200)
        # if shoot:
            # if golfBall.y < 500 - golfBall.r:
                # time += 0.05
                # po = ball.ball_path(x, y, power, angle, time)
                # ball.x = po[0]
                # ball.y = po[1]
            # else:
                # shoot = False
                # time = 0
                # ball.y = 494

        # line = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
        # redraw_window()

        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
                # run = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
                # if not shoot:
                    # x = golfBall.x
                    # y = golfBall.y
                    # pos = pygame.mouse.get_pos()
                    # shoot = True
                    # power = math.sqrt( (line[1][1] - line[1][0])**2 + (line[0][1] - line[0][0])**2 ) / 8
                    # angle = find_angle(pos)

# pygame.quit()
# quit()






import pygame
import math

wScreen = 1200
hScreen = 500

win = pygame.display.set_mode((wScreen,hScreen))
pygame.display.set_caption('Projectile Motion')


class ball(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)


    @staticmethod
    def ballPath(startx, starty, power, ang, time):
        angle = ang
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power

        distX = velx * time
        distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

        newx = round(distX + startx)
        newy = round(starty - distY)


        return (newx, newy)


def redrawWindow():
    win.fill((64,64,64))
    golfBall.draw(win)
    pygame.draw.line(win, (0,0,0),line[0], line[1])
    pygame.display.update()

def findAngle(pos):
    sX = golfBall.x
    sY = golfBall.y
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle


golfBall = ball(300,494,5,(255,255,255))

run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
while run:
    clock.tick(200)
    if shoot:
        if golfBall.y < 500 - golfBall.radius:
            time += 0.05
            po = ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[0]
            golfBall.y = po[1]
        else:
            shoot = False
            time = 0
            golfBall.y = 494

    line = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                x = golfBall.x
                y = golfBall.y
                pos =pygame.mouse.get_pos()
                shoot = True
                power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)/8
                angle = findAngle(pos)



pygame.quit()
quit()