from year2023.day2023 import Day2023
from typing import *
import numpy as np


INDEXES = {'red': 0, 'green': 1, 'blue': 2}


class Day(Day2023):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            line = line.split(': ')[1]
            pull_lst = []
            for pull in line.split('; '):
                splt = pull.split(', ')
                cube_lst = np.zeros((3, ))
                for cubes in splt:
                    parts = cubes.split(' ')
                    cube_lst[INDEXES[parts[1]]] = int(parts[0])
                pull_lst.append(cube_lst)
            data.append(pull_lst)
        return data

    def puzzle1(self):
        data = self.get_data()
        games = [np.stack(game) for game in data]
        min_cubes = [np.max(game, axis=0) for game in games]
        max_cubes = np.array([12, 13, 14])
        total = sum(idx + 1 for idx, cubes in enumerate(min_cubes) if np.all(cubes <= max_cubes))
        print(total)

    def puzzle2(self):
        data = self.get_data()
        games = [np.stack(game) for game in data]
        min_cubes = [np.max(game, axis=0) for game in games]
        total = sum(int(np.product(cube)) for cube in min_cubes)
        print(total)


def one_line():
    pass
