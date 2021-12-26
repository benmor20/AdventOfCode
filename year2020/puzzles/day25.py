import itertools
from year2020.day2020 import Day2020_3


def transform(subject, loops, value=1):
    for _ in range(loops):
        value *= subject
        value %= 20201227
    return value


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 25

    def get_data(self, example: bool = False):
        if example:
            return 5764801, 17807724
        else:
            return 8252394, 6269621

    def puzzle(self, num=1):
        if num == 1:
            public_keys = self.get_data()
            loop_nums = (None, None)
            value = 1
            for loop in itertools.count(1):
                value = transform(7, 1, value)
                if value == public_keys[0] and loop_nums[0] is None:
                    loop_nums = loop, loop_nums[1]
                if value == public_keys[1] and loop_nums[1] is None:
                    loop_nums = loop_nums[0], loop
                if all(loop_nums):
                    break
            print(loop_nums)
            print(transform(public_keys[0], loop_nums[1]))
