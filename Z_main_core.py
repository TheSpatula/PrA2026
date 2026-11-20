import pygame
import sys
from Z_tracks import load_track_1
from Z_model_DW_nn import DWNNModel

pygame.init()

pygame.init()

WIDTH, HEIGHT = 1080, 720
TURNING_POWER = 2.5
FPS = 60
N_PER_MODEL = 300
STEPS = 1000
GENERATIONS = 15

# choose which models should race/train together
ACTIVE_MODELS = ["DW"]

def build_models(choices):
    models = []
    for choice in choices:
        if choice == "DW":
            models.append(DWNNModel(population_size = N_PER_MODEL, hidden_neurons=15, color="WHITE"))
        elif choice == "second":
            raise NotImplementedError("Create model_second.py and append SecondModel(population_size=N_PER_MODEL) here.")
        else:
            raise ValueError(f"Unknown model choice: {choice}")
    if not models:
        raise ValueError("ACTIVE_MODELS cannot be empty.")
    return models

def update_all_cars(models):
    for model in models:
        for element in model.elements:
            if not element.car.is_alive:
                continue
            match element.choose_game_input():
                case 0:
                    element.car.speed += element.car.acceleration
                case 1:
                    element.car.speed += element.car.acceleration
                    element.car.angle -= 0.03 * element.car.speed / TURNING_POWER
                case 2:
                    element.car.speed += element.car.acceleration
                    element.car.angle += 0.03 * element.car.speed / TURNING_POWER
                case 3:
                    element.car.angle -= 0.03 * element.car.speed / TURNING_POWER
                case 4:
                    element.car.angle += 0.03 * element.car.speed / TURNING_POWER

def check_for_car_collisions(models, track):
    for model in models:
        for element in model.elements:
            if not element.car.is_alive:
                continue

            element.car.update_position(track.mask)
            element.car.steps_without_progress += 1

            if element.car.check_for_collision(track.mask) or element.car.steps_without_progress > 300:
                element.car.is_alive = False
                element.car.speed = 0 #freez instead of delete, so we can breed them after
            else:
                element.car.checkpoint_check(track.checkpoints)

def all_cars_dead(models):
    return all(
        not element.car.is_alive
        for model in models
        for element in model.elements
    )

def train(duration, models, track, screen, clock):
    timer = duration
    running = True
    while running:
        if timer < 0:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        update_all_cars(models)
        check_for_car_collisions(models, track)

        if all_cars_dead(models):
            running = False

        timer -= 1

        screen.fill("BLACK")
        track.draw(screen, show_checkpoints=True)
        for model in models:
            for element in model.elements:
                if element.car.is_alive:
                    element.car.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
    pygame.display.set_caption("Multi-Model Race & Training")
    clock = pygame.time.Clock()

    track = load_track_1()
    models = build_models(ACTIVE_MODELS)

    for model in models:
        model.elements = model.generate_population(track)

    for generation in range(GENERATIONS):
        train(STEPS, models, track, screen, clock)
        for model in models:
            model.elements = model.evolve_population(model.elements, track)
        print(f"Finished generation {generation + 1}/{GENERATIONS}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()