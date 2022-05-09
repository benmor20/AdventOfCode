import math
from typing import *
from year2019.day2019 import Day2019
import numpy as np
import itertools as it


class Moon:
    def __init__(self, pos: np.ndarray):
        self.pos = pos
        self.vel = np.zeros(pos.shape, dtype=int)

    @property
    def kinetic_energy(self) -> int:
        return int(np.sum(np.abs(self.vel)))

    @property
    def potential_energy(self) -> int:
        return int(np.sum(np.abs(self.pos)))

    @property
    def total_energy(self) -> int:
        return self.kinetic_energy * self.potential_energy

    def apply_gravity(self, other):
        self.vel += np.sign(other.pos - self.pos)

    def update_pos(self):
        self.pos += self.vel

    def __repr__(self):
        return f'<pos={self.pos} vel={self.vel}>'

    def __hash__(self):
        return hash(tuple(np.append(self.pos, self.vel)))

    def __eq__(self, other):
        return np.all(self.pos == other.pos) and np.all(self.vel == other.vel)

    def __copy__(self):
        m = Moon(self.pos.copy())
        m.vel = self.vel.copy()
        return m


def step(moons):
    for m1, m2 in it.product(moons, repeat=2):
        m1.apply_gravity(m2)
    for moon in moons:
        moon.update_pos()
    return moons


class Day(Day2019):
    @property
    def num(self) -> int:
        return 12

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        moons = [Moon(np.array([int(a[2:]) for a in l[1:-1].split(', ')])) for l in lines]
        return moons

    def puzzles(self):
        moons = self.get_data()
        nsteps = 1000
        for s in range(nsteps):
            moons = step(moons)
        total_energy = sum(m.total_energy for m in moons)
        print(f'After {nsteps} steps, there is {total_energy} energy in the system')

        moons = self.get_data()
        moons_by_axis = [[Moon(np.array([m.pos[a]])) for m in moons] for a in range(3)]
        rep_len = []
        for a, axis_moons in enumerate(moons_by_axis):
            start_pos = [m.pos[0] for m in axis_moons]
            i = 1
            for i in it.count(1):
                axis_moons = step(axis_moons)
                if [m.pos[0] for m in axis_moons] == start_pos and all(m.vel[0] == 0 for m in axis_moons):
                    break
            print(f'Axis {a} took {i} steps to repeat')
            rep_len.append(i)
        print(f'The full cycle will repeat every {math.lcm(*rep_len)} steps')
