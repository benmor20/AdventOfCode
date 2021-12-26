from year2020.day2020 import Day2020_3


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 6

    def get_data(self, example: bool = False):
        lines = super().get_data(example)
        data = []
        group = []
        for line in lines:
            if len(line) == 0:
                data.append(group)
                group = []
                continue
            group.append(set(line))
        data.append(group)
        return data

    def sum(self, sets, num):
        res = sets[0]
        for s in sets[1:]:
            res = res | s if num == 1 else res & s
        return res

    def puzzle(self, num=1):
        print(sum(len(self.sum(group, num)) for group in self.get_data()))
