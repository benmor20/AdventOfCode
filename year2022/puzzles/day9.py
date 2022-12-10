import numpy as np

from year2022.day2022 import Day2022


DIRECTIONS = {
    'R': np.array([0, 1]),
    'L': np.array([0, -1]),
    'U': np.array([1, 0]),
    'D': np.array([-1, 0])
}


def update_position(head, tail, drctn, is_head = True):
    if is_head:
        head += drctn
    diff = head - tail
    if np.any(np.abs(diff) > 1):
        if np.any(diff == 0):
            tail += diff // 2
        else:
            tail += np.sign(diff)
    return head, tail


class Day(Day2022):
    @property
    def num(self) -> int:
        return 9

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            d, i = tuple(line.split(' '))
            data.append((d, int(i)))
        return data

    def puzzle1(self):
        data = self.get_data()
        seen = {(0, 0)}
        head = np.array([0, 0])
        tail = head.copy()

        for drctn_str, amt in data:
            drctn = DIRECTIONS[drctn_str]
            for _ in range(amt):
                head, tail = update_position(head, tail, drctn)
                seen.add(tuple(tail))
        print(len(seen))

    def puzzle2(self):
        data = self.get_data()
        seen = {(0, 0)}
        poses = [np.array([0, 0]) for _ in range(10)]

        for dir_str, amt in data:
            drctn = DIRECTIONS[dir_str]
            for _ in range(amt):
                for i in range(9):
                    poses[i], poses[i+1] = update_position(poses[i], poses[i+1], drctn, i == 0)
                seen.add(tuple(poses[-1]))
        print(len(seen))
