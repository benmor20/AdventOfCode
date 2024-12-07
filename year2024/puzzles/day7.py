import itertools
import re

from year2024.day2024 import Day2024
from typing import *


def can_get_val(val: int, nums: list[int], can_concat: bool = False) -> bool:
    if len(nums) == 1:
        return val == nums[0]
    if val % nums[-1] == 0 and can_get_val(val // nums[-1], nums[:-1], can_concat):
        return True
    if can_concat and str(val).endswith(str(nums[-1])) and len(str(val)) > len(str(nums[-1])) and can_get_val(int(str(val)[:-len(str(nums[-1]))]), nums[:-1], can_concat):
        return True
    return val > nums[-1] and can_get_val(val - nums[-1], nums[:-1], can_concat)


class Day(Day2024):
    @property
    def num(self) -> int:
        return 7

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            target, nums = line.split(': ')
            data.append((int(target), [int(i) for i in nums.split(' ')]))
        return data

    def puzzle1(self):
        # data = self.get_data()
        # res = 0
        # for total, nums in data:
        #     for ops in itertools.product('+*', repeat=len(nums) - 1):
        #         val = nums[0]
        #         for op, num in zip(ops, nums[1:]):
        #             if op == '+':
        #                 val += num
        #             elif op == '*':
        #                 val *= num
        #             if val > total:
        #                 break
        #         if val == total:
        #             res += total
        #             break
        # print(res)

        data = self.get_data()
        total = sum(val for val, nums in data if can_get_val(val, nums))
        print(total)

    def puzzle2(self):
        # data = self.get_data()
        # res = 0
        # for total, nums in data:
        #     for ops in itertools.product('+*|', repeat=len(nums) - 1):
        #         val = nums[0]
        #         for op, num in zip(ops, nums[1:]):
        #             if op == '+':
        #                 val += num
        #             elif op == '*':
        #                 val *= num
        #             elif op == '|':
        #                 val = int(str(val) + str(num))
        #             if val > total:
        #                 break
        #         if val == total:
        #             res += total
        #             break
        # print(res)

        data = self.get_data()
        total = sum(val for val, nums in data if can_get_val(val, nums, True))
        print(total)


def one_line():
    return '\n'.join([data := [(int(line.split(': ')[0]), [int(i) for i in line.split(': ')[1].split(' ')]) for line in open('year2024/data/day7data.txt').readlines()], (can_get := lambda val, nums, pt2: val == nums[0] if len(nums) == 1 else (val % nums[-1] == 0 and can_get(val // nums[-1], nums[:-1], pt2)) or (pt2 and str(val).endswith(str(nums[-1])) and len(str(val)) > len(str(nums[-1])) and can_get(int(str(val)[:-len(str(nums[-1]))]), nums[:-1], pt2)) or (val > nums[-1] and can_get(val - nums[-1], nums[:-1], pt2))), str(sum(val for val, nums in data if can_get(val, nums, False))), str(sum(val for val, nums in data if can_get(val, nums, True)))][-2:])
