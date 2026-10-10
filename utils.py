import pygame
import math

#class Controls:
#    def __init__(self):
#        self.forward = False
#        self.left = False
#        self.right = False
#        self.reverse = False


#x and y pas every update by doing something like x += x * cos(theta) * 0.001

class Player:
    def __init__(self, x, y, w, h):
        self.color = "RED"

        self.x = x - w / 2
        self.y = y - h / 2
        self.w = w
        self.h = h
        self.surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.surf.fill(self.color)
        self.rect = [self.x, self.y, self.w, self.h]

        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = 10
        self.friction = 0.05

        self.angle = math.pi


    
    def update_position(self):
        self.x += self.speed * math.sin(self.angle) # always apply self.speed to the player
        self.y -= self.speed * math.cos(self.angle) # same but for y

        self.rect = self.surf.get_rect(center=(self.x, self.y))

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

    def draw(self, screen): 
        rotated = pygame.transform.rotozoom(self.surf, -math.degrees(self.angle), 1)
        rect = rotated.get_rect(center = (self.x, self.y))
        screen.blit(rotated, rect)