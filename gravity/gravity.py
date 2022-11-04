#!/usr/bin/env python3

import pygame

pygame.init()

width = 640
height = 640

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


class Sun():
    def __init__(self):
        self.loc = pygame.Vector2(width/2, height/2)

    def location(self):
        return self.loc

    def draw(self):
        pygame.draw.circle(screen, 'yellow', self.loc, 25)

class Planet():
    def __init__(self, x : int, y : int, sun : Sun):
        self.loc = pygame.Vector2(x, y)
        self.v = pygame.Vector2(10, 0)
        self.sun = sun

    def draw(self):
        pygame.draw.circle(screen, 'blue', self.loc, 5)

    def calculate_acceleration(self):
        dir_to_sun = self.sun.location() - self.loc
        self.a = pygame.math.Vector2.normalize(dir_to_sun)
        self.a *= 0.3

    def update(self):
        self.calculate_acceleration()
        self.v += self.a
        self.loc += self.v



if __name__ == '__main__':
    sun = Sun()
    earth = Planet(width/2, 50, sun)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        sun.draw()
        earth.draw()
        earth.update()
        pygame.display.flip()
        clock.tick(60)