import pygame
import numpy as np
import math
import random
from car import Car

WIDTH, HEIGHT = 1080, 720

class Element:
    def __init__(self, n_of_hidden_layer_neruons):
        self.car = Car(50, 479, 15, 30)

        self.input_weights = (0.10 * np.random.randn(self.car.sensor.ray_count, n_of_hidden_layer_neruons))
        self.input_biases = np.zeros((1, n_of_hidden_layer_neruons))

        self.hidden_layer1_weights = (0.10 * np.random.randn(n_of_hidden_layer_neruons, n_of_hidden_layer_neruons))
        self.hidden_layer1_biases = np.zeros((1, n_of_hidden_layer_neruons))

        self.hidden_layer2_weights = (0.10 * np.random.randn(n_of_hidden_layer_neruons, 5))
        self.hidden_layer2_biases = np.zeros((1, 5))

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

    def crossbread():
        pass
