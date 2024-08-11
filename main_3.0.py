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

        self.energy_all = 0
        self.energy_quartet = []

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
        line = []
        collector = []

        if len(self.matrix_connection) == 0:
            return 0

        for y in range(self.size_matrix - 2):
            if y % 2 == 0:
                for x in range(self.size_matrix - 2):
                    if x % 2 == 0:
                        dop.append(self.matrix_connection[y][x:x + 3])
                        dop.append(self.matrix_connection[y + 1][x:x + 3])
                        dop.append(self.matrix_connection[y + 2][x:x + 3])
                    if len(dop) == 3:
                        line.append(dop)
                        dop = []
            if len(line) > 0:
                collector.append(line)
                line = []
        self.quartet = collector

    def count_energy(self, quartet_one):
        x, y = self.find_x_y(quartet_one[0][0])
        a = self.matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[0][2])
        b = self.matrix_spin[y][x]
        en_12 = a * b * quartet_one[0][1]

        x, y = self.find_x_y(quartet_one[0][0])
        a = self.matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[2][0])
        b = self.matrix_spin[y][x]
        en_13 = a * b * quartet_one[1][0]

        x, y = self.find_x_y(quartet_one[0][2])
        a = self.matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[2][2])
        b = self.matrix_spin[y][x]
        en_24 = a * b * quartet_one[1][2]

        x, y = self.find_x_y(quartet_one[2][0])
        a = self.matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[2][2])
        b = self.matrix_spin[y][x]
        en_43 = a * b * quartet_one[2][1]

        energy_main = -1 * (en_12 + en_13 + en_24 + en_43)

        return energy_main

    def count_energy_all(self):
        if len(self.quartet) == 0:
            return 0

        for line in self.quartet:
            for q in line:
                self.energy_all += self.count_energy(q)




m = Model(3)
m.create_connection_matrix()
m.create_quartet()
m.create_spin_matrix()
m.count_energy_all()
print(f"energy   {m.energy_all}")
print(m.matrix_connection)
print(m.matrix_spin)
