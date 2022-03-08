from typing import *
from year2019.day2019 import Day2019


def fits_rules(num):
    diff = []
    digits = [int(i) for i in str(num)]
    prev = digits[0]
    for dig in digits[1:]:
        diff.append(dig - prev)
        prev = dig
    return all([d >= 0 for d in diff]) and\
           any([d == 0 and (i == 0 or diff[i - 1] > 0) and (i == len(diff) - 1 or diff[i + 1] > 0) for i, d in enumerate(diff)])


class Day(Day2019):
    @property
    def num(self) -> int:
        return 4

    def get_data(self, example: Union[bool, int] = False):
        return 136760, 595730

    def puzzles(self):
        lo, hi = self.get_data()
        num_fit = 0
        for num in range(lo, hi + 1):
            if fits_rules(num):
                print(num)
                num_fit += 1
        print(f'There are {num_fit} numbers that match')
