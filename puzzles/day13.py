from puzzles.daybase import DayBase
import numpy as np


def print_array(array):
    for row in array:
        for v in row:
            print('#' if v == 1 else '.', end='')
        print()
    print()


def fold(array, direction, line):
    if direction == 'x':
        l = array.shape[0]
        top = array[line - (l - line) + 1:line, :]
        bottom = array[line + 1:, :]
        # print_array(top)
        # print_array(bottom)
        # print_array(bottom[::-1, :])
        array[line - (l - line) + 1:line, :] = (top == 1) | (bottom[::-1, :] == 1)
        array = array[:line, :]
        return array
    else:
        l = array.shape[1]
        top = array[:, line - (l - line) + 1:line]
        bottom = array[:, line + 1:]
        # print_array(top)
        # print_array(bottom)
        # print_array(bottom[:, ::-1])
        array[:, line - (l - line) + 1:line] = (top == 1) | (bottom[:, ::-1] == 1)
        array = array[:, :line,]
        return array


class Day(DayBase):
    @property
    def num(self) -> int:
        return 13

    def get_data(self, example=False):
        points = []
        folds = []
        first_section = True
        for line in super().get_data(example):
            if len(line) == 0:
                first_section = False
                continue
            if first_section:
                points.append(tuple([int(i) for i in line.split(',')][::-1]))
            else:
                folds.append(('x' if line[len('fold along ')] == 'y' else 'y', int(line[line.index('=')+1:])))
        return points, folds

    def puzzle1(self):
        points, folds = self.get_data()
        array = np.zeros((max([p[0] for p in points]) + 1, max([p[1] for p in points]) + 1))
        for point in points:
            array[point] = 1
        print(array.shape)
        array = fold(array, folds[0][0], folds[0][1])
        print(np.sum(array))

    def puzzle2(self):
        points, folds = self.get_data()
        array = np.zeros((max([p[0] for p in points]) + 1, max([p[1] for p in points]) + 1))
        for point in points:
            array[point] = 1
        print(array.shape)
        for f in folds:
            array = fold(array, f[0], f[1])
        print_array(array)
