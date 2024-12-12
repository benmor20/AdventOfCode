from year2024.day2024 import Day2024
from typing import Optional
from collections import deque


class Stone:
    def __init__(self, val: int, left: Optional['Stone'] = None, right: Optional['Stone'] = None):
        self.val = val
        self.left = left
        self.right = right

    def step(self):
        if self.val == 0:
            self.val = 1
        elif len((strval := str(self.val))) % 2 == 0:
            self.val = int(strval[len(strval) // 2:])
            left = Stone(int(strval[:len(strval) // 2]), self.left, self)
            if self.left is not None:
                self.left.right = left
            self.left = left
        else:
            self.val *= 2024

    def num_stones(self):
        stone = self
        count = 0
        while stone is not None:
            count += 1
            stone = stone.right
        return count

    def stones_created(self, num_blinks: int):
        pass


MEMO_LIST: dict[tuple[int, int], deque[int]] = {}
MEMO: dict[tuple[int, int], int] = {}


def num_stones(val: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    if (val, blinks) in MEMO:
        return MEMO[(val, blinks)]
    if val == 0:
        res = num_stones(1, blinks - 1)
        MEMO[(val, blinks)] = res
        return res
    if (vallen := len(strval := str(val))) % 2 == 0:
        leftval = int(strval[:vallen // 2])
        rightval = int(strval[vallen // 2:])
        leftstones = num_stones(leftval, blinks - 1)
        rightstones = num_stones(rightval, blinks - 1)
        res = leftstones + rightstones
        MEMO[(val, blinks)] = res
        return res
    res = num_stones(val * 2024, blinks - 1)
    MEMO[(val, blinks)] = res
    return res


def stones(val: int, blinks: int) -> deque[int]:
    if blinks == 0:
        return deque([val])
    if (val, blinks) in MEMO_LIST:
        return MEMO_LIST[(val, blinks)]
    try:
        most_blinks = max(b for v, b in MEMO_LIST if v == val and b < blinks)
    except ValueError:
        pass
    else:
        rem_blinks = blinks - most_blinks
        init_stones = MEMO_LIST[(val, most_blinks)]
        res_stones = deque()
        for stone in init_stones:
            res_stones += stones(stone, rem_blinks)
        MEMO_LIST[(val, blinks)] = res_stones
        return res_stones
    if val == 0:
        res = stones(1, blinks - 1)
        MEMO_LIST[(val, blinks)] = res
        return res
    if (vallen := len(strval := str(val))) % 2 == 0:
        leftval = int(strval[:vallen // 2])
        rightval = int(strval[vallen // 2:])
        leftstones = stones(leftval, blinks - 1)
        rightstones = stones(rightval, blinks - 1)
        res = leftstones + rightstones
        MEMO_LIST[(val, blinks)] = res
        return res
    res = stones(val * 2024, blinks - 1)
    MEMO_LIST[(val, blinks)] = res
    return res


class Day(Day2024):
    @property
    def num(self) -> int:
        return 11

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [int(i) for i in lines[0].split(' ')]
        return data

    def puzzle(self, p1, example):
        stones = self.get_data(example)
        nblinks = 25 if p1 else 75
        total = 0
        for stone in stones:
            total += num_stones(stone, nblinks)
        print(total)

    def puzzle1(self):
        self.puzzle(True, False)

    def puzzle2(self):
        self.puzzle(False, False)


def one_line():
    pass
