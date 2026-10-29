import pygame
import numpy as np
import math
import random
from car import Car

WIDTH, HEIGHT = 1080, 720

def random_select(weights1, weights2, child_weights):
    for i in range(len(weights1)):
        for j in range(len(weights1[i])):
            if random.choice([0, 1]):
                child_weights[i][j] = weights1[i][j]
            else:
                child_weights[i][j] = weights2[i][j]

def mutation_chance(weights):
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.random() < 0.1:
                weights[i][j] += random.uniform(-0.05, 0.05)

class Element:
    def __init__(self, n_of_hidden_layer_neruons):
        self.car = Car(50, 479, 15, 30)

        self.input_weights = (0.10 * np.random.randn(self.car.sensor.ray_count, n_of_hidden_layer_neruons))
        self.input_biases = np.full((1, n_of_hidden_layer_neruons), random.uniform(0.01, 0.1))

        self.hidden_layer1_weights = (0.10 * np.random.randn(n_of_hidden_layer_neruons, n_of_hidden_layer_neruons))
        self.hidden_layer1_biases = np.full((1, n_of_hidden_layer_neruons), random.uniform(0.01, 0.1))

        self.hidden_layer2_weights = (0.10 * np.random.randn(n_of_hidden_layer_neruons, 5))
        self.hidden_layer2_biases = np.full((1, 5), random.uniform(0.01, 0.1))

    def feed_forward(self, inputs, weights, biases):
        self.output = np.dot(inputs, weights) + biases


    def activation_ReLU(self, inputs):
        self.output = np.maximum(0, inputs) ## just drop any negative values

    def choose_game_iput(self):
        if len(self.car.sensor.readings) != self.car.sensor.ray_count:
            return 0 ## sensor hasnt cast rays yet (first frame), just drive forward
        
        self.feed_forward(self.car.sensor.readings, self.input_weights, self.input_biases)
        self.activation_ReLU(self.output)
        self.feed_forward(self.output, self.hidden_layer1_weights, self.hidden_layer1_biases)
        self.activation_ReLU(self.output)
        self.feed_forward(self.output, self.hidden_layer2_weights, self.hidden_layer2_biases)

        return int(np.argmax(self.output))

    def breed(self, partner, number_of_hidden_layer_neurons):
        child = Element(number_of_hidden_layer_neurons)

        random_select(self.input_weights, partner.input_weights, child.input_weights)
        random_select(self.input_biases, partner.input_biases, child.input_biases)
        random_select(self.hidden_layer1_weights, partner.hidden_layer1_weights, child.hidden_layer1_weights)
        random_select(self.hidden_layer1_biases, partner.hidden_layer1_biases, child.hidden_layer1_biases)
        random_select(self.hidden_layer2_weights, partner.hidden_layer2_weights, child.hidden_layer2_weights)
        random_select(self.hidden_layer2_biases, partner.hidden_layer2_biases, child.hidden_layer2_biases)
        return child


