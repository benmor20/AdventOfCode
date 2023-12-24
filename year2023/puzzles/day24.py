import itertools

from year2023.day2023 import Day2023
from typing import *
import numpy as np
import re
import z3


class Day(Day2023):
    @property
    def num(self) -> int:
        return 24

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            match = re.fullmatch(r'(-?\d+), +(-?\d+), +(-?\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)', line)
            assert match is not None
            pos = np.array([int(match.group(i)) for i in range(1, 4)])
            vel = np.array([int(match.group(i)) for i in range(4, 7)])
            data.append((pos, vel))
        return data

    def puzzle1(self):
        is_ex = False
        minrange = (7 if is_ex else 200000000000000) * np.ones((2, ))
        maxrange = (27 if is_ex else 400000000000000) * np.ones((2, ))
        data = self.get_data(is_ex)
        hailstones = [(d[0][:2], d[1][:2]) for d in data]
        num_inter = 0
        for (pos1, vel1), (pos2, vel2) in itertools.combinations(hailstones, r=2):
            slope1 = vel1[1] / vel1[0]
            slope2 = vel2[1] / vel2[0]
            if slope1 == slope2:
                continue
            coefs = np.array([[-slope1, 1], [-slope2, 1]])
            try:
                inv = np.linalg.inv(coefs)
            except np.linalg.LinAlgError:
                continue
            vals = np.array([-slope1 * pos1[0] + pos1[1], -slope2 * pos2[0] + pos2[1]])
            intersection = inv @ vals
            if np.any((intersection < minrange) | (intersection > maxrange)):
                continue
            diff1 = (intersection - pos1) @ vel1
            diff2 = (intersection - pos2) @ vel2
            if diff1 > 0 and diff2 > 0:
                num_inter += 1
        print(num_inter)

    def puzzle2(self):
        data = self.get_data()
        p = z3.RealVector('p', 3)
        v = z3.RealVector('v', 3)
        ans = z3.Real('a')
        tis = [z3.Real(f't{i}') for i in range(4)]
        system = [ans == z3.Sum(p)]
        for idx, (pos, vel) in enumerate(data[:4]):
            ti = tis[idx]
            system.append(p[0] + ti * v[0] == pos[0] + ti * vel[0])
            system.append(p[1] + ti * v[1] == pos[1] + ti * vel[1])
            system.append(p[2] + ti * v[2] == pos[2] + ti * vel[2])
            system.append(ti >= 0)
        z3.solve(*system)  # Look for a = ????
        

def one_line():
    pass
