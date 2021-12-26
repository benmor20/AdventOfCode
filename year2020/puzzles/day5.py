from year2020.day2020 import Day2020_3


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 5

    def puzzle(self, num=1):
        codes = set()
        for seat in self.get_data():
            code = 0
            for i, letter in enumerate(seat):
                if letter == '\n':
                    continue
                code *= 2
                code += 1 if letter in ('B', 'R') else 0
            codes.add(code)
        if num == 1:
            print(max(codes))
        else:
            for i in range(2 ** 10):
                if i not in codes and i - 1 in codes and i + 1 in codes:
                    print(i)
