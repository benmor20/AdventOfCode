from typing import *
from year2019.day2019 import Day2019


class Day(Day2019):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = []
        return data

    def puzzles(self):
        pass
