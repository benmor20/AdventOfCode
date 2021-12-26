from year2020.day2020 import Day2020_3


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example: bool = False):
        return set(int(i) for i in super().get_data(example))

    def puzzle(self, num=1):
        data = self.get_data()
        if num == 1:
            for d in data:
                if 2020 - d in data:
                    print(d, d * (2020 - d))
                    return
        elif num == 2:
            for d1 in data:
                for d2 in data:
                    if 2020 - d1 - d2 in data:
                        print(d1, d2, d1 * d2 * (2020 - d1 - d2))
                        return
