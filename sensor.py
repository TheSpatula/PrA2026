import pygame
import math
from utils import lerp

class Sensor:
    def __init__(self, car):
        self.car = car
        self.ray_count = 7
        self.ray_length = 100
        self.ray_spread = math.pi

        self.rays = []
        self.readings = []


    def update(self):
        self.cast_rays()
    
    def cast_rays(self):
        self.rays = [] # clear out the list
        for i in range(self.ray_count): # for each of the rays, set the ray angle, based on the total ray spread using lerp
            RAY_ANGLE = lerp(
                self.ray_spread / 2,
                -self.ray_spread / 2,
                i/(self.ray_count - 1)
            ) - self.car.angle

            START = (self.car.x, self.car.y)
            END = (self.car.x - math.sin(RAY_ANGLE) * self.ray_length,
                   self.car.y - math.cos(RAY_ANGLE) * self.ray_length)

            self.rays.append((START, END)) # populate the list with the calculated distance

    def draw(self, screen):# indexing is grabbing the x ans y pos for the line that needs to be drawn
        for i in range(self.ray_count):
            pygame.draw.line(screen, "YELLOW", (self.rays[i][0][0], self.rays[i][0][1]), (self.rays[i][1][0], self.rays[i][1][1]))