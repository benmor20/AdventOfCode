from year2021.day2021 import Day2021
import numpy as np


def overlap2(bounds1, bounds2):
    return area(overlap2_bounds(bounds1, bounds2))


def overlap2_bounds(bounds1, bounds2):
    if isinstance(bounds1, slice) or len(bounds1) == 1:
        if isinstance(bounds1, list):
            bounds1 = bounds1[0]
            bounds2 = bounds2[0]
        if bounds1.start <= bounds2.start < bounds1.stop:
            return slice(bounds2.start, min(bounds1.stop, bounds2.stop))
        elif bounds1.start <= bounds2.stop < bounds1.stop:
            return slice(max(bounds1.start, bounds2.start), bounds2.stop)
        return None
    res = []
    for b1, b2 in zip(bounds1, bounds2):
        if b1 is None or b2 is None:
            return None
        bounds = overlap2_bounds(b1, b2)
        if bounds is None:
            return None
        res.append(bounds)
    return tuple(res)


def combined_overlap(of, wrt, ignoring=()):
    # Return the overlap of one bounds wrt a list of others, but ignore those with overlap in other list
    if len(wrt) == 0:
        return 0
    if of is None:
        return 0
    overlap = 0
    for i, bound in enumerate(wrt):
        if bound is None:
            continue
        # How to deal with triple overlap?
        overlap_bounds = overlap2_bounds(of, bound)
        overlap += area(overlap_bounds)
        overlap -= combined_overlap(overlap_bounds, ignoring)
        overlap -= combined_overlap(overlap_bounds, wrt[:i], ignoring)
    return overlap


def area(bounds):
    # I forget the name to N-Dimensional analog of area so we're going with this
    if bounds is None:
        return 0
    prod = 1
    for b in bounds:
        if b is None:
            return 0
        prod *= b.stop - b.start
    return prod


class Day(Day2021):
    @property
    def num(self) -> int:
        return 22

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            onoff, vals = tuple(line.split(' '))
            nums = vals.split(',')
            info = []
            for num in nums:
                edges = num[2:].split('..')
                info.append(slice(int(edges[0]), int(edges[1]) + 1))
            data.append((onoff == 'on', tuple(info)))
        return data

    def puzzle1(self):
        commands = self.get_data(True)
        arr = np.zeros((101, 101, 101))
        for onoff, (xrange, yrange, zrange) in commands:
            arr[xrange.start+50:xrange.stop+50,
                yrange.start + 50:yrange.stop + 50,
                zrange.start + 50:zrange.stop + 50] = 1 if onoff else 0
        print(np.sum(arr))

    def puzzle2(self):
        commands = self.get_data(True)
        onranges, offranges = [], []
        total = 0
        for onoff, bounds in commands:
            if onoff:
                total += area(bounds)
                total -= combined_overlap(bounds, onranges, offranges)
                onranges.append(bounds)
            else:
                total -= combined_overlap(bounds, onranges, offranges)
                offranges.append(bounds)
        print(total)
        print(total / 2758514936282235)
