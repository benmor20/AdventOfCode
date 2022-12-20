from year2022.day2022 import Day2022


def distance(a, b):
    diff = a - b
    return abs(diff.real) + abs(diff.imag)


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
        data = self.get_data()
        max_size = 4000001
        beacon_dists = {s: distance(s, b) for s, b in data}
        for x in range(0, max_size):
            for y in range(0, max_size):
                pos = x + y*1j
                never_in_range = True
                for sensor, dist in beacon_dists.items():
                    if distance(pos, sensor) <= dist:
                        never_in_range = False
                        break
                if never_in_range:
                    print(4000000 * x + y)
                    return
