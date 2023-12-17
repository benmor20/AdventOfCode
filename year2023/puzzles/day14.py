from year2023.day2023 import Day2023
from typing import *
import numpy as np


SYM_TO_NUM = {'.': 0, '#': 1, 'O': 2}
NUM_TO_SYM = ['.', '#', 'O']


def stones_to_str(stones: np.ndarray) -> str:
    return '\n'.join(''.join(NUM_TO_SYM[int(i)] for i in row) for row in stones)


def step(stones: np.ndarray, rev: bool = False) -> np.ndarray:
    top = stones[:-1, :]
    bot = stones[1:]
    if rev:
        new_round = (top == 2) & (bot == 0)
        top[new_round] = 0
        bot[new_round] = 2
        res = np.zeros(stones.shape)
        res[1:, :] = bot
        res[0, :] = top[0, :]
    else:
        new_round = (top == 0) & (bot == 2)
        top[new_round] = 2
        bot[new_round] = 0
        res = np.zeros(stones.shape)
        res[:-1, :] = top
        res[-1, :] = bot[-1, :]
    return res


def step_no_copy(stones: np.ndarray, rev: bool = False) -> np.ndarray:
    top = stones[:-1, :]
    bot = stones[1:]
    res = np.zeros(stones.shape)
    res[stones == 1] = 1
    if rev:
        new_round = (top == 2) & (bot == 0)
        res[1:, :][(bot == 2) | new_round] = 2
        res[:-1, :][new_round] = 0
        res[0, :][(stones[0, :] == 2) & ~new_round[0, :]] = 2
    else:
        new_round = (top == 0) & (bot == 2)
        res[:-1, :][(top == 2) | new_round] = 2
        res[1:, :][new_round] = 0
        res[-1, :][(stones[-1, :] == 2) & ~new_round[-1, :]] = 2
    return res


def run_till_done(stones: np.ndarray, rev: bool = False) -> np.ndarray:
    while True:
        new_stones = step_no_copy(stones, rev)
        if np.all(new_stones == stones):
            return new_stones
        stones = new_stones


def cycle(stones: np.ndarray) -> np.ndarray:
    stones = run_till_done(stones)
    stones = run_till_done(stones.T).T
    stones = run_till_done(stones, True)
    stones = run_till_done(stones.T, True).T
    return stones


def count_load(stones: np.ndarray) -> int:
    return sum(i * np.sum(stones[-i, :] == 2) for i in range(1, stones.shape[0] + 1))


class Day(Day2023):
    @property
    def num(self) -> int:
        return 14

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = np.array([[SYM_TO_NUM[c] for c in row] for row in lines])
        return data

    def puzzle1(self):
        data = self.get_data()
        while True:
            # print(stones_to_str(data))
            # print()
            # new_data = step(data.copy())
            new_data = step_no_copy(data)
            if np.all(new_data == data):
                break
            data = new_data
        # print(stones_to_str(data))
        print(count_load(data))

    def puzzle2(self):
        stones = self.get_data()
        seen = {}
        for i in range(1000000000):
            new_stones = cycle(stones)
            # print(stones_to_str(new_stones))
            # print()
            set_ele = tuple(new_stones.reshape((-1,)))
            if set_ele in seen:
                # print(seen)
                seen[set_ele].append(i)
                break
            seen[set_ele] = seen.get(set_ele, []) + [i]
            stones = new_stones
        first_in_cycle = next(v for v in seen.values() if len(v) > 1)
        len_cycle = first_in_cycle[1] - first_in_cycle[0]
        target_idx = (1000000000 - 1) % len_cycle
        while target_idx < first_in_cycle[0]:
            target_idx += len_cycle
        for stone_tup, idxs in seen.items():
            if target_idx in idxs:
                final_stones = np.array(stone_tup).reshape(stones.shape)
                print(count_load(final_stones))
                break


def one_line():
    pass
