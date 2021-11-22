#!/usr/bin/env python3

import random
import math
import pygame

WIDTH = 640
HEIGHT = 480

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Vector:
    def __init__(self, magnitude: float, angle: float):
        self.x_component = magnitude * math.cos(math.radians(angle))
        self.y_component = magnitude * math.sin(math.radians(angle))

    def get_x_component(self):
        return self.x_component

    def get_y_component(self):
        return self.y_component


class Particle:
    def __init__(self, mass: float, velocity: Vector):
        self.mass = mass
        self.velocity = velocity
        self.radius = 10 * mass
        self.x = random.randint(0, 300)
        self.y = random.randint(0, 300)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def move_x_direction(self):
        self.x += self.velocity.get_x_component()

    def move_y_direction(self):
        self.y += self.velocity.get_y_component()

    def move(self):
        self.x += self.velocity.get_x_component()
        self.y += self.velocity.get_y_component()

    def set_coordinates(self, coordinates: tuple):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def collides(self, another: 'Particle'):
        distance_between_particles = math.sqrt((self.x - another.x)**2 + (self.y - another.y)**2)
        return distance_between_particles - self.radius - another.radius <= 0

    def draw(self, surface, color):
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius) 



if __name__ == '__main__':
    v1 = Vector(1, -5)
    p1 = Particle(1, v1)
    v2 = Vector(2, 29)
    p2 = Particle(1, v2)
    # p1.set_coordinates((10, 10))
    # p2.set_coordinates((20, 20))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill((0, 0, 0))
        p1.draw(screen, 'red')
        p2.draw(screen, 'blue')
        pygame.display.flip()

        p1.move()
        p2.move()

        clock.tick(60)
