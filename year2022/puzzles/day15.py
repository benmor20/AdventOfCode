from year2022.day2022 import Day2022
from typing import *


def distance(a, b):
    diff = a - b
    return abs(diff.real) + abs(diff.imag)


def all_of_dist(origin: complex, dist: int) -> Generator[complex, None, None]:
    pos = origin + dist
    while pos.real > origin.real:
        yield pos
        pos += -1+1j
    while pos.imag > origin.imag:
        yield pos
        pos += -1-1j
    while pos.real < origin.real:
        yield pos
        pos += 1-1j
    while pos != origin + dist:
        yield pos
        pos += 1+1j


class Day(Day2022):
    @property
    def num(self) -> int:
        return 15

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            sensor_str, beacon_str = tuple(line.split(': '))
            sensor_splt = sensor_str.split('=')
            beacon_splt = beacon_str.split('=')
            sensor = int(sensor_splt[1][:-3]) + int(sensor_splt[2])*1j
            beacon = int(beacon_splt[1][:-3]) + int(beacon_splt[2]) * 1j
            data.append((sensor, beacon))
        return data

    def puzzle1(self):
        data = self.get_data()
        row = 2000000
        seen = set()
        for sensor, beacon in data:
            dist = distance(beacon, sensor)
            dist_to_row = abs(sensor.imag - row)
            rem_dist = dist - dist_to_row
            if rem_dist >= 0:
                seen.update(set(range(int(sensor.real - rem_dist), int(sensor.real + rem_dist + 1))))
            if beacon.imag == row and beacon.real in seen:
                seen.remove(int(beacon.real))
        print(len(seen))

    def puzzle2(self):
        ex = False
        data = self.get_data(ex)
        max_size = 20 if ex else 4000000
        beacon_dists = {s: distance(s, b) for s, b in data}
        for sensor, dist in beacon_dists.items():
            # print(f'Sensor {sensor} has a dist of')
            for pt in all_of_dist(sensor, dist + 1):
                # print()
                if not (0 <= pt.real <= max_size and 0 <= pt.imag <= max_size):
                    continue
                if all(distance(pt, s) > d for s, d in beacon_dists.items()):
                    print(4000000 * int(pt.real) + int(pt.imag))
                    return
        assert False
