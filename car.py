import pygame
import math
from sensor import Sensor

#class Controls:
#    def __init__(self):
#        self.forward = False
#        self.left = False
#        self.right = False
#        self.reverse = False


#x and y pas every update by doing something like x += x * cos(theta) * 0.001

class Car:
    def __init__(self, x, y, w, h):
        self.color = "WHITE"

        self.x = x - w / 2
        self.y = y - h / 2
        self.w = w
        self.h = h
        self.surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.surf.fill(self.color)
        
        #self.rect = [self.x, self.y, self.w, self.h] gewechselt zu:
        self.rect = self.surf.get_rect(center = (self.x, self.y))

        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = 5
        self.friction = 0.05

        self.angle = 0

        self.sensor = Sensor(self)

        self.checkpoint_reached = 0
        self.lap_count = 0

        self.steps_without_progress = 0 #time passed without progressing one checkpoint
        self.is_alive = True


    
    def update_position(self, track_mask):
        self.x += self.speed * math.sin(self.angle) # always apply self.speed to the player
        self.y -= self.speed * math.cos(self.angle) # same but for y

        self.rect = self.surf.get_rect(center = (self.x, self.y))

        if self.speed > self.max_speed: ## enforce a max speed
            self.speed = self.max_speed

        if self.speed < -self.max_speed: ## enforce a max speed
            self.speed = -self.max_speed

        if self.speed > 0: #slow down the car
            self.speed -= self.friction

        if self.speed < 0: #slow down the car
            self.speed += self.friction

        if abs(self.speed) < self.friction: #special check to make sure car doesnt slowly drift away
            self.speed = 0

        self.sensor.update(track_mask)

    def draw(self, screen): 
        rotated = pygame.transform.rotozoom(self.surf, -math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        screen.blit(rotated, rect)
        self.sensor.draw(screen)

    def check_for_collision(self, track_mask):
        rotated = pygame.transform.rotozoom(self.surf, -math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        car_mask = pygame.mask.from_surface(rotated)

        if track_mask.overlap(car_mask, rect.topleft) is not None:
            return True

    def checkpoint_check(self, checkpoints):
        for checkpoint in checkpoints:
            if self.rect.colliderect(checkpoint.rect):
                if checkpoint.id == 1 and self.checkpoint_reached == len(checkpoints):
                    self.lap_count += 1
                    self.checkpoint_reached = 1
                    self.steps_without_progress = 0 #reset
                    print(f"lap count: {self.lap_count}")
                elif checkpoint.id == self.checkpoint_reached + 1:
                    self.checkpoint_reached = checkpoint.id
                    self.steps_without_progress = 0