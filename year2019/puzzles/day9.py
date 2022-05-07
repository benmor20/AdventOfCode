from typing import *
from year2019.day2019 import Day2019
from year2019.intcode import Intcode


class Day(Day2019):
    @property
    def num(self) -> int:
        return 9

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = [int(i) for i in lines[0].split(',')]
        return data

    def puzzles(self):
        intcode = Intcode(self.get_data(), [2])
        intcode.run()
        print(intcode.outputs)
