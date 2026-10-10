import pygame
import sys
from utils import Player
pygame.init()

WIDTH, HEIGHT = 1080, 720
MOVEMENT_SPEED = 10
TURNING_POWER = 4 #lower value == More turning power

player = Player(100, 100, 30, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync = 1)
pygame.display.set_caption("GameTest")

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
        player.speed -= player.acceleration
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.speed += player.acceleration
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.angle -= 0.03 * player.speed / TURNING_POWER
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.angle += 0.03 * player.speed / TURNING_POWER
    
    #Update all things
    player.update_position()

    #RENDER
    screen.fill(("BLACK"))
    player.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()