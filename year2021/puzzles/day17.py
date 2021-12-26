from year2021.day2021 import Day2021
from utils import *


def in_range(values, xrange, yrange):
    return xrange[0] <= values[0] <= xrange[1]\
            and yrange[0] <= values[1] <= yrange[1]


def lands(initial_velocity, xrange, yrange):
    pos = 0, 0
    vel = initial_velocity
    # print(f'NEW INITIAL: {initial_velocity}')
    while not in_range(pos, xrange, yrange):
        if pos[0] > xrange[1]:
            if pos[1] < yrange[0]:
                return False, 'xy'
            else:
                return False, 'x'
        elif pos[1] < yrange[0]:
            return False, 'y'

        pos = add_tuples([pos, vel])
        # print(f'pos is {pos}')
        vel = (vel[0] - signum(vel[0]), vel[1] - 1)
    return True, 'xy'


def max_height(initial_y):
    pos = 0
    prev_pos = -1
    vel = initial_y
    while prev_pos < pos:
        prev_pos = pos
        pos += vel
        vel -= 1
    return prev_pos


def best_x(xrange):
    x = 1
    while not in_range((x * (x + 1) // 2, 0), xrange, (-1, 1)):
        x += 1
    return x


def reverse_ypath(end, prev):
    diff = end - prev
    while True:
        diff += 1
        prev -= diff
        if prev < 0 < diff:
            return diff - 1


class Day(Day2021):
    @property
    def num(self) -> int:
        return 17

    def get_data(self, example=False):
        line = super().get_data(example)[0]
        by_section = line.split(', ')
        res = ()
        for section in by_section:
            nums = section.split('=')[-1]
            res += (tuple(int(i) for i in nums.split('..')), )
        return res

    def puzzle1(self):
        xrange, yrange = self.get_data()
        print(max_height(-yrange[0] - 1))

    def puzzle2(self):
        xrange, yrange = self.get_data()
        count = 0
        for x in range(xrange[1] + 1):
            for y in range(-yrange[0] + 1):
                for yscale in ((1, ) if y == 0 else (1, -1)):
                    vel = x, y * yscale
                    if lands((vel), xrange, yrange)[0]:
                        # print(vel)
                        count += 1
        print(count)
