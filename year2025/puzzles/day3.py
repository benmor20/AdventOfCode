from year2025.day2025 import Day2025


def best_joltage(bank, num_on):
    if num_on == 1:
        return max(bank)
    valid_choices = bank[:-(num_on - 1)]
    best_tens = max(valid_choices)
    best_tens_idx = next(i for i, val in enumerate(valid_choices) if val == best_tens)
    return int(str(best_tens) + str(best_joltage(bank[best_tens_idx + 1:], num_on - 1)))


class Day(Day2025):
    @property
    def num(self) -> int:
        return 3

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [[int(i) for i in line] for line in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for bank in data:
            best = 0
            for idx1, tens in enumerate(bank):
                for idx2 in range(idx1 + 1, len(bank)):
                    ones = bank[idx2]
                    joltage = 10 * tens + ones
                    best = max(best, joltage)
            total += best
        print(total)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        for bank in data:
            total += best_joltage(bank, 12)
        print(total)


def one_line():
    pass
