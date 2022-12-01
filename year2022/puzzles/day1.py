from year2022.day2022 import Day2022


class Day(Day2022):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example=False):
        with open(self.filepath(example), 'r') as file:
            full_file = file.read()
        by_elf = full_file.split('\n\n')
        return [[int(i) for i in e.split('\n')] for e in by_elf]

    def puzzle1(self):
        data = self.get_data()
        totals = [sum(e) for e in data]
        print(max(totals))

    def puzzle2(self):
        data = self.get_data()
        totals = [sum(e) for e in data]
        print(sum(sorted(totals)[-3:]))
