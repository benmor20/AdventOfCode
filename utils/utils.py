def add_tuples(tuples):
    return tuple(sum(t[i] for t in tuples) for i in range(len(tuples)))


def signum(v):
    return 0 if v == 0 else abs(v) / v


def print_grid(grid):
    for row in grid:
        print(''.join('#' if c == 1 else '.' for c in row))
