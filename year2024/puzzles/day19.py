from year2024.day2024 import Day2024


MEMO = {}


def num_possibilities(towels, design):
    if len(design) == 0:
        return 1
    if design in MEMO:
        return MEMO[design]
    total = 0
    for towel in towels:
        if design.startswith(towel):
            total += num_possibilities(towels, design[len(towel):])
    MEMO[design] = total
    return total


class Day(Day2024):
    @property
    def num(self) -> int:
        return 19

    def get_data(self, example=False):
        text = super().get_raw_data(example)
        towel_str, design_str = text.split('\n\n')
        towels = set(towel_str.strip().split(', '))
        designs = design_str.splitlines()
        return towels, designs

    def puzzle1(self):
        towels, designs = self.get_data()
        num_poss = sum(num_possibilities(towels, des) > 0 for des in designs)
        print(num_poss)

    def puzzle2(self):
        towels, designs = self.get_data()
        num_poss = sum(num_possibilities(towels, des) for des in designs)
        print(num_poss)


def one_line():
    pass
