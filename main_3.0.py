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

    def start(self):
        self.create_spin_matrix()
        self.create_connection_matrix()
        self.create_spin_id()
        self.create_quartet()
        self.count_energy_all()

    def return_parameters(self):
        supper_array = [self.size, self.size_matrix, self.matrix_spin, self.matrix_id,
                        self.matrix_connection, self.quartet, self.energy_all, self.energy_quartet]

        return supper_array


pygame.init()


class Interface:
    def __init__(self, size, size_matrix, matrix_spin, matrix_id,
                        matrix_connection, quartet, energy_all, energy_quartet):

        self.screen = pygame.display.set_mode((1900, 1000))
        self.screen.fill((240, 230, 220))

        self.blue = (30, 50, 240)
        self.red = (240, 10, 40)
        self.green = (150, 190, 120)
        self.dark_grey = (207, 215, 230)
        self.brown = (216, 127, 0)

        self.x = 5
        self.y = 5

        self.size = size

        self.radius = 15 * (size - 1) + 30 * size + 5 + 6 + 6 + 6
        self.interval = 1900 - self.radius

        self.surface = pygame.Surface((size * 30 + 15 * (size - 1) + 12, (size * 30 + 15 * (size - 1) + 12)))
        self.surface_change = pygame.Surface((size * 30 + 15 * (size - 1) + 12, (size * 30 + 15 * (size - 1) + 12)))
        self.surface.fill(self.brown)
        self.surface_change.fill(self.brown)

        self.marker = 1
        self.block = 1

        #######################

        self.size_matrix = size_matrix
        self.matrix_spin = matrix_spin
        self.matrix_connection = matrix_connection
        self.quartet = quartet
        self.energy_all = energy_all
        self.energy_quartet = energy_quartet

    def draw_spin(self, matrix, surface):
        x, y = 6, 6

        for line in matrix:
            for spin in line:
                if spin == 1:
                    pygame.draw.rect(surface, (244, 244, 244), (x, y, 30, 30))
                elif spin == -1:
                    pygame.draw.rect(surface, (3, 3, 3), (x, y, 30, 30))
                x += 45
            x = 6
            y += 45

    def draw_connection(self, matrix_connection, surface):
        f1 = pygame.font.Font(None, 30)
        plus = f1.render("+", True, self.blue)
        minus = f1.render("-", True, self.red)

        x, y = 8 + 30, 6 + 6

        for line in range(0, self.size_matrix, 2):
            for connection in range(1, self.size_matrix - 1, 2):
                if matrix_connection[line][connection] == -1:
                    surface.blit(minus, (x, y))
                elif matrix_connection[line][connection] == 1:
                    surface.blit(plus, (x, y))
                x += 15 + 30
            x = 8 + 30
            y += 30 + 15

        x, y = 6 + 10, 6 + 27
        for line in range(1, self.size_matrix - 1, 2):
            for connection in range(0, self.size_matrix, 2):
                if matrix_connection[line][connection] == -1:
                    surface.blit(minus, (x, y))
                elif matrix_connection[line][connection] == 1:
                    surface.blit(plus, (x, y))
                x += 15 + 30
            y += 30 + 15
            x = 6 + 10

    def draw_quartets(self, quartet_energy, surface):
        pass

    def draw_button(self, coordinates):
        local_interval = (1000 - self.radius - 70) // 2
        color = ()
        x, y = 10, self.radius + local_interval

        a = 0
        if x < coordinates[0] < 160 and y < coordinates[1] < y + 70:
            a = 40

        if self.marker == 1:
            color = (150 - a, 190 - a, 120 - a)
        elif self.marker == -1:
            color = (240 - a, 40 - a, 40 - a)

        pygame.draw.rect(self.screen, color, (x, y, 150, 70))

    def change_marker(self, coordinates):
        local_interval = (1000 - self.radius - 70) // 2
        x, y = 10, self.radius + local_interval
        if x < coordinates[0] < 160 and y < coordinates[1] < y + 70:
            self.marker = self.marker * -1

    def draw_text(self):
        local_interval = (1000 - self.radius - 90) // 2
        x, y = 190, self.radius + local_interval
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(f'Start energy - {self.energy_all}', True, (50, 50, 50))

        self.screen.blit(text1, (x, y + 30))

    def draw_surface(self, quartet_energy, surface, matrix_spin, matrix_connection, x, y):
        surface.fill((145, 144, 89))
        self.draw_spin(matrix_spin, surface)
        self.draw_connection(matrix_connection, surface)

        self.screen.blit(surface, (x, y))

    def start(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.screen.fill((240, 230, 220))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.change_marker(pygame.mouse.get_pos())

                self.draw_surface(self.energy_quartet, self.surface, self.matrix_spin, self.matrix_connection, 5, 5)
                self.draw_surface(self.energy_quartet, self.surface, self.matrix_spin, self.matrix_connection,
                                  self.interval, 5)

                self.draw_button(pygame.mouse.get_pos())
                self.draw_text()
                pygame.display.flip()


size = 20
model = Model(size)
model.start()

interface = Interface(*model.return_parameters())
interface.start()

