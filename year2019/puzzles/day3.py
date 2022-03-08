from typing import *
from year2019.day2019 import Day2019


def get_points(path):
    points = [(0, 0, 0)]
    for drctn, dist in path:
        nxt_pt = list(points[-1])
        if drctn == 'U':
            nxt_pt[1] += dist
        elif drctn == 'D':
            nxt_pt[1] -= dist
        elif drctn == 'L':
            nxt_pt[0] -= dist
        elif drctn == 'R':
            nxt_pt[0] += dist
        nxt_pt[2] += dist
        points.append(nxt_pt)
    return points


def is_between(a, x, b):
    return a < x < b or b < x < a


def intersection(a, b, m, n):
    if (a[0] == b[0]) == (m[0] == n[0]):  # parallel
        return None
    if a[0] == b[0] and is_between(m[0], a[0], n[0]) and is_between(a[1], m[1], b[1]):
        return a[0], m[1]
    if a[1] == b[1] and is_between(m[1], a[1], n[1]) and is_between(a[0], m[0], b[0]):
        return m[0], a[1]
    return None


def manhattan(point):
    return sum(list(map(abs, point))[:2])


class Day(Day2019):
    @property
    def num(self) -> int:
        return 3

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        wires = []
        for line in lines:
            wires.append((p[0], int(p[1:])) for p in line.split(','))
        return wires

    def puzzles(self):
        wires = self.get_data()
        points = list(map(get_points, wires))

        p1_closest = (-1, -1)
        p2_closest = (-1, -1)
        p2_steps = -1
        for i, a in enumerate(points[0][:-1]):
            b = points[0][i + 1]
            for j, m in enumerate(points[1][:-1]):
                n = points[1][j + 1]
                intersect = intersection(a, b, m, n)
                if intersect:
                    steps1 = a[2] + abs(intersect[0] - a[0]) + abs(intersect[1] - a[1])
                    steps2 = m[2] + abs(intersect[0] - m[0]) + abs(intersect[1] - m[1])
                    steps = steps1 + steps2
                    if p1_closest[0] == -1 or manhattan(intersect) < manhattan(p1_closest):
                        p1_closest = intersect
                    if p2_steps == -1 or steps < p2_steps:
                        p2_closest = intersect
                        p2_steps = steps
        print(f'Closest dist is at {p1_closest}, it is {manhattan(p1_closest)}')
        print(f'Closest dist is at {p2_closest}, it is {p2_steps}')
