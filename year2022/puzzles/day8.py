import itertools

import numpy as np

from year2022.day2022 import Day2022


def in_range(arr, pos):
    return np.all(pos >= 0) and np.all(pos < np.array(arr.shape))


class Day(Day2022):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = np.array([[int(i) for i in l] for l in lines])
        return data

    def puzzle1(self):
        data = self.get_data()
        seen_trees = set()
        for i in range(data.shape[0]):
            highest = -1
            for j in range(data.shape[1]):
                val = data[i, j]
                if val > highest:
                    seen_trees.add((i, j))
                    highest = val
            highest = -1
            for j in list(range(data.shape[1]))[::-1]:
                val = data[i, j]
                if val > highest:
                    seen_trees.add((i, j))
                    highest = val
        for j in range(data.shape[1]):
            highest = -1
            for i in range(data.shape[0]):
                val = data[i, j]
                if val > highest:
                    seen_trees.add((i, j))
                    highest = val
            highest = -1
            for i in list(range(data.shape[0]))[::-1]:
                val = data[i, j]
                if val > highest:
                    seen_trees.add((i, j))
                    highest = val
        print(len(seen_trees))

    def puzzle2(self):
        data = self.get_data()
        best_score = -1
        for i in range(1, data.shape[0] - 1):
            for j in range(1, data.shape[1] - 1):
                score = 1
                for step in [np.array([0, 1]), np.array([0, -1]), np.array([1, 0]), np.array([-1, 0])]:
                    pos = np.array([i, j]) + step
                    cnt = 0
                    while in_range(data, pos) and data[pos[0], pos[1]] < data[i, j]:
                        cnt += 1
                        pos += step
                    if in_range(data, pos):
                        cnt += 1
                    score *= cnt
                    # print(f'From {i, j}, in dir {step.tolist()}, can see {cnt} trees')
                # print(f'Score of {i, j} is {score}\n')
                if score > best_score:
                    best_score = score
        print(best_score)
