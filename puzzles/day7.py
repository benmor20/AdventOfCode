from puzzles.daybase import DayBase


def tri(n):
    return n * (n + 1) // 2


class Day(DayBase):
    @property
    def num(self) -> int:
        return 7

    def get_data(self, example=False):
        return [int(i) for i in super().get_data(example)[0].split(',')]

    def puzzle1(self):
        poses = self.get_data()
        low, high = min(poses), max(poses)
        best_pos, best_fuel = 0, 1000000
        for test in range(low, high + 1):
            fuel = sum(abs(p - test) for p in poses)
            if fuel < best_fuel:
                best_pos, best_fuel = test, fuel
        print(best_pos, best_fuel)

    def puzzle2(self):
        poses = self.get_data()
        low, high = min(poses), max(poses)
        best_pos, best_fuel = 0, 1000000000
        for test in range(low, high + 1):
            fuel = sum(tri(abs(p - test)) for p in poses)
            if fuel < best_fuel:
                best_pos, best_fuel = test, fuel
        print(best_pos, best_fuel)
