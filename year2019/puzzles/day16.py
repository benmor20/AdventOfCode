import itertools
from typing import *
from year2019.day2019 import Day2019
import numpy as np


mem = {}
def wave(n, rep):
    if (n, rep) in mem:
        return mem[(n, rep)]
    single_wave = np.repeat(np.array((0, 1, 0, -1)), rep)
    res = np.concatenate([single_wave] * (n // len(single_wave) + 1))
    res = res[1:n+1]
    mem[(n, rep)] = res
    return res


def step(inp):
    res = []
    length = len(inp)
    for n in range(length):
        # print(f'{inp.shape = }')
        w = wave(length, n+1)
        # print(f'{w.shape = }')
        res.append(abs(w.dot(inp)) % 10)
    return np.array(res)


class Day(Day2019):
    @property
    def num(self) -> int:
        return 16

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = [int(i) for i in lines[0]]
        return np.array(data).astype(np.uint8)

    def puzzles(self):
        data = self.get_data()
        nxt = data
        for _ in range(100):
            nxt = step(nxt)
        print(''.join(str(i) for i in nxt[:8]))

        start = int(''.join(str(i) for i in data[:7]))
        rep_data = np.concatenate([data] * 10000)
        nxt = rep_data
        for _ in range(100):
            nxt = step(nxt)
        print(''.join(str(i) for i in nxt[start:start+8]))
