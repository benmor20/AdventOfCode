from year2020.day2020 import Day2020


def update(last_said, turn_said, turn):
    num = turn - turn_said[last_said] - 1 if last_said in turn_said else 0
    turn_said[last_said] = turn - 1
    return num, turn_said


class Day(Day2020):
    @property
    def num(self) -> int:
        return 15

    def get_data(self, example=False):
        return [int(i) for i in super().get_data(example)[0].split(',')]

    def puzzles(self):
        starting = self.get_data(True)

        n = 30000000
        turn_said = {n: i for i, n in enumerate(starting[:-1])}
        last_said = starting[-1]
        for i in range(len(starting), n - 1):
            last_said, turn_said = update(last_said, turn_said, i)
        print(update(last_said, turn_said, n - 1)[0])
