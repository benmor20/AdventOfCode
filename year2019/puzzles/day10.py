from typing import *
import math
from year2019.day2019 import Day2019

from utils import utils


def blockteroids(testeroid, baseteroid):
    diff = utils.tuple_diff(testeroid, baseteroid)
    gcd = math.gcd(*diff)
    if gcd == 1:
        return
    step = diff[0] // gcd, diff[1] // gcd
    resteroid = utils.add_tuples(baseteroid, step)
    while resteroid != testeroid:
        yield resteroid
        resteroid = utils.add_tuples(resteroid, step)


def all_slopes(start, size):
    for x in range(size[0]):
        for y in range(size[1]):
            diff = utils.tuple_diff((x, y), start)
            if math.gcd(*diff) == 1:
                yield diff


def atan_in_range(x, y):
    angle = math.atan2(x, -y) * 180 / math.pi
    return angle + (0 if angle >= 0 else 360)


def sorted_slopes(start, size):
    yield from sorted(all_slopes(start, size), key=lambda s: atan_in_range(*s))


def first_asteroid_on_slope(start, slope, asteroids, size=None):
    if size is None:
        maxx = max(a[0] for a in asteroids)
        maxy = max(a[1] for a in asteroids)
        size = maxx + 1, maxy + 1
    curr = utils.add_tuples(start, slope)
    while utils.in_range(curr, size):
        if curr in asteroids:
            return curr
        curr = utils.add_tuples(curr, slope)
    return None


class Day(Day2019):
    @property
    def num(self) -> int:
        return 10

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    data.add((x, y))
        return data

    def puzzles(self):
        asteroids = self.get_data()

        # Puzzle 1
        besteroid = None
        most_seen = -1
        for baseteroid in asteroids:
            num_seen = 0
            for testeroid in asteroids:
                if testeroid == baseteroid:
                    continue
                if any(a in asteroids for a in blockteroids(testeroid, baseteroid)):
                    continue
                num_seen += 1
            if num_seen > most_seen:
                besteroid = baseteroid
                most_seen = num_seen
        print(f'Best base is {besteroid} with {most_seen} asteroids seen')

        # Puzzle 2
        maxx = max(a[0] for a in asteroids)
        maxy = max(a[1] for a in asteroids)
        size = maxx + 1, maxy + 1
        count = 0
        while (len(asteroids)) > 1:
            for slope in sorted_slopes(besteroid, size):
                dusteroid = first_asteroid_on_slope(besteroid, slope, asteroids, size)
                if dusteroid is not None:
                    asteroids.remove(dusteroid)
                    count += 1
                    # print(f'Vaporizing {dusteroid} (number {count})')
                    if count == 200:
                        print(100 * dusteroid[0] + dusteroid[1])
