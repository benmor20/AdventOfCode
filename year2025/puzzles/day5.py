from utils.utils import get_range_union
from year2025.day2025 import Day2025


class RangeSet:
    def __init__(self):
        self._ranges = list[range]()

    def update(self, new_range: range):
        new_ranges = list[range]()
        overlap_idx = -1
        for idx, old_range in enumerate(self._ranges):
            union = get_range_union(old_range, new_range)
            if union is None:
                new_ranges.append(old_range)
            elif overlap_idx < 0:
                overlap_idx = idx
                new_ranges.append(union)
            else:
                new_ranges[overlap_idx] = get_range_union(new_ranges[overlap_idx], old_range)
        if overlap_idx < 0:
            new_ranges.append(new_range)
        self._ranges = new_ranges

    def __contains__(self, item: int) -> bool:
        return any(item in rng for rng in self._ranges)

    def __len__(self) -> int:
        return sum(len(rng) for rng in self._ranges)


class Day(Day2025):
    @property
    def num(self) -> int:
        return 5

    def get_data(self, example=False) -> tuple[list[range], set[int]]:
        lines = super().get_data(example)
        fresh_ranges = []
        ids = set()

        for line in lines:
            if len(line.strip()) == 0:
                continue
            if "-" in line:
                fresh_ranges.append(range(int((splt := line.split("-"))[0]), int(splt[1]) + 1))
            else:
                ids.add(int(line))
        return fresh_ranges, ids

    def puzzle1(self):
        fresh_ranges, ids = self.get_data()
        total_stock = len(ids)
        for rng in fresh_ranges:
            to_remove = set()
            for id in ids:
                if id in rng:
                    to_remove.add(id)
            ids.difference_update(to_remove)
        spoiled_stock = len(ids)
        print(total_stock - spoiled_stock)

    def puzzle2(self):
        fresh_ranges, _ = self.get_data(True)
        fresh = RangeSet()
        for rng in fresh_ranges:
            fresh.update(rng)
        print(len(fresh))


def one_line():
    pass
