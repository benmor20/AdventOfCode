from year2022.day2022 import Day2022
from typing import *


SNAFU_TO_INT = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
INT_TO_SNAFU = ['0', '1', '2', '=', '-']


def snafu_to_dec(snafu: str) -> int:
    res = 0
    for c in snafu:
        res *= 5
        res += SNAFU_TO_INT[c]
    # print(f'{snafu} -> {res}')
    return res


def dec_to_snafu(dec: int) -> str:
    res = ''
    while dec != 0:
        val = dec % 5
        if val > 2:
            val -= 5
        res += INT_TO_SNAFU[val]
        dec -= val
        dec //= 5
    return res[::-1]


class Day(Day2022):
    @property
    def num(self) -> int:
        return 25

    # def get_data(self, example=False):
    #     lines = super().get_data(example)
    #     return [Snafu(line) for line in lines]

    def puzzle1(self):
        data = self.get_data()
        print(dec_to_snafu(sum(snafu_to_dec(s) for s in data)))

    def puzzle2(self):
        data = self.get_data(True)
