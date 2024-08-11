import numpy as np
import random
import pygame
import sys

# size = 2
#
# dop = size * 2 - 1
#
# matrix = np.random.choice([-1, 1], (dop, dop))
#
# spins = np.random.choice([-1, 1], (size, size))
#
# a = 0
# for i in range(dop):
#     for j in range(dop):
#         if i % 2 == 0:
#             if j % 2 == 0:
#                 matrix[i][j] = a
#                 a += 1
#         else:
#             if j % 2 != 0:
#                 matrix[i][j] = -5
#
# print(matrix)


class Model:
    def __init__(self, size):
        self.size = size
        self.size_matrix = size * 2 - 1

        self.matrix_spin = []
        self.matrix_id = []
        self.matrix_connection = []

        self.quartet = []

        self.quartet_energy = []

    def create_spin_matrix(self):
        self.matrix_spin = np.random.choice([-1, 1], (self.size, self.size))

    def create_connection_matrix(self):
        a = 0
        self.matrix_connection = np.random.choice([-1, 1], (self.size_matrix, self.size_matrix))
        for i in range(self.size_matrix):
            for j in range(self.size_matrix):
                if i % 2 == 0:
                    if j % 2 == 0:
                        self.matrix_connection[i][j] = a
                        a += 1
                else:
                    if j % 2 != 0:
                        self.matrix_connection[i][j] = -5

    def create_spin_id(self):
        self.matrix_id = np.arange(self.size * self.size).reshape(self.size, self.size)

    def find_x_y(self, number):
        y = number // self.size
        x = number % self.size
        return x, y

    def return_number(self, x, y):
        return y * self.size + x

    def create_quartet(self):
        dop = []
        collector = []
        print(self.size_matrix)
        for y in range(self.size_matrix - 2):
            if y % 2 == 0:
                for x in range(self.size_matrix - 2):
                    if x % 2 == 0:
                        dop.append(self.matrix_connection[y][x:x + 3])
                        dop.append(self.matrix_connection[y + 1][x:x + 2])
                        dop.append(self.matrix_connection[y + 1][x:x + 2])
                collector.append(dop)
                dop = []
        self.quartet = collector
        print(self.quartet)

m = Model(3)
m.create_quartet()