from year2020.day2020 import Day2020
import numpy as np


def rotate(waypoint, k=1):
    if k == 0:
        return waypoint
    if k > 0:
        return rotate([-waypoint[1], waypoint[0]], k-1)
    return rotate([waypoint[1], -waypoint[0]], k+1)


class Day(Day2020):
    @property
    def num(self) -> int:
        return 12

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            data.append((line[0], int(line[1:])))
        return data

    def puzzles(self):
        directions = self.get_data()

        # Puzzle 1
        boat = [0, 0, 0]
        for instr, amt in directions:
            if instr == 'N':
                boat[1] += amt
            elif instr == 'S':
                boat[1] -= amt
            elif instr == 'E':
                boat[0] += amt
            elif instr == 'W':
                boat[0] -= amt
            elif instr == 'R':
                assert amt % 90 == 0
                boat[2] -= np.deg2rad(amt)
            elif instr == 'L':
                assert amt % 90 == 0
                boat[2] += np.deg2rad(amt)
            elif instr == 'F':
                boat[0] += amt * np.cos(boat[2])
                boat[1] += amt * np.sin(boat[2])
            else:
                assert False
            # print(f'{instr}{amt} -> {boat}')
        print(boat)
        print(abs(boat[0]) + abs(boat[1]))

        # Puzzle 2
        boat = [0, 0]
        waypoint = [10, 1]
        for instr, amt in directions:
            if instr == 'N':
                waypoint[1] += amt
            elif instr == 'S':
                waypoint[1] -= amt
            elif instr == 'E':
                waypoint[0] += amt
            elif instr == 'W':
                waypoint[0] -= amt
            elif instr == 'R':
                waypoint = rotate(waypoint, -amt // 90)
            elif instr == 'L':
                waypoint = rotate(waypoint, amt // 90)
            elif instr == 'F':
                boat[0] += amt * waypoint[0]
                boat[1] += amt * waypoint[1]
            else:
                assert False
        print(boat)
        print(abs(boat[0]) + abs(boat[1]))
