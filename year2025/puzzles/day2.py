import itertools
from typing import Generator

from dataclasses import dataclass

from networkx.algorithms.minors.contraction import quotient_graph

from utils.utils import get_range_overlap
from year2025.day2025 import Day2025


@dataclass
class Divisor:
    divisor: int
    quotient_range: range

    @property
    def effective_range(self) -> range:
        return range(self.quotient_range.start * self.divisor, (self.quotient_range.stop - 1) * self.divisor + 1)

    def works(self, amount: int) -> bool:
        div, mod = divmod(amount, self.divisor)
        return mod == 0 and div in self.quotient_range

    def is_in_range(self, amount: int) -> bool:
        div = amount // self.divisor
        return div in self.quotient_range

    def invalid_ids(self, id_range: range) -> Generator[int, None, None]:
        overlap = get_range_overlap(id_range, self.effective_range)
        if overlap is None:
            return
        start_div, start_mod = divmod(overlap.start, self.divisor)
        end_div, end_mod = divmod(overlap.stop, self.divisor)
        if start_mod == 0:
            yield overlap.start
        for quotient in range(start_div + 1, end_div + (0 if end_mod == 0 else 1)):
            yield quotient * self.divisor



def generate_divisors(pt1: bool) -> Generator[Divisor, None, None]:
    # 11: 1-9
    # 101: 10-99
    # 111: 1-9
    # 1001, 1111
    # 10001, 10101, 11111
    # 100001, 111111
    # 1000001, 1001001, 1010101, 1111111
    for digits in itertools.count(2):
        for nzeros in range(digits - 2, (digits - 3) if pt1 else -1, -1):
            div, mod = divmod(digits - 1, nzeros + 1)
            if mod != 0:
                continue
            section = "1" + "0" * nzeros
            divisor = int(section * div + "1")
            quotient_range = range(10 ** nzeros, 10 ** (nzeros + 1))
            yield Divisor(divisor, quotient_range)



class Day(Day2025):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [range(int((splt := section.split("-"))[0]), int(splt[1]) + 1) for section in lines[0].split(",")]
        return data

    def do_puzzle(self, pt1: bool, example: bool = False):
        data = self.get_data(example)
        invalid_ids = set[int]()
        max_range = len(str(max(r.stop for r in data)))
        print(f"{max_range=}")
        for divisor in generate_divisors(pt1):
            for id_range in data:
                new_ids = set(divisor.invalid_ids(id_range))
                # print(f"{new_ids=}, {divisor.divisor=}, {id_range=}")
                invalid_ids.update(new_ids)
            if len(str(divisor.divisor)) > max_range:
                break
        print(sum(invalid_ids))

    def puzzle1(self):
        self.do_puzzle(True)

    def puzzle2(self):
        self.do_puzzle(False)


def one_line():
    pass
