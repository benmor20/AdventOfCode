import itertools

from year2024.day2024 import Day2024
from typing import *


class Day(Day2024):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            data.append([int(i) for i in line.split()])
        return data

    def is_safe(self, report):
        if len(report) <= 1:
            return True
        decreasing = report[1] < report[0]
        for i in range(1, len(report)):
            diff = report[i] - report[i - 1]
            if not (1 <= abs(diff) <= 3 and (diff < 0) == decreasing):
                return False
        return True

    def is_safe_damp(self, report):
        # if len(report) <= 2:
        #     return True
        # if self.is_safe(report[1:]) or self.is_safe([report[0]] + report[2:]):
        #     return True
        # damp_idx = None
        # decreasing = report[1] < report[0]
        # for i in range(1, len(report)):
        #     diff = report[i] - report[i - 1 if damp_idx is None or i - 1 != damp_idx else i - 2]
        #     if not (1 <= abs(diff) <= 3 and (diff < 0) == decreasing):
        #         if damp_idx is not None:
        #             return False
        #         damp_idx = i
        # return True
        for i in range(len(report)):
            if self.is_safe(report[:i] + report[i + 1:]):
                return True
        return False

    def puzzle1(self):
        data = self.get_data()
        print(sum(self.is_safe(report) for report in data))

    def puzzle2(self):
        data = self.get_data()
        print(sum(self.is_safe_damp(report) for report in data))


def one_line():
    return '\n'.join([reports := [[int(i) for i in line.strip().split()] for line in open('year2024/data/day2data.txt', 'r').readlines()], is_safe := lambda report: len(report) <= 1 or all(1 <= abs(a - b) <= 3 and (a < b) == (report[0] < report[1]) for a, b in itertools.pairwise(report)), is_safe_damp := lambda report: any(is_safe(report[:i] + report[i + 1:]) for i in range(len(report))), str(sum(is_safe(report) for report in reports)), str(sum(is_safe_damp(report) for report in reports))][-2:])
