import itertools

from year2024.day2024 import Day2024
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def step(pos, vel, size):
    new_pos = pos + vel
    if new_pos[0] < 0:
        new_pos[0] += size[0]
    elif new_pos[0] >= size[0]:
        new_pos[0] -= size[0]
    if new_pos[1] < 0:
        new_pos[1] += size[1]
    elif new_pos[1] >= size[1]:
        new_pos[1] -= size[1]
    return new_pos


def safety_factor(poses, size):
    robots = np.zeros(size)
    for pos in poses:
        robots[tuple(pos)] += 1
    assert np.sum(robots) == len(poses)
    half = size // 2
    q1 = np.sum(robots[:half[0], :half[1]])
    q2 = np.sum(robots[:half[0], -half[1]:])
    q3 = np.sum(robots[-half[0]:, :half[1]])
    q4 = np.sum(robots[-half[0]:, -half[1]:])
    return q1 * q2 * q3 * q4


def print_grid(poses, size, i):
    robots = np.zeros(size)
    for pos in poses:
        robots[tuple(pos)] += 1
    plt.imshow(robots)
    plt.title(f'After {i} seconds')
    plt.show()


def dimension(poses, size, idx):
    robots = np.zeros(size)
    for pos in poses:
        robots[tuple(pos)] += 1
    xs = []
    num_bots = []
    for i in range(10, min(size[0], size[1])):
        xs.append(i)
        num_bots.append(np.sum(robots[:i, :i]))
    xs = np.array(xs)
    ys = np.array(num_bots)
    params = linregress(np.log(xs), np.log(ys))
    print(f'After {idx} seconds, dim of {params[0]}')
    assert abs(params[0] - 2) < 0.4


class Day(Day2024):
    @property
    def num(self) -> int:
        return 14

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            match = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
            pos = np.array([int(match[2]), int(match[1])])
            vel = np.array([int(match[4]), int(match[3])])
            data.append((pos, vel))
        return data

    def puzzle1(self):
        example = False
        size = np.array([7, 11] if example else [103, 101])
        data = self.get_data(example)
        for _ in range(100):
            new_data = []
            for pos, vel in data:
                new_data.append((step(pos, vel, size), vel))
            data = new_data
        print(safety_factor([pos for pos, _ in data], size))

    def puzzle2(self):
        example = False
        size = np.array([7, 11] if example else [103, 101])
        data = self.get_data(example)
        for i in range(7520):
            new_data = []
            for pos, vel in data:
                new_data.append((step(pos, vel, size), vel))
            data = new_data
            # robots = np.zeros(size)
            # for pos, _ in data:
            #     robots[tuple(pos)] += 1
            # if np.sum(robots > 0) == len(data):
            #     print_grid([pos for pos, _ in data], size, i)
        try:
            dimension([pos for pos, _ in data], size, 7520)
        except AssertionError:
            print_grid([pos for pos, _ in data], size, 7520)


def one_line():
    pass
