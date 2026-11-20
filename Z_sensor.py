import pygame
import math
from Z_utils import lerp

class Sensor:
    def __init__(self, car, ray_count = 7, ray_length = 250, ray_spread = math.pi):
        self.car = car
        self.ray_count = ray_count
        self.ray_length = ray_length
        self.ray_spread = ray_spread

        self.rays = []
        self.readings = []


    def update(self, track_mask):
        self.cast_rays(track_mask)
    
    def cast_rays(self, track_mask):
        self.rays = []
        self.readings = []
        step = 2
        for ray_idx in range(self.ray_count):
            RAY_ANGLE = lerp(
                self.ray_spread / 2,
                -self.ray_spread / 2,
                ray_idx / (self.ray_count - 1),
            ) - self.car.angle

            START = (self.car.x, self.car.y)
            direction = (-math.sin(RAY_ANGLE), -math.cos(RAY_ANGLE))
            END = (
                self.car.x - math.sin(RAY_ANGLE) * self.ray_length,
                self.car.y - math.cos(RAY_ANGLE) * self.ray_length,
            )

            reading = 1
            for dist in range(0, int(self.ray_length), step):
                point = (START[0] + direction[0] * dist, START[1] + direction[1] * dist)

                if 0 <= point[0] < track_mask.get_size()[0] and 0 <= point[1] < track_mask.get_size()[1]:
                    if track_mask.get_at(point):
                        END = point
                        reading = dist / self.ray_length
                        break

            self.rays.append((START, END))  # populate the list with the calculated distance
            self.readings.append(reading)

    def draw(self, screen): # indexing is grabbing the x ans y pos for the line that needs to be drawn
        for i in range(self.ray_count):
            pygame.draw.line(
                screen,
                "YELLOW",
                (self.rays[i][0][0], self.rays[i][0][1]),
                (self.rays[i][1][0], self.rays[i][1][1]),
            )