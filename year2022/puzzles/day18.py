from year2022.day2022 import Day2022
from typing import *
import numpy as np
from collections import Counter


def faces_from_cube(cube: np.ndarray) -> Set[Tuple[int, int, int]]:
    res = set()
    for i in range(3):
        arr = np.zeros((3,))
        arr[i] = 0.5
        res.add(tuple(cube + arr))
        res.add(tuple(cube - arr))
    return res


def adjacent_cubes(cube: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    return [
        (cube[0] + 1, cube[1], cube[2]),
        (cube[0] - 1, cube[1], cube[2]),
        (cube[0], cube[1] + 1, cube[2]),
        (cube[0], cube[1] - 1, cube[2]),
        (cube[0], cube[1], cube[2] + 1),
        (cube[0], cube[1], cube[2] - 1),
    ]


class Day(Day2022):
    @property
    def num(self) -> int:
        return 18

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            data.append(tuple(int(i) for i in line.split(',')))
        return data

    def puzzle1(self):
        data = self.get_data()
        cnt = Counter()
        for cube in data:
            cnt.update(faces_from_cube(np.array(cube)))
        print(sum(1 for n in cnt.values() if n == 1))

    def puzzle2(self):
        data = self.get_data()
        lava_cubes = set(data)
        water = set()
        to_check = set()
        to_check.add((0, 0, 0))
        while len(to_check) > 0:
            cube = to_check.pop()
            water.add(cube)
            for adj in adjacent_cubes(cube):
                if any(x < -2 or x > 23 for x in adj):
                    continue
                if adj not in lava_cubes and adj not in water:
                    to_check.add(adj)
            # print(to_check)
        cnt = Counter()
        for cube in water:
            cnt.update({f for f in faces_from_cube(np.array(cube)) if all(-2 < x < 23 for x in f)})
        print(sum(1 for n in cnt.values() if n == 1))
