import itertools
from collections import deque

from year2024.day2024 import Day2024


class Pseudorandom:
    def __init__(self, seed):
        self.value = seed

    def next_number(self):
        self.value = (self.value ^ (self.value << 6)) % 16777216
        self.value = (self.value ^ (self.value >> 5)) % 16777216
        self.value = (self.value ^ (self.value << 11)) % 16777216
        return self.value


class Day(Day2024):
    @property
    def num(self) -> int:
        return 22

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [int(i) for i in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for seed in data:
            rand = Pseudorandom(seed)
            for _ in range(1999):
                rand.next_number()
            final = rand.next_number()
            total += final
        print(total)

    def puzzle2(self):
        data = self.get_data()
        sequences = {}
        for seed in data:
            rand = Pseudorandom(seed)
            seen = set()
            queue = deque()
            prev = seed % 10
            for _ in range(2000):
                nxt = rand.next_number() % 10
                diff = nxt - prev
                prev = nxt
                queue.append(diff)
                if len(queue) <= 4:
                    continue
                queue.popleft()
                seq = tuple(queue)
                assert len(seq) == 4
                if seq in seen:
                    continue
                seen.add(seq)
                if seq not in sequences:
                    sequences[seq] = 0
                sequences[seq] += nxt
        print(max(sequences.values()))


def one_line():
    pass
