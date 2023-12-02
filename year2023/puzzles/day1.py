from year2023.day2023 import Day2023
from typing import *


class Day(Day2023):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example=False):
        lines = super().get_data(example)
        return lines

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for line in data:
            first = -1
            last = -1
            for c in line:
                if c in '0123456789':
                    if first == -1:
                        first = int(c)
                    last = int(c)
            num = 10 * first + last
            total += num
        print(total)

    def puzzle2(self):
        data = self.get_data()
        nums = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9
        }
        total = 0
        for line in data:
            first = -1
            first_idx = -1
            last = -1
            last_idx = -1
            for digit in '123456789':
                try:
                    idx = line.index(digit)
                    ridx = line.rindex(digit)
                except ValueError:
                    continue
                if first_idx == -1 or idx < first_idx:
                    first_idx = idx
                    first = int(digit)
                if ridx > last_idx:
                    last_idx = ridx
                    last = int(digit)
            for name, digit in nums.items():
                try:
                    idx = line.index(name)
                    ridx = line.rindex(name)
                except ValueError:
                    continue
                if first_idx == -1 or idx < first_idx:
                    first_idx = idx
                    first = digit
                if ridx > last_idx:
                    last_idx = ridx
                    last = digit
            assert first > -1
            assert last > -1
            num = 10 * first + last
            # print(num)
            total += num
        print(total)


def one_line():
    with open('year2023/data/day1data.txt', 'r') as f: print('\n'.join([num_dict := {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}, str(sum(10 * min(range(1, 10), key=lambda d: line.index(str(d)) if str(d) in line else len(line)) + max(range(1, 10), key=lambda d: line.rindex(str(d)) if str(d) in line else -1) for line in f.read().split('\n'))), str(sum(10 * num_dict[min(num_dict.keys(), key=lambda n: line.index(n) if n in line else len(line))] + num_dict[max(num_dict.keys(), key=lambda n: line.rindex(n) if n in line else -1)] for line in f.read().split('\n')))][1:]))
