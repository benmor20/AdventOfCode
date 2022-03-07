from year2019.day2019 import Day2019


def calculate_fuel(mass):
    return mass // 3 - 2


def calculate_total_fuel(mass):
    total = 0
    prev = mass
    fuel = calculate_fuel(mass)
    while fuel > 0:
        total += fuel
        prev = fuel
        fuel = calculate_fuel(prev)
    return total


class Day(Day2019):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [int(i) for i in lines]
        return data

    def puzzles(self):
        masses = self.get_data()
        total = sum(map(calculate_fuel, masses))
        print(f'Total is {total}')

        full_total = sum(map(calculate_total_fuel, masses))
        print(f'Total with fuel is {full_total}')
