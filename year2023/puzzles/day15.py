from year2023.day2023 import Day2023
from typing import *


class Day(Day2023):
    @property
    def num(self) -> int:
        return 15

    def get_data(self, example=False):
        lines = super().get_data(example)
        return lines[0].split(',')

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for part in data:
            val = 0
            for c in part:
                val += ord(c)
                val *= 17
                val = val % 256
            total += val
        print(total)

    def puzzle2(self):
        data = self.get_data()
        hashmap = [{} for _ in range(256)]
        for part in data:
            if '-' in part:
                label = part[:-1]
                num = -1
            elif '=' in part:
                label = part.split('=')[0]
                num = int(part.split('=')[1])
            else:
                assert False
            box = 0
            for c in label:
                box += ord(c)
                box *= 17
                box = box % 256
            if num == -1:
                if label in hashmap[box]:
                    del hashmap[box][label]
            else:
                hashmap[box][label] = num
        total = 0
        for box, dct in enumerate(hashmap):
            for idx, label in enumerate(dct):
                total += (box + 1) * (idx + 1) * dct[label]
        print(total)


def one_line():
    pass
