from year2023.day2023 import Day2023
from typing import *
import re


SYM_TO_NUM = {'?': -1, '.': 0, '#': 1}
NUM_TO_SYM = {-1: '?', 0: '.', 1: '#'}


CACHE = {}


def springs_to_str(springs: List[int]):
    return ''.join(NUM_TO_SYM[n] for n in springs)


def count_possibilities(springs: str, nums: List[int], verbose: bool = False) -> int:
    if verbose: print(springs, nums)
    cache_key = (springs, tuple(nums))
    if cache_key in CACHE:
        if verbose: print(f'Found in cache; returning {CACHE[cache_key]}')
        return CACHE[cache_key]
    if len(springs) == 0:
        if len(nums) == 0:
            if verbose: print('Got through all springs, no nums left, returning 1')
            CACHE[cache_key] = 1
            return 1
        if verbose: print('Got through all springs but there are still nums left; returning 0')
        CACHE[cache_key] = 0
        return 0
    if len(nums) == 0:
        res = 0 if any(s == '#' for s in springs) else 1
        if verbose: print(f'Got through all nums. Remaining springs: {springs}; Returning {res}')
        CACHE[cache_key] = res
        return res
    if len(springs) == 1:
        res = 1 if (len(nums) == 0 and springs[0] in '.?') or (len(nums) == 1 and nums[0] == 1 and springs[0] in '#?') else 0
        if verbose: print(f'Only one spring left: {springs[0]}')
        CACHE[cache_key] = res
        return res
    if sum(1 for c in springs if c in '?#') < sum(nums):
        if verbose: print('Not enough possible broken springs left')
        CACHE[cache_key] = 0
        return 0

    if springs[0] == '?':
        if verbose: print('Attempting #')
        with_bad_spring = count_possibilities(f'#{springs[1:]}', nums, verbose)
        if verbose: print(f'Done - found {with_bad_spring}')
        if verbose: print('Attempting .')
        with_good_spring = count_possibilities(springs[1:], nums, verbose)
        if verbose: print(f'Done - found {with_good_spring}')
        res = with_good_spring + with_bad_spring
        CACHE[cache_key] = res
        return res
    if springs[0] == '.':
        remaining = re.fullmatch(r'\.+([.#?]*)', springs).group(1)
        if verbose: print(f'Found operational spring. Continuing with {remaining}')
        res = count_possibilities(remaining, nums, verbose)
        CACHE[cache_key] = res
        return res
    if springs[0] == '#':
        if len(nums) == 1:
            pattern = f'[#?]{{{nums[0]}}}[.?]*'
            if re.fullmatch(pattern, springs) is None:
                if verbose: print('One num left and run doesnt match it')
                CACHE[cache_key] = 0
                return 0
            CACHE[cache_key] = 1
            return 1
        pattern = f'[#?]{{{nums[0]}}}[.?][.#?]*'
        match = re.fullmatch(pattern, springs)
        if match is None:
            if verbose: print('Run does not end at the right time')
            CACHE[cache_key] = 0
            return 0
        if verbose: print('Run ends properly. Continuing...')
        res = count_possibilities(springs[nums[0] + 1:], nums[1:], verbose)
        CACHE[cache_key] = res
        return res
    assert False


# Attempt at speeding it up by splitting it in half is actually slower :/

# def part2_split(spring_half1: str, spring_half2: str, num_half1: List[int], num_half2: List[int], verbose: Optional[str] = None) -> int:
#     first_half = part2(spring_half1, num_half1, None if verbose is None else verbose[0] + verbose)
#     if first_half == 0:
#         return 0
#     return first_half * part2(spring_half2, num_half2, None if verbose is None else verbose[0] + verbose)
#
#
# def part2(springs: str, nums: List[int], verbose: Optional[str] = None) -> int:
#     if verbose is not None: print(f'{verbose}{springs}, {nums}')
#     cache_key = (springs, tuple(nums))
#     if cache_key in CACHE:
#         if verbose is not None: print(f'{verbose}Found in cache - returning {CACHE[cache_key]}')
#         return CACHE[cache_key]
#     if len(springs) < 8:
#         res = part1(springs, nums)
#         if verbose: print(f'{verbose}part 1 gives {res}')
#         return res
#     if len(springs) == 0 or all(s == '.' for s in springs):
#         res = 1 if len(nums) == 0 else 0
#         if verbose is not None: print(f'{verbose}No more broken springs. Remaining nums: {len(nums)}. Returning {res}')
#         CACHE[cache_key] = res
#         return res
#     if len(springs) == 1:
#         if springs[0] == '#':
#             res = 1 if len(nums) == 1 and nums[0] == 1 else 0
#             if verbose is not None: print(f'{verbose}Only one broken spring. Returning {res}')
#             CACHE[cache_key] = res
#             return res
#         if springs[0] == '?':
#             res = 1 if len(nums) == 0 or len(nums) == 1 and nums[0] == 1 else 0
#             if verbose is not None: print(f'{verbose}One unknown spring. Returning {res}')
#             CACHE[cache_key] = res
#             return res
#     if len(nums) == 0:
#         res = 0 if any(s == '#' for s in springs) else 1
#         if verbose is not None: print(f'{verbose}No more nums. Returning {res}')
#         CACHE[cache_key] = res
#         return res
#     num_broke = sum(nums)
#     if (max_springs := sum(1 for s in springs if s in '?#')) < num_broke:
#         if verbose is not None: print(f'{verbose}Max number of springs is {max_springs} - not enough to hit {num_broke}')
#         CACHE[cache_key] = 0
#         return 0
#     if (min_springs := sum(1 for s in springs if s == '#')) > num_broke:
#         if verbose is not None: print(f'{verbose}Min number of springs is {min_springs} - too much for {num_broke}')
#         CACHE[cache_key] = 0
#         return 0
#
#     halflen = len(springs) // 2
#     first_half = springs[:halflen]
#     first_but_good = f'{first_half[:-1]}.'
#     first_but_bad = f'{first_half[:-1]}#'
#     second_half = springs[halflen:]
#     second_but_good = f'.{second_half[1:]}'
#     second_but_bad = f'#{second_half[1:]}'
#     recurse = lambda l, r: part2_split(first_half, second_half, l, r, verbose)
#     just_right = recurse([], nums)
#     if verbose: print(f'{verbose}Just right with {first_half} / {second_half} gives {just_right}')
#     total = just_right
#     if verbose: print(f'{verbose}Total starting at {total}')
#     for idx, num in enumerate(nums):
#         left_nums = nums[:idx + 1]
#         right_nums = nums[idx + 1:]
#         to_add = 0
#         if first_half[-1] == '#' and second_half[0] == '.':
#             to_add = recurse(left_nums, right_nums)
#         elif first_half[-1] == '#' and second_half[0] == '?':
#             to_add = part2_split(first_half, f'.{second_half[1:]}', left_nums, right_nums, verbose)
#         elif first_half[-1] == '.' and second_half[0] == '#':
#             to_add = recurse(left_nums, right_nums)
#         elif first_half[-1] == '.' and second_half[0] == '.':
#             to_add = recurse(left_nums, right_nums)
#         elif first_half[-1] == '.' and second_half[0] == '?':
#             to_add = recurse(left_nums, right_nums)
#         elif first_half[-1] == '?' and second_half[0] == '#':
#             to_add = part2_split(f'{first_half[:-1]}.', second_half, left_nums, right_nums, verbose)
#         elif first_half[-1] == '?' and second_half[0] == '.':
#             to_add = recurse(left_nums, right_nums)
#         elif first_half[-1] == '?' and second_half[0] == '?':
#             good_good = part2_split(first_but_good, second_but_good, left_nums, right_nums, verbose)
#             if verbose: print(f'{verbose}{first_but_good}/{left_nums} and {second_but_good}/{right_nums} gives {good_good} options')
#             bad_good = part2_split(first_but_bad, second_but_good, left_nums, right_nums, verbose)
#             if verbose: print(f'{verbose}{first_but_bad}/{left_nums} and {second_but_good}/{right_nums} gives {bad_good} options')
#             good_bad = part2_split(first_but_good, second_but_bad, left_nums, right_nums, verbose)
#             if verbose: print(f'{verbose}{first_but_good}/{left_nums} and {second_but_bad}/{right_nums} gives {good_bad} options')
#             to_add = good_good + bad_good + good_bad
#         total += to_add
#         if verbose: print(f'{verbose}{first_half}/{left_nums} and {second_half}/{right_nums} gives {to_add} options. total is now {total}')
#
#         if first_half[-1] != '.' and second_half[0] != '.':
#             for left_num in range(1, num):
#                 right_num = num - left_num
#                 left_nums = nums[:idx] + [left_num]
#                 right_nums = [right_num] + nums[idx+1:]
#                 res = part2_split(first_but_bad, second_but_bad, left_nums, right_nums, verbose)
#                 total += res
#                 if verbose: print(f'{verbose}{first_but_bad}/{left_nums} and {second_but_bad}/{right_nums} gives {res} options. total is now {total}')
#     CACHE[cache_key] = total
#     return total


class Day(Day2023):
    @property
    def num(self) -> int:
        return 12

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            syms, nums_str = tuple(line.split(' '))
            nums = [int(i) for i in nums_str.split(',')]
            data.append((syms, nums))
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for springs, nums in data:
            res = count_possibilities(springs, nums, False)
            total += res
        print(total)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        for idx, (springs, nums) in enumerate(data):
            new_springs = '?'.join([springs] * 5)
            new_nums = nums * 5
            res = count_possibilities(new_springs, new_nums)
            # print(f'{idx}: {new_springs}, {new_nums} -> {res}')
            total += res
        print(total)


def one_line():
    pass
