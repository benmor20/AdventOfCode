from year2019.day2019 import Day2019
from year2019.intcode import Intcode


class Day(Day2019):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example=False):
        lines = super().get_data(type(example) is int or example)  # bool is int
        data = lines[0 if isinstance(example, bool) else example].split(',')
        data = [int(i) for i in data]
        return data

    def puzzles(self):
        example = False
        is_ex = not (isinstance(example, bool) and not example)
        code = self.get_data(example)
        if is_ex:
            intcode = Intcode(code)
        else:
            intcode = Intcode(code, noun=12, verb=2)
        print(f'Result is {intcode.run()[0]} (final intcode is {intcode.intcode})')

        if not is_ex:
            target = 19690720
            for i in range(10000):
                noun, verb = divmod(i, 100)
                testcode = Intcode(code, noun=noun, verb=verb)
                res = testcode.run()[0]
                if res == target:
                    print(f'Value to give {target} is {i}')
