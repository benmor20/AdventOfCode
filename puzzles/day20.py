from puzzles.daybase import DayBase
import numpy as np
from scipy.signal import correlate2d


kernel = np.array([[256, 128, 64], [32, 16, 8], [4, 2, 1]])


def step(key, image, step=0):
    fill = 0
    if step > 0:
        fill = key[0 if step % 2 == 0 else 1]
    return key[correlate2d(image, kernel, fillvalue=(step % 2))]


def print_image(image):
    for row in image:
        for v in row:
            print('#' if v == 1 else '.', end='')
        print()
    print()


class Day(DayBase):
    @property
    def num(self) -> int:
        return 20

    def get_data(self, example=False):
        lines = super().get_data(example)
        key = [1 if c == '#' else 0 for c in lines[0]]
        image = []
        for line in lines[2:]:
            image.append([1 if c == '#' else 0 for c in line])
        return np.array(key), np.array(image)

    def puzzle1(self):
        key, image = self.get_data()
        for i in range(2):
            image = step(key, image, step=i)
        print(np.sum(image))

    def puzzle2(self):
        key, image = self.get_data()
        for i in range(50):
            image = step(key, image, step=i)
        print(np.sum(image))
