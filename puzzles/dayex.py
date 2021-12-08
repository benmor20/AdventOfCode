from puzzles.daybase import DayBase


class Day(DayBase):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example=False):
        return [int(i) for i in super().get_data(example)[0].split(',')]

    def puzzle1(self):
        pass

    def puzzle2(self):
        pass
