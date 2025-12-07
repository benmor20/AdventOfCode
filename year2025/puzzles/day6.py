import re

import numpy as np

from year2025.day2025 import Day2025


def char_or_default(line: str, idx: int, default: str = " ") -> str:
    if idx >= len(line):
        return default
    return line[idx]



class Day(Day2025):
    @property
    def num(self) -> int:
        return 6

    def get_data(self, example=False, pt1=True):
        lines = super().get_data(example)
        if pt1:
            data = []
            ops = []
            for line in lines:
                if '+' in line or '*' in line:
                    ops = re.split(r"\s+", line.strip())
                    continue
                nums = re.split(r"\s+", line.strip())
                data.append([int(i) for i in nums])
            return np.array(data).T, ops

        nums = []
        ops = []
        current_nums = []
        for col in range(max(len(l) for l in lines)):
            op = char_or_default(lines[-1], col)
            if op != ' ':
                if len(ops) != 0:
                    nums.append(current_nums)
                    current_nums = []
                ops.append(op)

            num = 0
            for row in range(len(lines) - 1):
                space = char_or_default(lines[row], col)
                if space != ' ':
                    num *= 10
                    num += int(space)
            if num > 0:
                current_nums.append(num)
        nums.append(current_nums)
        return nums, ops

    def puzzle1(self):
        data, ops = self.get_data()
        total = 0
        for nums, op in zip(data, ops):
            if op == '+':
                total += sum(nums)
            elif op == '*':
                prod = 1
                for num in nums:
                    prod *= num
                total += prod
            else:
                assert False, op
        print(total)

    def puzzle2(self):
        data, ops = self.get_data(False, False)
        total = 0
        for nums, op in zip(data, ops):
            if op == '+':
                total += sum(nums)
            elif op == '*':
                prod = 1
                for num in nums:
                    prod *= num
                total += prod
            else:
                assert False, op
        print(total)



def one_line():
    pass
