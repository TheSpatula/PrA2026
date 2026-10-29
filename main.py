import math
import pygame
import random
import sys
from car import *
from element import Element
from checkpoint import Checkpoint

pygame.init()

def update_all_cars():
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

def check_for_car_collisions():
    for idx, element in enumerate(elements):
            element.car.update_position(track_mask)
            if element.car.check_for_collision(track_mask):
                elements.pop(idx) ##TODO; we wont actually want to delete the elements, well just want to stop them from driving and give them a negative reward
            element.car.checkpoint_check(checkpoints)

#game loop
def train(duration, elements):
    timer = duration
    running = True
    while running:
        if timer < 0:
            running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #handle events
        update_all_cars()
        check_for_car_collisions()

        timer -= 1
        print(timer)

        #RENDER
        screen.fill(("BLACK"))
        for checkpoint in checkpoints: #put this above screen.blit(track, (0, 0)) to make them hegind the track
            checkpoint.draw(screen)
        screen.blit(track, (0, 0))
        for element in elements:
            element.car.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

def generate_population(number_of_elements, number_of_hidden_layer_neurons):
    elements = []
    for i in range(number_of_elements):
        elements.append(Element(number_of_hidden_layer_neurons))
    return elements

def generate_breeding_pool(elements):
    breeding_pool = []
    for element in elements:
        fitness = (element.car.lap_count * 25) + element.car.checkpoint_reached
        for _ in range(math.floor(fitness)):
            breeding_pool.append(element)
    return breeding_pool

def breed_new_population(breeding_pool):
    population = []
    for _ in range(N):
        parent1 = random.choice(breeding_pool)
        parent2 = random.choice(breeding_pool)
        population.append(parent1.breed(parent2, HIDDEN_LAYER_NEURONS))
    return population

def mutate_population(elements):
    for element in elements:
        element.mutation_chance(element.input_weights)
        element.mutation_chance(element.input_biases)
        element.mutation_chance(element.hidden_layer1_weights)
        element.mutation_chance(element.hidden_layer1_biases)
        element.mutation_chance(element.hidden_layer2_weights)
        element.mutation_chance(element.hidden_layer2_biases)

pygame.init()


WIDTH, HEIGHT = 1080, 720
MOVEMENT_SPEED = 10
TURNING_POWER = 2.5 #lower value == More turning power
FPS = 60
HIDDEN_LAYER_NEURONS = 15
N = 100
STEPS = 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync = 1)
pygame.display.set_caption("GameTest")

track = pygame.image.load("assets/RaceTrack.png").convert_alpha()
track_mask = pygame.mask.from_surface(track)

checkpoints = [Checkpoint(15, 381, 120, 20, 1), Checkpoint(4, 229, 120, 20, 2), Checkpoint(204, 20, 20, 120, 3), Checkpoint(437, 14, 20, 120, 4),
               Checkpoint(684, 24, 20, 120, 5), Checkpoint(878, 21, 20, 130, 6), Checkpoint(901, 167, 130, 20, 7), Checkpoint(847, 187, 20, 120, 8),
               Checkpoint(719, 197, 20, 100, 9), Checkpoint(585, 195, 20, 100, 10), Checkpoint(484, 198, 20, 100, 11), Checkpoint(351, 200, 20, 100, 12),
               Checkpoint(183, 326, 160, 20, 13), Checkpoint(359, 349, 20, 120, 14), Checkpoint(472, 360, 20, 120, 15), Checkpoint(609, 355, 20, 120, 16),
               Checkpoint(771, 356, 20, 120, 17), Checkpoint(933, 373, 20, 130, 18), Checkpoint(962, 540, 100, 20, 19), Checkpoint(893, 585, 20, 100, 20),
               Checkpoint(755, 510, 20, 120, 21), Checkpoint(650, 560, 20, 120, 22), Checkpoint(532, 498, 20, 120, 23), Checkpoint(415, 572, 20, 120, 24),
               Checkpoint(194, 613, 20, 100, 25), Checkpoint(10, 591, 130, 20, 26)
            ]

clock = pygame.time.Clock()

elements = generate_population(N, HIDDEN_LAYER_NEURONS)

for _ in range(15):
    train(STEPS, elements)
    breeding_pool = generate_breeding_pool(elements)
    elements = breed_new_population(breeding_pool)


pygame.quit()