from year2021.day2021 import Day2021
import numpy as np
from scipy.signal import correlate2d


kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


class Day(Day2021):
    @property
    def num(self) -> int:
        return 11

    def get_data(self, example=False):
        return np.array([[int(i) for i in row] for row in super().get_data(example)])

    def puzzle1(self):
        octopi = self.get_data()
        flashes = 0
        for _ in range(100):
            octopi += 1
            oct_flash = octopi > 9
            all_flash = oct_flash
            while np.sum(oct_flash) > 0:
                octopi += ~oct_flash * correlate2d(oct_flash, kernel, mode='same')
                octopi[all_flash] = 0
                oct_flash = octopi > 9
                all_flash = all_flash | oct_flash
            flashes += np.sum(all_flash)
        print(flashes)

    def puzzle2(self):
        octopi = self.get_data()
        flashes = 0
        for i in range(10000000):
            octopi += 1
            oct_flash = octopi > 9
            all_flash = oct_flash
            while np.sum(oct_flash) > 0:
                octopi += ~oct_flash * correlate2d(oct_flash, kernel, mode='same')
                octopi[all_flash] = 0
                oct_flash = octopi > 9
                all_flash = all_flash | oct_flash
            total = np.sum(all_flash)
            if total == octopi.shape[0] * octopi.shape[1]:
                print(i + 1)
                return
        print(flashes)
