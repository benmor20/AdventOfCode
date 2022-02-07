import numpy as np
from scipy.signal import correlate


def get_data(example=False):
    with open(f'year2020/data/day24{"ex" if example else ""}data.txt', 'r') as file:
        lines = [line.replace('\n', '') for line in file.readlines()]
    data = []
    for line in lines:
        i = 0
        instr = []
        while i < len(line):
            c = line[i]
            if c in 'ns':
                instr.append(line[i:i + 2])
                i += 2
            else:
                instr.append(c)
                i += 1
        data.append(instr)
    return data


# Complex numbers to symbolizes indexes - adding is easier than with tuples
drctn_updates = {
    'e': 1 + 0j,
    'w': -1 + 0j,
    'ne': 1 + 1j,
    'nw': 0 + 1j,
    'se': 0 - 1j,
    'sw': -1 - 1j
}

# 10 in mid of kernel to differentiate white tiles and black tiles
kernel = np.array([[1,  1, 0],
                   [1, 10, 1],
                   [0,  1, 1]])

# Tile becomes black if white (<10) and 2 black tiles around it
# Tile stays black if black (>=10) and 1 or 2 black tiles around it
lookup_table = np.zeros(17)
lookup_table[np.array([2, 11, 12])] = 1


def index_from_complex(cmplx):
    return int(cmplx.real), int(cmplx.imag)


def get_tile(instruction):
    return sum(drctn_updates[i] for i in instruction)


def print_hex_grid(grid):
    for i, row in enumerate(grid):
        d, m = divmod(len(grid) - i, 2)
        if m == 1:
            print(' ', end='')
        print('. ' * d, end='')
        print(' '.join('#' if v == 1 else '.' for v in row), end='')
        print(' .' * (i // 2))


def day24():
    instructions = get_data()
    black_tiles = set()

    # Determine all the black tiles
    for instr in instructions:
        tile = get_tile(instr)
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)
    print(f'On day 0 there are {len(black_tiles)} black tiles')
    print(f'The black tiles are {black_tiles}')

    # Find highest and lowest index to make grid from
    lo = 100 + 100 * 1j  # 100 is more than enough for upper bound
    hi = -lo
    for tile in black_tiles:
        lo = min(lo.real, tile.real) + min(lo.imag, tile.imag) * 1j
        hi = max(hi.real, tile.real) + max(hi.imag, tile.imag) * 1j
    grid_size = hi - lo + 1 + 1j

    # Populate grid
    grid = np.zeros(index_from_complex(grid_size))
    for tile in black_tiles:
        grid[index_from_complex(tile - lo)] = 1
    print_hex_grid(grid)

    # Run daily updates
    print(f'Day 0: {int(np.sum(grid))}')
    for i in range(1, 101):
        corr = correlate(grid, kernel).round().astype(int)
        grid = lookup_table[corr]
        print(f'Day {i}: {int(np.sum(grid))}')
        if i <= 12:  # With example, 1-10 match up but by 20 it's different
            print_hex_grid(grid)


if __name__ == '__main__':
    day24()
