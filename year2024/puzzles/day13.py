import itertools

from year2024.day2024 import Day2024
import re
import numpy as np


def min_tokens(avec, bvec, prize_loc):
    coefs = np.zeros((2, 2))
    coefs[:, 0] = avec
    coefs[:, 1] = bvec
    ans = np.linalg.solve(coefs, prize_loc)
    ans_int = ans.round().astype(int)
    if np.all(coefs @ ans_int == prize_loc):
        return 3 * ans_int[0] + ans_int[1]
    return 0


class Day(Day2024):
    @property
    def num(self) -> int:
        return 13

    def get_data(self, example=False):
        text = super().get_raw_data(example)
        machine_lines = text.split('\n\n')
        data = []
        for machine in machine_lines:
            match = re.match(r'Button A: X\+([\d]+), Y\+([\d]+)\nButton B: X\+([\d]+), Y\+([\d]+)\nPrize: X=([\d]+), Y=([\d]+)', machine)
            data.append(tuple(int(match[i]) for i in range(1, 7)))
        return data

    def puzzle1(self):
        data = self.get_data()
        tokens = 0
        tokens_old = 0
        for machine in data:
            avec = np.array(machine[:2])
            bvec = np.array(machine[2:4])
            prize = np.array(machine[4:])
            tokens += min_tokens(avec, bvec, prize)
        print(tokens)

    def puzzle2(self):
        data = self.get_data()
        tokens = 0
        for machine in data:
            avec = np.array(machine[:2])
            bvec = np.array(machine[2:4])
            prize = np.array(machine[4:]) + np.array((1,)) * 10000000000000
            tokens += min_tokens(avec, bvec, prize)
        print(tokens)


def one_line():
    pass
