from year2023.day2023 import Day2023
from typing import *
import re
import numpy as np


class Day(Day2023):
    @property
    def num(self) -> int:
        return 6

    def get_data(self, example=False):
        lines = super().get_data(example)
        times = [int(i) for i in re.split(' +', lines[0].split(':')[1]) if len(i) > 0]
        dists = [int(i) for i in re.split(' +', lines[1].split(':')[1]) if len(i) > 0]
        return times, dists

    def puzzle1(self):
        times, records = self.get_data()
        prod = 1
        for time, record in zip(times, records):
            allowed_times = np.arange(time + 1)
            dists = allowed_times * (time - allowed_times)
            prod *= np.sum(dists > record)
        # print(prod)

    def puzzle2(self):
        times, records = self.get_data()
        time = int(''.join(str(t) for t in times))
        record = int(''.join(str(r) for r in records))
        # allowed_times = np.arange(time + 1)
        # dists = allowed_times * (time - allowed_times)
        # print(np.sum(dists > record))
        cnt = 0
        for wait_time in range(time + 1):
            speed = wait_time
            rem_time = time - wait_time
            dist = speed * rem_time
            if dist > record:
                cnt += 1
        print(cnt)

def one_line():
    pass
