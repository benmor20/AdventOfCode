import itertools

from year2024.day2024 import Day2024
import numpy as np


class Day(Day2024):
    @property
    def num(self) -> int:
        return 25

    def get_data(self, example=False):
        lines = super().get_raw_data(example)
        lock_keys = lines.split('\n\n')
        locks = []
        keys = []
        for string in lock_keys:
            lines = string.splitlines()
            # There will always be one set of hashtags that arent counted
            # Either at the top or bottom
            lock_key = np.ones((len(lines[0]),)) * -1
            for line in lines:
                for idx, c in enumerate(line):
                    if c == '#':
                        lock_key[idx] += 1
            if all(c == '#' for c in lines[0]):
                locks.append(lock_key)
            else:
                keys.append(lock_key)
        return locks, keys

    def puzzle1(self):
        locks, keys = self.get_data()
        total = 0
        for lock, key in itertools.product(locks, keys):
            if np.all((lock + key) <= 5):
                total += 1
        print(total)

    def puzzle2(self):
        # Hit the button!
        pass


def one_line():
    pass
