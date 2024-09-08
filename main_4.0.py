import numpy as np
import random
import pygame
import sys
import os
from itertools import product


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
        energy_start = 0
        energy_final = 0
        energy_line = 0
        for line in range(0, self.size_matrix, 2):
            for connection in range(0, self.size_matrix - 1, 2):
                one = self.matrix_connection[line][connection]
                x_one, y_one = self.find_x_y(one)
                two = self.matrix_connection[line][connection + 2]
                x_two, y_two = self.find_x_y(two)

                spin_1 = self.matrix_spin[y_one][x_one]
                spin_2 = self.matrix_spin[y_two][x_two]
                energy_line += spin_1 * spin_2 * self.matrix_connection[line][connection + 1]
        for connection in range(0, self.size_matrix, 2):
            for line in range(0, self.size_matrix - 1, 2):
                one = self.matrix_connection[line][connection]
                x_one, y_one = self.find_x_y(one)
                two = self.matrix_connection[line + 2][connection]
                x_two, y_two = self.find_x_y(two)

                spin_1 = self.matrix_spin[y_one][x_one]
                spin_2 = self.matrix_spin[y_two][x_two]
                energy_line += spin_1 * spin_2 * self.matrix_connection[line + 1][connection]
        self.energy_all = -1 * energy_line

        energy_line = 0
        for line in range(0, self.size_matrix, 2):
            for connection in range(0, self.size_matrix - 1, 2):
                one = self.matrix_connection[line][connection]
                x_one, y_one = self.find_x_y(one)
                two = self.matrix_connection[line][connection + 2]
                x_two, y_two = self.find_x_y(two)

                spin_1 = self.matrix_spin_change[y_one][x_one]
                spin_2 = self.matrix_spin_change[y_two][x_two]
                energy_line += spin_1 * spin_2 * self.matrix_connection[line][connection + 1]
        for connection in range(0, self.size_matrix, 2):
            for line in range(0, self.size_matrix - 1, 2):
                one = self.matrix_connection[line][connection]
                x_one, y_one = self.find_x_y(one)
                two = self.matrix_connection[line + 2][connection]
                x_two, y_two = self.find_x_y(two)

                spin_1 = self.matrix_spin_change[y_one][x_one]
                spin_2 = self.matrix_spin_change[y_two][x_two]
                energy_line += spin_1 * spin_2 * self.matrix_connection[line + 1][connection]
        self.energy_all_change = -1 * energy_line

        # if len(self.quartet) == 0:
        #     return 0
        #
        # for line in self.quartet:
        #     for q in line:
        #         self.energy_all += self.count_energy(q, self.matrix_spin)
        #
        # for line in self.quartet:
        #     for q in line:
        #         self.energy_all_change += self.count_energy(q, self.matrix_spin_change)

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

                energy_main = self.energy_all_change
                self.count_energy_all()

                print(f'old{energy_main}, new{self.energy_all_change}')
                if energy_main < self.energy_all_change:
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

    def algorithm_4(self):
        self.create_quartet()
        frustrate_quartet = 0
        for line in self.quartet:
            for q in line:
                minus = 0
                l_1 = q[0]
                l_2 = q[1]
                l_3 = q[2]
                a, b, c, d = 0, 0, 0, 0

                x, y = self.find_x_y(l_1[0])
                a = self.matrix_spin_change[y][x]

                x, y = self.find_x_y(l_1[2])
                b = self.matrix_spin_change[y][x]

                x, y = self.find_x_y(l_3[2])
                c = self.matrix_spin_change[y][x]

                x, y = self.find_x_y(l_3[0])
                d = self.matrix_spin_change[y][x]

                if a * l_1[1] * b == -1:
                    minus += 1
                if d * l_3[1] * c == -1:
                    minus += 1

                if a * l_2[0] * d == -1:
                    minus += 1
                if b * l_2[2] * c == -1:
                    minus += 1

                if minus % 2 != 0:
                    frustrate_quartet += 1

        self.count_energy_all()

        return frustrate_quartet
        # if 1 <= frustrate_quartet <= 2:
        #     while self.energy_all_change != -10:
        #         self.algorithm_1()
        #         x, y = random.choice([i for i in range(self.size)]), random.choice([i for i in range(self.size)])
        #         self.spin(x, y, self.matrix_spin_change)
        #         self.count_energy_all()
        #         print(f"fr {frustrate_quartet} en {self.energy_all_change} x {x}, y {y}")
        #
        # elif frustrate_quartet > 2:
        #     while self.energy_all_change != -8:
        #         x, y = random.choice([i for i in range(self.size)]), random.choice([i for i in range(self.size)])
        #         self.spin(x, y, self.matrix_spin_change)
        #         self.count_energy_all()
        #         print(f"fr {frustrate_quartet} en {self.energy_all_change} x {x}, y {y}")
        #
        # elif frustrate_quartet == 0:
        #     while self.energy_all_change != -12:
        #         x, y = random.choice([i for i in range(self.size)]), random.choice([i for i in range(self.size)])
        #         self.spin(x, y, self.matrix_spin_change)
        #         self.count_energy_all()
        #         print(f"fr {frustrate_quartet} en {self.energy_all_change} x {x}, y {y}")
        #
        # self.count_energy_all()

    def algorithm_5(self):
        count = 0
        quartet_frustration_array = []
        dop = []
        ch_x, ch_y = 0, 0

        for i in self.quartet:
            for j in i:
                dop.append(self.check_quartet(j))
                print(self.check_quartet(j))
            quartet_frustration_array.append(dop)
            print()
            dop = []

        for line in self.quartet:
            for q in line:
                frustration = self.check_quartet(q)

                l_1 = q[0]
                l_2 = q[1]
                l_3 = q[2]
                a, b, c, d = 0, 0, 0, 0

                x_a, y_a = self.find_x_y(l_1[0])
                a = self.matrix_spin_change[y_a][x_a]

                x_b, y_b = self.find_x_y(l_1[2])
                b = self.matrix_spin_change[y_b][x_b]

                x_c, y_c = self.find_x_y(l_3[2])
                c = self.matrix_spin_change[y_c][x_c]

                x_d, y_d = self.find_x_y(l_3[0])
                d = self.matrix_spin_change[y_d][x_d]

                if frustration == 0:

                    print(np.array(q))
                    if a * l_1[1] * b != 1:
                        self.spin(x_b, y_b, self.matrix_spin_change)
                        b = b * -1
                        print("change_b")

                    if b * l_2[2] * c != 1:
                        self.spin(x_c, y_c, self.matrix_spin_change)
                        c = c * -1
                        print("change_c")

                    if c * l_3[1] * d != 1:
                        self.spin(x_d, y_d, self.matrix_spin_change)
                        d = d * -1
                        print("change_d")

                else:
                    if ch_y == 0:

                        if a * l_1[1] * b != 1:
                            self.spin(x_b, y_b, self.matrix_spin_change)
                            b = b * -1
                        if b * l_2[2] * c != 1:
                            self.spin(x_c, y_c, self.matrix_spin_change)
                            c = c * -1

                    else:
                        if ch_x <= self.size - 2:
                            marker = quartet_frustration_array[ch_y - 1][ch_x]
                            if a * l_1[1] * b != 1 and marker != 1:
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1

                            if b * l_2[2] * c != 1:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1
                        else:
                            marker_u = quartet_frustration_array[ch_y - 1][ch_x]
                            marker_r = quartet_frustration_array[ch_y - 1][ch_x + 1]
                            if (a * l_1[1] * b != 1 and marker_u == 1) or (a * l_1[1] * b != 1 and marker_r == 1):
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1

                            if b * l_2[2] * c != 1:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1

                ch_x += 1
            print()
            ch_y += 1
            ch_x = 0

        self.count_energy_all()
        self.count_frustration_change()

    def algorithm_5_test(self):
        count = 0
        quartet_frustration_array = []
        dop = []
        ch_x, ch_y = 0, 0

        for i in self.quartet:
            for j in i:
                dop.append(self.check_quartet(j))
                print(self.check_quartet(j))
            quartet_frustration_array.append(dop)
            print()
            dop = []

        for line in self.quartet:
            for q in line:
                frustration = self.check_quartet(q)

                l_1 = q[0]
                l_2 = q[1]
                l_3 = q[2]
                a, b, c, d = 0, 0, 0, 0

                x_a, y_a = self.find_x_y(l_1[0])
                a = self.matrix_spin_change[y_a][x_a]

                x_b, y_b = self.find_x_y(l_1[2])
                b = self.matrix_spin_change[y_b][x_b]

                x_c, y_c = self.find_x_y(l_3[2])
                c = self.matrix_spin_change[y_c][x_c]

                x_d, y_d = self.find_x_y(l_3[0])
                d = self.matrix_spin_change[y_d][x_d]

                if frustration == 0:

                    print(np.array(q))
                    if a * l_1[1] * b != 1:
                        self.spin(x_b, y_b, self.matrix_spin_change)
                        b = b * -1
                        print("change_b")

                    if b * l_2[2] * c != 1:
                        self.spin(x_c, y_c, self.matrix_spin_change)
                        c = c * -1
                        print("change_c")

                    if c * l_3[1] * d != 1:
                        self.spin(x_d, y_d, self.matrix_spin_change)
                        d = d * -1
                        print("change_d")

                # else:
                #     if ch_y == 0:
                #
                #         if a * l_1[1] * b != 1:
                #             self.spin(x_b, y_b, self.matrix_spin_change)
                #             b = b * -1
                #         if b * l_2[2] * c != 1:
                #             self.spin(x_c, y_c, self.matrix_spin_change)
                #             c = c * -1
                #
                #     else:
                #         if ch_x <= self.size - 2:
                #             marker = quartet_frustration_array[ch_y - 1][ch_x]
                #             if a * l_1[1] * b != 1 and marker != 1:
                #                 self.spin(x_b, y_b, self.matrix_spin_change)
                #                 b = b * -1
                #
                #             if b * l_2[2] * c != 1:
                #                 self.spin(x_c, y_c, self.matrix_spin_change)
                #                 c = c * -1
                #         else:
                #             marker_u = quartet_frustration_array[ch_y - 1][ch_x]
                #             marker_r = quartet_frustration_array[ch_y - 1][ch_x + 1]
                #             if (a * l_1[1] * b != 1 and marker_u == 1) or (a * l_1[1] * b != 1 and marker_r == 1):
                #                 self.spin(x_b, y_b, self.matrix_spin_change)
                #                 b = b * -1
                #
                #             if b * l_2[2] * c != 1:
                #                 self.spin(x_c, y_c, self.matrix_spin_change)
                #                 c = c * -1

            #     ch_x += 1
            # print()
            # ch_y += 1
            # ch_x = 0

        ch_x, ch_y = 0, 0
        for line in self.quartet:
            for q in line:

                frustration = self.check_quartet(q)

                l_1 = q[0]
                l_2 = q[1]
                l_3 = q[2]
                a, b, c, d = 0, 0, 0, 0

                x_a, y_a = self.find_x_y(l_1[0])
                a = self.matrix_spin_change[y_a][x_a]

                x_b, y_b = self.find_x_y(l_1[2])
                b = self.matrix_spin_change[y_b][x_b]

                x_c, y_c = self.find_x_y(l_3[2])
                c = self.matrix_spin_change[y_c][x_c]

                x_d, y_d = self.find_x_y(l_3[0])
                d = self.matrix_spin_change[y_d][x_d]

                if frustration == 1:
                    if ch_y == 0:

                        if ch_x != self.size - 2:
                            marker_r = quartet_frustration_array[ch_y][ch_x + 1]
                            marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            if a * l_1[1] * b != 1 and marker_r == 1:
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1
                            if b * l_2[2] * c != 1 and marker_r * marker_d * marker_dr == 1:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1
                        else:
                            marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            # marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            if a * l_1[1] * b != 1:
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1
                            if b * l_2[2] * c != 1 and marker_d == 1:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1

                    elif ch_y == self.size - 2:

                        if ch_x != self.size - 2:
                            marker_r = quartet_frustration_array[ch_y][ch_x + 1]
                            # marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            # marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            marker_ur = quartet_frustration_array[ch_y - 1][ch_x + 1]
                            marker_u = quartet_frustration_array[ch_y - 1][ch_x]
                            if a * l_1[1] * b != 1 and marker_r * marker_ur * marker_u == 1:
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1
                            if b * l_2[2] * c != 1 and marker_r == 1:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1
                        else:
                            # marker_r = quartet_frustration_array[ch_y][ch_x + 1]
                            # marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            # marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            # marker_ur = quartet_frustration_array[ch_y - 1][ch_x + 1]
                            marker_u = quartet_frustration_array[ch_y - 1][ch_x]
                            # marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            # marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            if a * l_1[1] * b != 1 and marker_u == 1:
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1
                            if b * l_2[2] * c != 1:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1

                    else:

                        if ch_x != self.size - 2:
                            marker_r = quartet_frustration_array[ch_y][ch_x + 1]
                            marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            marker_ur = quartet_frustration_array[ch_y - 1][ch_x + 1]
                            marker_u = quartet_frustration_array[ch_y - 1][ch_x]
                            if a * l_1[1] * b != 1 and marker_r * marker_ur * marker_u == 1:
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1
                            if b * l_2[2] * c != 1 and marker_r * marker_d * marker_dr == 1:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1
                        else:
                            # marker_r = quartet_frustration_array[ch_y][ch_x + 1]
                            # marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            # marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            # marker_ur = quartet_frustration_array[ch_y - 1][ch_x + 1]
                            marker_u = quartet_frustration_array[ch_y - 1][ch_x]
                            marker_d = quartet_frustration_array[ch_y + 1][ch_x]
                            # marker_dr = quartet_frustration_array[ch_y + 1][ch_x + 1]
                            if a * l_1[1] * b != 1 and marker_u == 1:
                                self.spin(x_b, y_b, self.matrix_spin_change)
                                b = b * -1
                            if b * l_2[2] * c != 1 and marker_d:
                                self.spin(x_c, y_c, self.matrix_spin_change)
                                c = c * -1
                ch_x += 1
            ch_x = 0
            ch_y += 1

        self.count_energy_all()
        self.count_frustration_change()

    def check_quartet(self, q):
        a, b, c, d = q[0][1], q[1][0], q[1][2], q[2][1]
        if (a * b * c * d) == 1:
            return 0
        else:
            return 1

    def all_combinations(self, n):
        # Создаем список всех возможных значений для матрицы
        possible_values = [-1, 1]

        # Генерируем все возможные комбинации для n*n элементов
        all_combinations = product(possible_values, repeat=n * n)

        # Формируем матрицы из комбинаций и возвращаем их
        matrices = []
        for combination in all_combinations:
            matrix = np.array(combination).reshape(n, n)
            matrices.append(matrix)

        return matrices

    def test_matrix_con(self, matrix):
        a = 0
        for i in range(self.size_matrix):
            for j in range(self.size_matrix):
                if i % 2 == 0:
                    if j % 2 == 0:
                        matrix[i][j] = a
                        a += 1
                else:
                    if j % 2 != 0:
                        matrix[i][j] = -5
        return matrix

    def find_spins(self):
        matrix = self.all_combinations(self.size)
        print(self.size_matrix)
        connections = self.all_combinations(self.size_matrix)

        error_list = []
        print("start")
        for con in connections:
            self.matrix_connection = self.test_matrix_con(con)
            frustrate = self.algorithm_4()
            # print(f"frust - {frustrate}")
            marker = 0
            # print(self.matrix_connection)
            for i in matrix:
                self.matrix_spin_change = i
                self.matrix_spin = i
                self.count_energy_all()
                if frustrate == 0 and self.energy_all_change == -12:
                    # print(i)
                    marker = 1
                    break
                elif frustrate < 3 and self.energy_all_change == -10:
                    # print(i)
                    marker = 1
                    break
                elif frustrate > 2 and self.energy_all_change == -8:
                    # print(i)
                    marker = 1
                    break
            if marker == 0:
                print("ERROR", frustrate)
                error_list.append([frustrate, self.matrix_connection])
        a1, a2, a3, a4, a0 = 0, 0, 0, 0, 0
        for i in error_list:
            print(i[0])
            print(i[1])
            print()
            print()
            if i[0] == 1:
                a1 += 1
            elif i[0] == 2:
                a2 += 1
            elif i[0] == 3:
                a3 += 1
            elif i[0] == 4:
                a4 += 1
            elif i[0] == 0:
                a0 += 1
        print(f"1 - {a1}, 2 - {a2}, 3 - {a3}, 4 - {a4}, 0 - {a0}")

    def start(self):
        self.create_spin_matrix()
        self.create_connection_matrix()
        self.create_spin_id()
        self.create_quartet()

        self.count_frustration()

        self.algorithm_1()

        self.count_frustration_change()
        self.count_energy_all()

    def start_algorithm5t(self):
        self.matrix_spin = np.random.choice([1], (self.size, self.size))
        self.matrix_spin_change = self.matrix_spin.copy()
        self.create_connection_matrix()
        self.create_spin_id()
        self.create_quartet()

        self.count_frustration()

        self.algorithm_5_test()

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
            self.clear()

            self.size = size
            self.size_matrix = size_matrix

            self.matrix_connection = file_manager.create_connection_matrix(connection_matrix_extra[matrix])

            self.create_spin_matrix()
            self.create_spin_id()
            self.create_quartet()

            self.count_frustration()

            self.algorithm_1()

            self.algorith_2()
            self.algorith_2()

            self.count_frustration_change()
            self.count_energy_all()
            #######################
            with open(f"files/{matrix}/{file_manager.res_files[matrix]}", 'r') as f:
                for i in range(4):
                    f.readline()
                energy_original = f.readline()
            print(sum(self.matrix_spin_change[0]))
            spin_excess = str(sum(list(map(int, (sum(i) for i in self.matrix_spin_change)))))
            message = \
                f"{file_manager.con_files[matrix]} \t spin excess - {spin_excess} \t|\t " \
                f"energy_final - {self.energy_all_change} \t energy_original - {energy_original.split()[1]}\t|\t" \
                f"percentage - {round(self.energy_all_change / int(energy_original.split()[1])* 100, 2)}%\n"
            letter.append(message)

            with open("results.txt", "w+") as file:
                file.writelines(letter)
                file.close()

    def check_files_5t(self, file_manager, size, size_matrix, connection_matrix_extra):
        self.size = size
        self.size_matrix = size_matrix

        letter = []
        for matrix in connection_matrix_extra:
            self.clear()

            self.size = size
            self.size_matrix = size_matrix

            self.matrix_connection = file_manager.create_connection_matrix(connection_matrix_extra[matrix])

            self.matrix_spin = np.random.choice([1], (self.size, self.size))
            self.matrix_spin_change = self.matrix_spin.copy()

            # self.create_spin_matrix()

            self.create_spin_id()
            self.create_quartet()

            self.count_frustration()

            self.algorithm_5_test()

            self.count_frustration_change()
            self.count_energy_all()
            #######################
            with open(f"files/{matrix}/{file_manager.res_files[matrix]}", 'r') as f:
                for i in range(4):
                    f.readline()
                energy_original = f.readline()
            print(sum(self.matrix_spin_change[0]))
            spin_excess = str(sum(list(map(int, (sum(i) for i in self.matrix_spin_change)))))
            message = \
                f"{file_manager.con_files[matrix]} \t spin excess - {spin_excess} \t|\t " \
                f"energy_final - {self.energy_all_change} \t energy_original - {energy_original.split()[1]}\t|\t" \
                f"percentage - {round(self.energy_all_change / int(energy_original.split()[1])* 100, 2)}%\n"
            letter.append(message)

            with open("results_2.0.txt", "w+") as file:
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

        text5 = f1.render(f'максимальная энергия {-2 *(self.size * self.size - self.size)}', True, (50, 50, 50))

        self.screen.blit(text1, (x, y + 30))
        self.screen.blit(text2, (x + 300, y + 30))
        self.screen.blit(text3, (x + 600, y + 30))
        self.screen.blit(text4, (x + 1100, y + 30))
        self.screen.blit(text5, (x + 1300, y + 30 + 30))

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

                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if event.button == 5:
                #         self.model.algorithm_4()
                #         self.restart(*self.model.return_parameters())

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 5:
                        model.algorithm_5()
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




# f = File_manager()
# f.find_dirs()
# f.create_connection_directories()
# f.find_size()
# print(f.size, f.size_matrix)
# f.create_connection_matrix_extra()
# for i in f.connection_matrix_extra:
#     f.create_connection_matrix(f.connection_matrix_extra[i])
#     break


# size = 5
# file_mananger = File_manager()
# file_mananger.size = 3
#
# model = Model(size)
# model.start_algorithm5()
# model.find_spins()

#
#


model = Model(20)
model.start()
model.algorithm_5_test()

interface = Interface(*model.return_parameters())
interface.connect(model)
interface.start()
