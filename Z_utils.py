import math
import pygame

def lerp(A, B, t): #lerp meaning "linear interpolation"
    return A + (B - A) * t