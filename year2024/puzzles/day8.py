import itertools

from year2024.day2024 import Day2024
from typing import *


class Day(Day2024):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = {}
        all_points = set()
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c not in data:
                    data[c] = set()
                data[c].add(i + j * 1j)
                all_points.add(i + j * 1j)
        return data, all_points

    def puzzle1(self):
        data, all_points = self.get_data()
        antinodes = set()
        for freq, sats in data.items():
            if freq == '.':
                continue
            for p1, p2 in itertools.permutations(sats, r=2):
                if (antinode := 2 * p2 - p1) in all_points:
                    antinodes.add(antinode)
        print(len(antinodes))

    def puzzle2(self):
        data, all_points = self.get_data()
        antinodes = set()
        for freq, sats in data.items():
            if freq == '.':
                continue
            for p1, p2 in itertools.permutations(sats, r=2):
                step = p2 - p1
                antinode = p1
                while antinode in all_points:
                    antinodes.add(antinode)
                    antinode += step
        print(len(antinodes))


def one_line():
    pass
