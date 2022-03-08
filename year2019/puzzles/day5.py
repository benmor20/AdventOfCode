from typing import *
from year2019.intcode import Intcode
from year2019.day2019 import Day2019


class Day(Day2019):
    @property
    def num(self) -> int:
        return 5

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        return [int(i) for i in lines[0].split(',')]

    def puzzles(self):
        code = self.get_data()
        intcode = Intcode(code, [5])
        res_code, outputs = intcode.run()
        print(f'Outputs are {outputs}')
