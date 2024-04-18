#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'denisbalyko'

# Взято и портировано: http://habrahabr.ru/post/192102/

import random

from utils import solver


class grid:
    def __init__(self, n=3):
        """ Generation of the base table """
        self.n = n
        self.table = [
            [
                ((i * n + i // n + j) % (n * n) + 1)
                for j in range(n * n)
            ]
            for i in range(n * n)
        ]

    def show(self):
        for row in self.table:
            print(row)

    def transposing(self):
        """ Transposing the whole grid """

        self.table = map(list, zip(*self.table))
        self.table = list(self.table)

    def swap_rows_small(self):
        """ Swap the two rows """
        area = random.randrange(0, self.n, 1)
        line1 = random.randrange(0, self.n, 1)
        # получение случайного района и случайной строки
        N1 = area * self.n + line1
        # номер 1 строки для обмена

        line2 = random.randrange(0, self.n, 1)
        # случайная строка, но не та же самая
        while line1 == line2:
            line2 = random.randrange(0, self.n, 1)

        N2 = area * self.n + line2

        # номер 2 строки для обмена
        self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

    def swap_columns_small(self):
        self.transposing()
        self.swap_rows_small()
        self.transposing()

    def swap_rows_area(self):
        """ Swap the two area horizon """
        area1 = random.randrange(0, self.n, 1)
        # получение случайного района

        area2 = random.randrange(0, self.n, 1)
        # ещё район, но не такой же самый
        while area1 == area2:
            area2 = random.randrange(0, self.n, 1)

        for i in range(0, self.n):
            N1, N2 = area1 * self.n + i, area2 * self.n + i
            self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

    def swap_columns_area(self):
        self.transposing()
        self.swap_rows_area()
        self.transposing()

    def mix(self, amt=10):
        mix_func = ['self.transposing()',
                    'self.swap_rows_small()',
                    'self.swap_columns_small()',
                    'self.swap_rows_area()',
                    'self.swap_columns_area()']
        for i in range(1, amt):
            id_func = random.randrange(0, len(mix_func), 1)
            eval(mix_func[id_func])


def gen():
    """Функция генерации таблицы судоку."""

    example = grid()
    example.mix()

    mask = [
        [0 for _ in range(example.n * example.n)]
        for _ in range(example.n * example.n)
    ]

    difficult = example.n ** 4

    iterator = example.n ** 4 - 30

    while iterator < example.n ** 4:
        i = random.randrange(0, example.n * example.n)
        j = random.randrange(0, example.n * example.n)
        if mask[i][j] == 0:
            iterator += 1
            mask[i][j] = 1

            example.table[i][j] = 0
            difficult -= 1  # Усложняем если убрали элемент

            table_solution = []
            for copy_i in range(0, example.n * example.n):
                table_solution.append(example.table[copy_i][:])  # Скопируем в отдельный список

            i_solution = 0
            for _ in solver.solve_sudoku((example.n, example.n), table_solution):
                i_solution += 1  # Считаем количество решений

            if i_solution != 1:  # Если решение не одинственное вернуть всё обратно
                example.table[i][j] = 1
                difficult += 1  # Облегчаем

    return example.table, (example.n, example.n)
