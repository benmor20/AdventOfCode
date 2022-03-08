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
