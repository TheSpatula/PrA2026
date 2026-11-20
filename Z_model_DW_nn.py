import math
import random
import numpy as np
from Z_car import Car

def _random_select(weights1, weights2, child_weights):
    for i in range(len(weights1)):
        for j in range(len(weights1[i])):
            if random.choice([0, 1]):
                child_weights[i][j] = weights1[i][j]
            else:
                child_weights[i][j] = weights2[i][j]

def _mutate_weights(weights):
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.random() < 0.1:
                weights[i][j] += random.uniform(-0.05, 0.05)

class DWNNElement:
    def __init__(self, hidden_neurons, start_pos = (50, 479), start_angle = 0, color = "WHITE"):
        self.car = Car(start_pos[0], start_pos[1], 15, 30, ray_count=7)
        self.car.angle = start_angle
        self.car.color = color
        self.car.surf.fill(self.car.color)

        self.input_weights = 0.10 * np.random.randn(self.car.sensor.ray_count, hidden_neurons)
        self.input_biases = np.full((1, hidden_neurons), random.uniform(0.01, 0.1))

        self.hidden1_weights = 0.10 * np.random.randn(hidden_neurons, hidden_neurons)
        self.hidden1_biases = np.full((1, hidden_neurons), random.uniform(0.01, 0.1))

        self.hidden2_weights = 0.10 * np.random.randn(hidden_neurons, 5)
        self.hidden2_biases = np.full((1, 5), random.uniform(0.01, 0.1))

    def _feed_forward(self, inputs, weights, biases):
        return np.dot(inputs, weights) + biases


    def _relu(self, values):
        return np.maximum(0, values) ## just drop any negative values

    def choose_game_input(self):
        if len(self.car.sensor.readings) != self.car.sensor.ray_count:
            return 0

        h1 = self._relu(self._feed_forward(self.car.sensor.readings, self.input_weights, self.input_biases))
        h2 = self._relu(self._feed_forward(h1, self.hidden1_weights, self.hidden1_biases))
        out = self._feed_forward(h2, self.hidden2_weights, self.hidden2_biases)
        return int(np.argmax(out))

        return int(np.argmax(self.output))

    def breed(self, partner, hidden_neurons, start_pos = (50, 479), start_angle = 0, color = "WHITE"):
        child = DWNNElement(
            hidden_neurons,
            start_pos = start_pos,
            start_angle = start_angle,
            color = color,
        )

        _random_select(self.input_weights, partner.input_weights, child.input_weights)
        _random_select(self.input_biases, partner.input_biases, child.input_biases)
        _random_select(self.hidden1_weights, partner.hidden1_weights, child.hidden1_weights)
        _random_select(self.hidden1_biases, partner.hidden1_biases, child.hidden1_biases)
        _random_select(self.hidden2_weights, partner.hidden2_weights, child.hidden2_weights)
        _random_select(self.hidden2_biases, partner.hidden2_biases, child.hidden2_biases)
        return child

    def mutate(self):
        _mutate_weights(self.input_weights)
        _mutate_weights(self.input_biases)
        _mutate_weights(self.hidden1_weights)
        _mutate_weights(self.hidden1_biases)
        _mutate_weights(self.hidden2_weights)
        _mutate_weights(self.hidden2_biases)

class DWNNModel:
    def __init__(self, population_size = 300, hidden_neurons = 15, color = "WHITE"):
        self.population_size = population_size
        self.hidden_neurons = hidden_neurons
        self.color = color

    def generate_population(self, track):
        return [
            DWNNElement(
                self.hidden_neurons,
                start_pos = track.start_pos,
                start_angle = track.start_angle,
                color=self.color,
            )
            for _ in range(self.population_size)
        ]

    def _fitness(self, element):
        return (element.car.lap_count * 25) + element.car.checkpoint_reached

    def evolve_population(self, elements, track):
        breeding_pool = []
        for element in elements:
            score = self._fitness(element)
            if score > 0:
                for _ in range(math.floor(score)):
                    breeding_pool.append(element)

        if not breeding_pool:
            return self.generate_population(track)

        next_gen = []
        for _ in range(self.population_size):
            parent1 = random.choice(breeding_pool)
            parent2 = random.choice(breeding_pool)
            child = parent1.breed(
                parent2,
                self.hidden_neurons,
                start_pos = track.start_pos,
                start_angle = track.start_angle,
                color = self.color,
            )
            child.mutate()
            next_gen.append(child)

        return next_gen
