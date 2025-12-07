from typing import Optional


def add_tuples(*tuples):
    return tuple(sum(t[i] for t in tuples) for i in range(len(tuples)))


def signum(v):
    return 0 if v == 0 else abs(v) / v


def print_grid(grid):
    for row in grid:
        print(''.join('#' if v == 1 or (isinstance(v, bool) and v) else '.' for v in row))


def first_ele(obj):
    for e in obj:
        return e


def to_digits(num, ndigs=-1):
    digs = [int(i) for i in str(num)]
    if ndigs == -1:
        return digs
    if ndigs >= len(digs):
        return [0] * (ndigs - len(digs)) + digs
    return digs[-ndigs:]


def tuple_diff(t1, t2):
    res = []
    for i, e1 in enumerate(t1):
        res.append(e1 - t2[i])
    return tuple(res)


def in_range(x, min_range, max_range=None):
    if max_range is None:
        max_range = min_range
        min_range = tuple([0] * len(max_range))
    for i, ele in enumerate(x):
        if not min_range[i] <= ele <= max_range[i]:
            return False
    return True


def get_range_intersection(range1: range, range2: range) -> Optional[range]:
    # assumes step of 1
    # [range1] {range2}

    if range1 == range2:
        return range1
    if range1.stop <= range2.start or range1.start >= range2.stop:
        # [ ] { }
        # { } [ ]
        return None
    if range2.start in range1 and range2.stop >= range1.stop:
        # [ { ] }
        return range(range2.start, range1.stop)
    if range1.start in range2 and range1.stop in range2:
        # { [ ] }
        return range1
    if range2.start in range1 and range2.stop in range1:
        # [ { } ]
        return range2
    if range1.start in range2 and range1.stop >= range2.stop:
        # { [ } ]
        return range(range1.start, range2.stop)
    assert False, f"{range1}, {range2}"


def get_range_union(range1: range, range2: range) -> Optional[range]:
    # assumes (near) overlap. will return null if no way to represent the union as a single set
    if range1.start == range2.stop:
        return range(range2.start, range1.stop)
    if range1.stop == range2.start:
        return range(range1.start, range2.stop)

    intersection = get_range_intersection(range1, range2)
    if intersection is None:
        return None

    return range(min(range1.start, range2.start), max(range1.stop, range2.stop))
