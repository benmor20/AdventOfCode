from year2024.day2024 import Day2024
from typing import *
import numpy as np
from scipy.signal import correlate


def unzip_filesys(compact: list[int]) -> list[int]:
    res = []
    for idx, blocks in enumerate(compact):
        res.extend([idx // 2 if idx % 2 == 0 else -1] * blocks)
    return res


class Day(Day2024):
    @property
    def num(self) -> int:
        return 9

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for idx, blocks in enumerate(lines[0]):
            data.extend([idx // 2 if idx % 2 == 0 else -1] * int(blocks))
        return data

    def puzzle1(self):
        file_sys = self.get_data()
        blocks_used = sum(1 if b >= 0 else 0 for b in file_sys)
        right_idx = len(file_sys) - 1
        left_idx = 0
        while right_idx >= blocks_used:
            while file_sys[left_idx] >= 0:
                left_idx += 1
            if file_sys[right_idx] >= 0:
                file_sys[left_idx] = file_sys[right_idx]
                file_sys[right_idx] = -1
            right_idx -= 1
        checksum = sum(i * file_sys[i] for i in range(blocks_used))
        print(checksum)

    def puzzle2(self):
        file_sys = np.array(self.get_data())

        # Find the start index and length of each file
        file_data = []
        for idx, val in enumerate(file_sys):
            if idx == 0:
                file_data.append((0, -1))
                continue
            if val != len(file_data) - 1 and file_data[-1][1] == -1:
                file_data[-1] = (file_data[-1][0], idx - file_data[-1][0])
            if val == len(file_data):
                file_data.append((idx, -1))
        file_data[-1] = file_data[-1][0], len(file_sys) - file_data[-1][0]

        # Move each file over
        for file_id in range(len(file_data))[::-1]:
            start, length = file_data[file_id]
            corr = correlate(file_sys, np.ones((length, )), mode='valid')
            locs = np.where(corr == -length)[0]
            if len(locs) == 0:  # No place in filesystem with (length) empty spaces
                continue
            leftmost = locs[0]
            if leftmost > start:  # Only viable spot to move it to is to the right
                continue
            # Move file
            file_sys[leftmost:leftmost + length] = file_id
            file_sys[start:start + length] = -1
            file_data[file_id] = (leftmost, length)

        # Calculate checksum
        checksum = sum(i * f for i, f in enumerate(file_sys) if f != -1)
        print(checksum)


def one_line():
    pass
