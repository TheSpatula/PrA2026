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


    def update(self, track_mask):
        self.cast_rays(track_mask)
    
    def cast_rays(self, track_mask):
        self.rays = [] # clear out the list
        self.readings = []
        step = 2
        for i in range(self.ray_count): # for each of the rays, set the ray angle, based on the total ray spread using lerp
            RAY_ANGLE = lerp(
                self.ray_spread / 2,
                -self.ray_spread / 2,
                i/(self.ray_count - 1)
            ) - self.car.angle

            START = (self.car.x, self.car.y)
            direction = (-math.sin(RAY_ANGLE), -math.cos(RAY_ANGLE))
            END = (self.car.x - math.sin(RAY_ANGLE) * self.ray_length,
                   self.car.y - math.cos(RAY_ANGLE) * self.ray_length)

            for i in range(0, int(self.ray_length), step):
                point = ((START[0] + direction[0] * i), (START[1] + direction[1] * i))
                reading = 0

                if 0 <= point[0] < track_mask.get_size()[0] and 0 <= point[1] < track_mask.get_size()[1]:
                    if track_mask.get_at(point):
                        END = point
                        reading = i / self.ray_length
                        break

                if reading == 0:
                    reading = 1

            self.rays.append((START, END)) # populate the list with the calculated distance
            self.readings.append(reading)

    def draw(self, screen):# indexing is grabbing the x ans y pos for the line that needs to be drawn
        for i in range(self.ray_count):
            pygame.draw.line(screen, "YELLOW", (self.rays[i][0][0], self.rays[i][0][1]), (self.rays[i][1][0], self.rays[i][1][1]))