import numpy as np
import random
import pygame
import sys
import os


class Model:
    def __init__(self, size):
        self.size = size
        self.size_matrix = size * 2 - 1

        self.matrix_spin = []
        self.matrix_id = []
        self.matrix_connection = []
        self.matrix_spin_change = []

        self.quartet = []

        self.energy_all = 0
        self.energy_all_change = 0

        self.frustration_row = []
        self.frustration_col = []

        self.frustration_row_ch = []
        self.frustration_col_ch = []

    def create_spin_matrix(self):
        self.matrix_spin = np.random.choice([-1, 1], (self.size, self.size))
        self.matrix_spin_change = self.matrix_spin.copy()

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

    def spin(self, x, y, matrix):
        matrix[y][x] = matrix[y][x] * -1

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

    def count_energy(self, quartet_one, matrix_spin):
        x, y = self.find_x_y(quartet_one[0][0])
        a = matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[0][2])
        b = matrix_spin[y][x]
        en_12 = a * b * quartet_one[0][1]

        x, y = self.find_x_y(quartet_one[0][0])
        a = matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[2][0])
        b = matrix_spin[y][x]
        en_13 = a * b * quartet_one[1][0]

        x, y = self.find_x_y(quartet_one[0][2])
        a = matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[2][2])
        b = matrix_spin[y][x]
        en_24 = a * b * quartet_one[1][2]

        x, y = self.find_x_y(quartet_one[2][0])
        a = matrix_spin[y][x]
        x, y = self.find_x_y(quartet_one[2][2])
        b = matrix_spin[y][x]
        en_43 = a * b * quartet_one[2][1]

        energy_main = -1 * (en_12 + en_13 + en_24 + en_43)

        return energy_main

    def count_energy_all(self):
        if len(self.quartet) == 0:
            return 0

        for line in self.quartet:
            for q in line:
                self.energy_all += self.count_energy(q, self.matrix_spin)

        for line in self.quartet:
            for q in line:
                self.energy_all_change += self.count_energy(q, self.matrix_spin_change)

    def count_frustration(self):
        dop = []
        colletor = []

        for line in range(0, self.size_matrix, 2):
            for q in range(0, self.size_matrix - 1, 2):
                spin_1 = self.matrix_connection[line][q]
                x, y = self.find_x_y(spin_1)
                spin_1 = self.matrix_spin[y][x]

                spin_2 = self.matrix_connection[line][q + 2]
                x, y = self.find_x_y(spin_2)
                spin_2 = self.matrix_spin[y][x]

                if spin_1 * spin_2 * self.matrix_connection[line][q + 1] < 0:
                    dop.append(0)
                else:
                    dop.append(1)
            colletor.append(dop)
            dop = []
        self.frustration_row = colletor

        dop = []
        colletor = []

        for col in range(0, self.size_matrix, 2):
            for q in range(0, self.size_matrix - 1, 2):
                spin_1 = self.matrix_connection[q][col]
                x, y = self.find_x_y(spin_1)
                spin_1 = self.matrix_spin[y][x]

                spin_2 = self.matrix_connection[q + 2][col]
                x, y = self.find_x_y(spin_2)
                spin_2 = self.matrix_spin[y][x]

                if spin_1 * spin_2 * self.matrix_connection[q + 1][col] < 0:
                    dop.append(0)
                else:
                    dop.append(1)
            colletor.append(dop)
            dop = []
        self.frustration_col = colletor

    def count_frustration_change(self):
        self.frustration_row_ch = []
        self.frustration_col_ch = []
        dop = []
        colletor = []

        for line in range(0, self.size_matrix, 2):
            for q in range(0, self.size_matrix - 1, 2):
                spin_1 = self.matrix_connection[line][q]
                x, y = self.find_x_y(spin_1)
                spin_1 = self.matrix_spin_change[y][x]

                spin_2 = self.matrix_connection[line][q + 2]
                x, y = self.find_x_y(spin_2)
                spin_2 = self.matrix_spin_change[y][x]

                if spin_1 * spin_2 * self.matrix_connection[line][q + 1] < 0:
                    dop.append(0)
                else:
                    dop.append(1)
            colletor.append(dop)
            dop = []
        self.frustration_row_ch = colletor

        dop = []
        colletor = []

        for col in range(0, self.size_matrix, 2):
            for q in range(0, self.size_matrix - 1, 2):
                spin_1 = self.matrix_connection[q][col]
                x, y = self.find_x_y(spin_1)
                spin_1 = self.matrix_spin_change[y][x]

                spin_2 = self.matrix_connection[q + 2][col]
                x, y = self.find_x_y(spin_2)
                spin_2 = self.matrix_spin_change[y][x]

                if spin_1 * spin_2 * self.matrix_connection[q + 1][col] < 0:
                    dop.append(0)
                else:
                    dop.append(1)
            colletor.append(dop)
            dop = []
        self.frustration_col_ch = colletor

    def algorithm_1(self):
        for operation in range(0, self.size * 2 - 1, 1):

            if operation % 2 == 0:
                for q in range(0, self.size_matrix - 1, 2):

                    x, y = self.find_x_y(self.matrix_connection[operation][q])
                    a = self.matrix_spin_change[y][x]

                    b = self.matrix_connection[operation][q + 1]

                    x, y = self.find_x_y(self.matrix_connection[operation][q + 2])
                    c = self.matrix_spin_change[y][x]
                    if a * b * c < 0:
                        x, y = self.find_x_y(self.matrix_connection[operation][q + 2])
                        self.spin(x, y, self.matrix_spin_change)

            elif operation % 2 != 0:
                for q in range(0, self.size_matrix - 1, 2):

                    x, y = self.find_x_y(self.matrix_connection[operation - 1][q])
                    a = self.matrix_spin_change[y][x]

                    b = self.matrix_connection[operation][q]

                    x, y = self.find_x_y(self.matrix_connection[operation + 1][q])
                    c = self.matrix_spin_change[y][x]
                    if a * b * c < 0:
                        x, y = self.find_x_y(self.matrix_connection[operation + 1][q])
                        self.spin(x, y, self.matrix_spin_change)

    def algorith_2(self):
        counter = 0
        energy_main = 0
        energy_new = 0

        for line in range(0, self.size_matrix - 1, 4):
            spin_line = self.matrix_connection[line]

            if 0 == 0:
                for q in self.quartet[counter]:
                    energy_main += self.count_energy(q, self.matrix_spin_change)

                for spin in range(0, self.size_matrix, 2):
                    spin = self.matrix_connection[line][spin]
                    x, y = self.find_x_y(spin)
                    self.spin(x, y, self.matrix_spin_change)

                for q in self.quartet[counter]:
                    energy_new += self.count_energy(q, self.matrix_spin_change)
                print(f'old{energy_main}, new{energy_new}')
                if energy_main < energy_new:
                    for spin in range(0, self.size_matrix, 2):
                        spin = self.matrix_connection[line][spin]
                        x, y = self.find_x_y(spin)
                        self.spin(x, y, self.matrix_spin_change)

            energy_main = 0
            energy_new = 0
            counter += 2
            self.count_frustration_change()
            self.energy_all_change, self.energy_all = 0, 0
            self.count_energy_all()

    def algorithm_3(self):
        counter = 0
        energy_main = 0
        energy_new = 0

        for col in range(0, self.size_matrix - 1, 4):

            for q in range(len(self.quartet)):
                energy_main += self.count_energy(self.quartet[counter][q], self.matrix_spin_change)

            for spin in range(self.size_matrix):
                spin = self.matrix_connection[spin][col]
                x, y = self.find_x_y(spin)
                self.spin(x, y, self.matrix_spin_change)

            for q in range(len(self.quartet)):
                energy_new += self.count_energy(self.quartet[counter][q], self.matrix_spin_change)

            print(f'old{energy_main}, new{energy_new}')
            if energy_main < energy_new:
                for spin in range(self.size_matrix):
                    spin = self.matrix_connection[spin][col]
                    x, y = self.find_x_y(spin)
                    self.spin(x, y, self.matrix_spin_change)

            energy_main = 0
            energy_new = 0
            counter += 2
            self.count_frustration_change()
            self.energy_all_change, self.energy_all = 0, 0
            self.count_energy_all()

    def start(self):
        self.create_spin_matrix()
        self.create_connection_matrix()
        self.create_spin_id()
        self.create_quartet()

        self.count_frustration()

        self.algorithm_1()

        self.count_frustration_change()
        self.count_energy_all()

    def clear(self):
        self.matrix_spin = []
        self.matrix_id = []
        self.matrix_connection = []
        self.matrix_spin_change = []

        self.quartet = []

        self.energy_all = 0
        self.energy_all_change = 0

        self.frustration_row = []
        self.frustration_col = []

        self.frustration_row_ch = []
        self.frustration_col_ch = []

    def continue_algorithm_1(self):
        self.energy_all_change = 0
        self.energy_all = 0
        self.frustration_col_ch = []
        self.frustration_row_ch = []

        self.algorithm_1()
        self.count_frustration_change()
        self.count_energy_all()

    def check_files(self, file_manager, size, size_matrix, connection_matrix_extra):
        self.size = size
        self.size_matrix = size_matrix

        letter = []

        for matrix in connection_matrix_extra:
            self.matrix_connection = file_manager.create_connection_matrix(connection_matrix_extra[matrix])

            self.create_spin_matrix()
            self.create_spin_id()
            self.create_quartet()

            self.count_frustration()

            self.algorithm_1()

            self.count_frustration_change()
            self.count_energy_all()
            #######################
            with open(f"files/{matrix}/{file_manager.res_files[matrix]}", 'r') as f:
                for i in range(4):
                    f.readline()
                energy_original = f.readline()


            message = \
                f"{file_manager.con_files[matrix]} \t energy_start - {self.energy_all} \t|\t " \
                f"energy_final - {self.energy_all_change} \t energy_original - {energy_original.split()[1]}\n"
            letter.append(message)

            with open("results.txt", "w+") as file:
                file.writelines(letter)
                file.close()

    def return_parameters(self):
        supper_array = [self.size, self.size_matrix, self.matrix_spin, self.matrix_id, self.matrix_connection,
                        self.quartet, self.energy_all, self.frustration_row, self.matrix_spin_change,
                        self.frustration_col, self.frustration_row_ch, self.frustration_col_ch, self.energy_all_change]

        return supper_array


pygame.init()


class Interface:
    def __init__(self, size, size_matrix, matrix_spin, matrix_id, matrix_connection, quartet, energy_all,
                 frustration_row, matrix_spin_change, frustration_col,
                 frustration_row_ch, frustration_col_ch, energy_all_change):

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
        self.frustration_row = frustration_row
        self.frustration_col = frustration_col
        self.frustration_row_ch = frustration_row_ch
        self.frustration_col_ch = frustration_col_ch
        self.energy_all_change = energy_all_change
        self.matrix_spin_change = matrix_spin_change

    def connect(self, model):
        self.model = model

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

    def draw_frustration(self, frustration_row, frustration_col, surface):
        x, y = 3, 3
        for line in frustration_row:
            for q in line:
                if q == 0:
                    pygame.draw.rect(surface, (255, 0, 255), (x, y, 30 + 30 + 15 + 6, 30 + 6), 4)
                x += 15 + 30
            x = 3
            y += 30 + 15
        ################
        x, y = 3, 3
        for col in frustration_col:
            for q in col:
                if q == 0:
                    pygame.draw.rect(surface, (128, 0, 128), (x, y, 30 + 6, 30 + 30 + 15 + 6), 4)
                y += 15 + 30
            y = 3
            x += 30 + 15

    def change_marker(self, coordinates):
        local_interval = (1000 - self.radius - 70) // 2
        x, y = 10, self.radius + local_interval
        if x < coordinates[0] < 160 and y < coordinates[1] < y + 70:
            self.marker = self.marker * -1

    def restart(self, size, size_matrix, matrix_spin, matrix_id, matrix_connection, quartet, energy_all,
                 frustration_row, matrix_spin_change, frustration_col,
                 frustration_row_ch, frustration_col_ch, energy_all_change):
        self.matrix_spin = matrix_spin
        self.matrix_connection = matrix_connection
        self.quartet = quartet
        self.energy_all = energy_all
        self.frustration_row = frustration_row
        self.frustration_col = frustration_col
        self.frustration_row_ch = frustration_row_ch
        self.frustration_col_ch = frustration_col_ch
        self.energy_all_change = energy_all_change
        self.matrix_spin_change = matrix_spin_change

    def draw_text(self):
        local_interval = (1000 - self.radius - 90) // 2
        x, y = 190, self.radius + local_interval
        f1 = pygame.font.Font(None, 36)

        text1 = f1.render(f'Start energy -    [{self.energy_all}]', True, (50, 50, 50))
        text2 = f1.render(f'Final energy -    [{self.energy_all_change}]', True, (50, 50, 50))

        text3 = f1.render('ПКМ - генерация новой матрицы', True, (50, 50, 50))
        text4 = f1.render('колесико вверх - алгоритм 2', True, (50, 50, 50))

        self.screen.blit(text1, (x, y + 30))
        self.screen.blit(text2, (x + 300, y + 30))
        self.screen.blit(text3, (x + 600, y + 30))
        self.screen.blit(text4, (x + 1100, y + 30))

    def draw_surface(self, frustration_row, frustration_col, surface, matrix_spin, matrix_connection, x, y):
        surface.fill((145, 144, 89))
        self.draw_spin(matrix_spin, surface)
        self.draw_connection(matrix_connection, surface)
        if self.marker == 1:
            self.draw_frustration(frustration_row, frustration_col, surface)
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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.model.clear()
                        self.model.start()
                        self.restart(*self.model.return_parameters())

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.model.algorith_2()
                        self.restart(*self.model.return_parameters())

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 5:
                        self.model.algorithm_3()
                        self.restart(*self.model.return_parameters())

                ######################################
                self.draw_surface(self.frustration_row, self.frustration_col, self.surface,
                                  self.matrix_spin, self.matrix_connection, 5, 5)
                self.draw_surface(self.frustration_row_ch, self.frustration_col_ch, self.surface_change,
                                  self.matrix_spin_change, self.matrix_connection, self.interval, 5)

                self.draw_button(pygame.mouse.get_pos())
                self.draw_text()

                pygame.display.flip()


class File_manager:
    def __init__(self):
        self.directories = []
        self.con_files = {}
        self.res_files = {}

        self.connection_matrix_extra = {}

        self.matrix_connection = []

        self.size = 0
        self.size_matrix = 0

    def find_dirs(self):
        for filename in os.listdir("files"):
            self.directories.append(filename)

    def create_connection_directories(self):
        if self.directories == 0:
            return 0

        for dir in self.directories:

            for file in os.listdir(f"files/{dir}"):
                if "cell" in file:
                    self.con_files[f"{dir}"] = file
                if "gem" in file:
                    self.res_files[f"{dir}"] = file

    def find_size(self):
        a = ''
        for file in os.listdir(f'files/{self.directories[0]}'):
            if "gem" in file:
                a = file
                break
        with open(f'files/{self.directories[0]}/{a}', "r") as file:
            for line in file:
                self.size = int(line)
                self.size_matrix = self.size * 2 - 1
                break
            file.close()

    def create_connection_matrix_extra(self):
        for one in self.con_files:
            way = f'files/{one}/{self.con_files[one]}'
            with open(way, "r") as file:
                self.connection_matrix_extra[one] = np.array(file.readlines())
                file.close()

        for cell in self.connection_matrix_extra:
            self.connection_matrix_extra[cell] = \
                np.array(list(map(list, (map(int, (i[0:-2]).split()) for i in self.connection_matrix_extra[cell]))))

    def find_x_y(self, number):
        y = number // self.size
        x = number % self.size
        return x, y

    def return_number(self, x, y):
        return y * self.size + x

    def create_connection_matrix(self, connection_matrix_extra):
        a = 0
        self.matrix_connection = np.random.choice([0], (self.size_matrix, self.size_matrix))
        for i in range(self.size_matrix):
            for j in range(self.size_matrix):
                if i % 2 == 0:
                    if j % 2 == 0:
                        self.matrix_connection[i][j] = a
                        a += 1
                else:
                    if j % 2 != 0:
                        self.matrix_connection[i][j] = -5

        counter = 0
        for line in range(0, self.size_matrix - 1, 2):
            for spin in range(0, self.size_matrix - 1, 2):

                self.matrix_connection[line][spin + 1] = connection_matrix_extra[counter][counter + 1]

                # x, y = self.find_x_y(spin)
                # a = self.return_number(x, y + 1)
                self.matrix_connection[line + 1][spin] = connection_matrix_extra[counter][counter + 8]

                if spin % (self.size - 2) == 0:
                    self.matrix_connection[line + 1][spin + 2] = connection_matrix_extra[counter + 1][counter + 9]
                counter += 1
            counter += 1

        for spin in range(0, self.size_matrix - 1, 2):
            self.matrix_connection[self.size_matrix - 1][spin + 1] = connection_matrix_extra[counter][counter + 1]
            counter += 1
        self.matrix_connection = np.array(self.matrix_connection)
        return self.matrix_connection

    def start(self):
        self.find_dirs()
        self.create_connection_directories()
        self.find_size()
        self.create_connection_matrix_extra()

    def return_parameters(self):
        array = [self.size, self.size_matrix, self.connection_matrix_extra]
        return array


class Model_for_file:
    def __init__(self, size, connection_matrix):
        self. size = size

        self.quartet = []
        self.matrix_id = []

        self.connection_matrix = connection_matrix

        self.matrix_spin = []
        self.matrix_spin_change = []

    def find_x_y(self, number):
        y = number // self.size
        x = number % self.size
        return x, y

    def return_number(self, x, y):
        return y * self.size + x

    def create_quartet(self):
        quartet = []

        dop = []

        for number in range(self.size * self.size):
            x, y = self.find_x_y(number)

            if x < self.size - 1:
                dop.append(self.return_number(x + 1, y))
            if y < self.size - 1:
                dop.append(self.return_number(x + 1, y + 1))
                dop.append(self.return_number(x, y + 1))
            if len(dop) == 3:
                dop.append(self.return_number(x, y))

            if len(dop) == 4:
                quartet.append(dop)
            dop = []

        self.quartet = np.array(quartet)
        # self.quartet = list(map(list, (i + 1 for i in self.quartet)))
        # print(self.quartet)

    def create_matrix_id(self):
        dop = []
        collector = []

        for spin in range(1, self.size * self.size + 1):
            dop.append(spin - 1)
            if spin != 0 and spin % self.size == 0:
                collector.append(dop)
                dop = []
        self.matrix_id = np.array(collector)
        print(self.matrix_id)

    def count_energy(self, one_quartet, connection_matrix, spin_matrix):
        a, b, c, d = one_quartet[3], one_quartet[0], one_quartet[2], one_quartet[1]
        en_ab, en_bd, en_dc, en_ac = 0, 0, 0, 0
        energy = 0

        x_a, y_a = self.find_x_y(a)
        x_b, y_b = self.find_x_y(b)
        x_c, y_c = self.find_x_y(c)
        x_d, y_d = self.find_x_y(d)

        spin_a = spin_matrix[y_a][x_a]
        spin_b = spin_matrix[y_b][x_b]
        spin_c = spin_matrix[y_c][x_c]
        spin_d = spin_matrix[y_d][x_d]

        en_ab = spin_a * spin_b * connection_matrix[a][b]
        en_bd = spin_b * spin_d * connection_matrix[b][d]
        en_dc = spin_c * spin_d * connection_matrix[d][c]
        en_ac = spin_a * spin_c * connection_matrix[c][a]

        energy = en_ab + en_bd + en_dc + en_ac
        return energy

    def generate_spin_matrix(self):
        self.matrix_spin = np.random.choice([-1, 1], (self.size, self.size))
        self.matrix_spin_change = self.matrix_spin.copy()

    def spin(self, x, y, spin_matrix):
        spin_matrix[y][x] = spin_matrix[y][x] * -1










# f = File_manager()
# f.find_dirs()
# f.create_connection_directories()
# f.find_size()
# print(f.size, f.size_matrix)
# f.create_connection_matrix_extra()
# for i in f.connection_matrix_extra:
#     f.create_connection_matrix(f.connection_matrix_extra[i])
#     break


# size = 20
# model = Model(size)
# model.start()
#
#
# interface = Interface(*model.return_parameters())
# interface.connect(model)
# interface.start()

file_manager = File_manager()
model = Model(8)

file_manager.start()
print(file_manager.res_files)
model.check_files(file_manager, *file_manager.return_parameters())
