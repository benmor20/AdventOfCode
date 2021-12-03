from puzzles.daybase import DayBase
from collections import deque


class Day(DayBase):
    @property
    def num(self) -> int:
        return 1

    def get_data(self):
        return [int(d) for d in super().get_data()]

    def puzzle1(self):
        data = self.get_data()
        increases = 0
        prev = data[0]
        for d in data[1:]:
            if d > prev:
                increases += 1
            prev = d
        print(increases)

    def puzzle2(self):
        window_size = 3
        data = self.get_data()
        increases = 0
        queue = deque(data[:window_size])
        prev = sum(queue) / window_size
        for d in data[window_size:]:
            queue.popleft()
            queue.append(d)
            av = sum(queue) / window_size
            if av > prev:
                increases += 1
            prev = av
        print(increases)
