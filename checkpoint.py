import pygame
import numpy

class Checkpoint:
    def __init__(self, x, y, w, h, id):
        self.rect = pygame.Rect(x, y, w, h)
        self.id = id

    def draw(self, screen):
        pygame.draw.rect(screen, "BLUE", self.rect)