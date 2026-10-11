import pygame
import sys
from car import Car

pygame.init()

WIDTH, HEIGHT = 1080, 720
MOVEMENT_SPEED = 10
TURNING_POWER = 2.5 #lower value == More turning power

car = Car(50, HEIGHT * .90, 15, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync = 1)
pygame.display.set_caption("GameTest")

track = pygame.image.load("assets/RaceTrack.png").convert_alpha()
track_mask = pygame.mask.from_surface(track)

clock = pygame.time.Clock()
FPS = 60

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #handle events
    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        car.speed -= car.acceleration
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        car.speed += car.acceleration
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        car.angle -= 0.03 * car.speed / TURNING_POWER
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        car.angle += 0.03 * car.speed / TURNING_POWER
    
    #Update all things
    car.update_position()
    print(car.check_for_collision(track_mask))

    #RENDER
    screen.fill(("BLACK"))
    car.draw(screen)
    screen.blit(track, (0, 0))
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()