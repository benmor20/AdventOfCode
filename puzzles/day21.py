from puzzles.daybase import DayBase
import itertools


rolls_to_coefs = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def move(start, amt):
    res = start + amt
    while res > 10:
        res -= 10
    return res


memo = {}
def num_universes(positions, points=(0, 0), turn=0):
    t = tuple(positions + list(points) + [turn])
    if t in memo:
        return memo[t]
    if points[0] >= 21:
        return 1, 0
    elif points[1] >= 21:
        return 0, 1
    unis = [0, 0]
    for roll, coef in rolls_to_coefs.items():
        new_pos = [positions[0], positions[1]]
        new_pos[turn] = move(new_pos[turn], roll)
        new_points = [points[0], points[1]]
        new_points[turn] += new_pos[turn]
        res = num_universes(new_pos, new_points, 1-turn)
        unis[0] += res[0] * coef
        unis[1] += res[1] * coef
    memo[t] = unis
    return unis


class Day(DayBase):
    @property
    def num(self) -> int:
        return 21

    def get_data(self, example=False):
        if example:
            return [4, 8]
        else:
            return [4, 1]

    def puzzle1(self):
        turn = 0
        die = 1
        points = [0, 0]
        positions = self.get_data()
        for i in itertools.count():
            for _ in range(3):
                positions[turn] += die
                while positions[turn] > 10:
                    positions[turn] -= 10
                die += 1
                while die > 100:
                    die -= 100
            points[turn] += positions[turn]
            if points[turn] >= 1000:
                print(points[1 - turn] * (3 * (i + 1)))
                return
            turn = 1 - turn

    def puzzle2(self):
        res = num_universes(self.get_data())
        print(res)
        print(max(res))
