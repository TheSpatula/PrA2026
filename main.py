import pygame
import sys
#from car import Car
from element import Element
from checkpoint import Checkpoint

pygame.init()

WIDTH, HEIGHT = 1080, 720
MOVEMENT_SPEED = 10
TURNING_POWER = 2.5 #lower value == More turning power

elements = []

for i in range(10):
    elements.append(Element(12))

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync = 1)
pygame.display.set_caption("GameTest")

track = pygame.image.load("assets/RaceTrack.png").convert_alpha()
track_mask = pygame.mask.from_surface(track)

checkpoints = [Checkpoint(4, 380, 100, 20, 1), Checkpoint(7, 222, 100, 20, 2), Checkpoint(197, 0, 20, 100, 3), Checkpoint(428, 8, 20, 100, 4),
               Checkpoint(677, 5, 20, 100, 5), Checkpoint(889, 8, 20, 100, 6), Checkpoint(922, 158, 100, 20, 7), Checkpoint(826, 195, 20, 100, 8),
               Checkpoint(677, 185, 20, 100, 9), Checkpoint(526, 183, 20, 100, 10), Checkpoint(387, 187, 20, 100, 11), Checkpoint(287, 200, 20, 100, 12),
               Checkpoint(135, 350, 150, 20, 13), Checkpoint(345, 389, 20, 120, 14), Checkpoint(466, 391, 20, 120, 15), Checkpoint(603, 389, 20, 120, 16),
               Checkpoint(767, 392, 20, 120, 17), Checkpoint(923, 391, 20, 120, 18), Checkpoint(969, 534, 100, 20, 19), Checkpoint(884, 607, 20, 100, 20),
               Checkpoint(749, 622, 20, 100, 21), Checkpoint(613, 508, 20, 100, 22), Checkpoint(426, 613, 20, 100, 23), Checkpoint(261, 497, 20, 100, 24),
               Checkpoint(127, 635, 20, 100, 25), Checkpoint(6, 535, 100, 20, 26)
            ]

clock = pygame.time.Clock()

FPS = 60

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #handle events
    if event.type == pygame.MOUSEBUTTONDOWN:
        print(pygame.mouse.get_pos())

    keys = pygame.key.get_pressed()

    for element in elements:
        match element.choose_game_iput():
            case 0: #forward
                element.car.speed += element.car.acceleration
            case 1: #forward-left
                element.car.speed += element.car.acceleration
                element.car.angle -= 0.03 * element.car.speed / TURNING_POWER
            case 2: #forward-right
                element.car.speed += element.car.acceleration
                element.car.angle += 0.03 * element.car.speed / TURNING_POWER
            case 3: #left
                element.car.angle -= 0.03 * element.car.speed / TURNING_POWER
            case 4: #right
                element.car.angle += 0.03 * element.car.speed / TURNING_POWER


    #Update all things
    for idx, element in enumerate(elements):
        element.car.update_position(track_mask)
        if element.car.check_for_collision(track_mask):
            elements.pop(idx) ##TODO; we wont actually want to delete the elements, well just want to stop them from driving and give them a negative reward

        element.car.checkpoint_check(checkpoints)

    #RENDER
    screen.fill(("BLACK"))
    screen.blit(track, (0, 0))
    for element in elements:
        element.car.draw(screen)
    for checkpoint in checkpoints: #put this above screen.blit(track, (0, 0)) to make them hegind the track
        checkpoint.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()