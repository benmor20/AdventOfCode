from year2020.day2020 import Day2020_3
from collections import deque


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 9

    def get_data(self, example: bool = False):
        return deque(int(i) for i in super().get_data(example))

    def is_sum(self, nums, num):
        num_set = set(nums)
        for n in num_set:
            if num - n in num_set and num != n * 2:
                return True
        return False

    def puzzle(self, num=1):
        example = False
        full_queue = self.get_data(example)
        preamble = 5 if example else 25
        queue = deque()
        for _ in range(preamble):
            queue.append(full_queue.popleft())
        res = 0
        while len(full_queue) > 0:
            n = full_queue.popleft()
            if not self.is_sum(queue, n):
                print(n)
                res = n
                if num == 1:
                    return
                break
            queue.popleft()
            queue.append(n)

        full_list = list(self.get_data(example))
        for starti, start in enumerate(full_list):
            total = 0
            lst = []
            for val in full_list[starti:]:
                lst.append(val)
                total += val
                if total == res:
                    print(min(lst) + max(lst))
                    return
                if total > res:
                    break
