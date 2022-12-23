import numpy as np

from year2022.day2022 import Day2022
from typing import *


DIRECTION_SCORE = {1: 0, -1: 2, 1j: 1, -1j: 3}


def get_start(grid: Set[complex]):
    start = 0
    while True:
        if start in grid:
            return start
        start += 1


def move_pos(cur: complex, drctn: complex, amt: int, grid: Set[complex], walls: Set[complex]) -> complex:
    nxt = cur
    for _ in range(amt):
        nxt += drctn
        if nxt in walls:
            return nxt - drctn
        if nxt not in grid:
            last_on = nxt - drctn
            nxt = last_on
            while nxt in grid:
                nxt -= drctn
            nxt += drctn
            if nxt in walls:
                return last_on
    return nxt


def get_face(pos: complex, example: bool) -> int:
    """
    0 - bottom (where start is)
    1 - top
    2 - front (in input orientation, from bottom edge of bottom)
    3 - back
    4 - left
    5 - right
    """
    size = 4 if example else 50
    # print(f'get face {pos = }')
    sq_pos = int(pos.real) // size + (int(pos.imag) // size) * 1j
    if example:
        pos_to_face = {2: 0, 1j: 3, 1+1j: 4, 2+1j: 2, 2+2j: 1, 3+2j: 5}
    else:
        pos_to_face = {1: 0, 1+2j: 1, 1+1j: 2, 3j: 3, 2j: 4, 2: 5}
    if sq_pos in pos_to_face:
        return pos_to_face[sq_pos]
    return -1


def map_edge(start: complex, start_dir: complex, end: complex, end_dir: complex, val: complex) -> complex:
    return (val - start) * end_dir / start_dir + end


def cube_wrap(pos: complex, drctn: complex, example: bool) -> Tuple[complex, complex]:
    new_pos = pos + drctn
    new_face = get_face(new_pos, example)
    if new_face > -1:
        return new_pos, drctn
    cur_face = get_face(pos, example)
    # print(f'Cube wrap, {pos = }, {drctn = }')
    if example:
        if cur_face == 0:
            if drctn == 1:
                return map_edge(11, 1j, 15+11j, -1j, pos), -1
            if drctn == -1:
                return map_edge(8+3j, -1j, 7+1j, -1, pos), 1j
            if drctn == -1j:
                return map_edge(8, 1, 3+4j, -1, pos), 1j
            assert False
        if cur_face == 1:
            if drctn == -1:
                return map_edge(8+8j, 1j, 7+7j, -1, pos), -1j
            if drctn == 1j:
                return map_edge(8+11j, 1, 3+7j, -1, pos), -1j
            assert False
        if cur_face == 2:
            assert drctn == 1
            return map_edge(11+7j, -1j, 12+8j, 1, pos), 1j
        if cur_face == 3:
            if drctn == -1:
                return map_edge(7j, -1j, 12+11j, 1, pos), -1j
            if drctn == 1j:
                return map_edge(3+7j, -1, 8+11j, 1, pos), 1j
            if drctn == -1j:
                return map_edge(3+4j, -1, 8, 1, pos), -1j
            assert False
        if cur_face == 4:
            assert drctn.real == 0
            if drctn == 1j:
                return map_edge(7+7j, -1, 8+8j, 1j, pos), 1
            if drctn == -1j:
                return map_edge(7+4j, -1, 8+3j, -1j, pos), 1
        if cur_face == 5:
            if drctn == 1:
                return map_edge(15+8j, 1j, 11+3j, -1j, pos), -1
            if drctn == 1j:
                return map_edge(15+11j, -1, 11, -1, pos), 1j
            if drctn == -1j:
                return map_edge(12+8j, 1, 11+7j, -1j, pos), -1
            assert False
        assert False
    else:
        if cur_face == 0:
            if drctn == -1:
                return map_edge(50+49j, -1j, 100j, 1j, pos), 1
            if drctn == -1j:
                return map_edge(50, 1, 150j, 1j, pos), 1
        if cur_face == 1:
            if drctn == 1:
                return map_edge(99+100j, 1j, 149+49j, -1j, pos), -1
            if drctn == 1j:
                return map_edge(50+149j, 1, 49+150j, 1j, pos), -1
        if cur_face == 2:
            if drctn == 1:
                return map_edge(99+50j, 1j, 100+49j, 1, pos), -1j
            if drctn == -1:
                return map_edge(50+99j, -1j, 49+100j, -1, pos), 1j
        if cur_face == 3:
            if drctn == 1:
                return map_edge(49+150j, 1j, 50+149j, 1, pos), -1j
            if drctn == -1:
                return map_edge(150j, 1j, 50, 1, pos), 1j
            if drctn == 1j:
                return map_edge(199j, 1, 100, 1, pos), 1j
        if cur_face == 4:
            if drctn == -1:
                return map_edge(100j, 1j, 50+49j, -1j, pos), 1
            if drctn == -1j:
                return map_edge(49+100j, -1, 50+99j, -1j, pos), 1
        if cur_face == 5:
            if drctn == 1:
                return map_edge(149+49j, -1j, 99+100j, 1j, pos), -1
            if drctn == 1j:
                return map_edge(100+49j, 1, 99+50j, 1j, pos), -1
            if drctn == -1j:
                return map_edge(100, 1, 199j, 1, pos), -1j
        assert False


def move_pos_cube(cur: complex, drctn: complex, amt: int, walls: Set[complex], example: bool) -> Tuple[complex, complex]:
    nxt = cur, drctn
    for _ in range(amt):
        p, d = cube_wrap(*nxt, example)
        if p in walls:
            return nxt
        nxt = p, d
    return nxt


class Day(Day2022):
    @property
    def num(self) -> int:
        return 22

    def get_data(self, example=False) -> Tuple[Set[complex], Set[complex], List[complex]]:
        fulltxt = self.get_raw_data(example)
        grid_str, mvmnt_str = tuple(fulltxt.split('\n\n'))
        grid = set()
        walls = set()
        for y, row in enumerate(grid_str.split('\n')):
            for x, c in enumerate(row):
                if c == '#':
                    grid.add(x + y*1j)
                    walls.add(x + y*1j)
                elif c == '.':
                    grid.add(x + y*1j)

        mvmnt = [0]
        for c in mvmnt_str:
            if c in '1234567890':
                mvmnt[-1] = 10 * mvmnt[-1] + int(c)
            elif c == 'L':
                mvmnt.extend([-1j, 0])  # Opposite because down is positive
            elif c == 'R':
                mvmnt.extend([1j, 0])

        return grid, walls, mvmnt

    def puzzle1(self):
        grid, walls, movement = self.get_data()
        pos = get_start(grid)
        drctn = 1 + 0j
        for move in movement:
            if move.imag != 0:
                drctn *= move
            else:
                pos = move_pos(pos, drctn, int(move.real), grid, walls)
        row = int(pos.imag) + 1
        col = int(pos.real) + 1
        fac = DIRECTION_SCORE[drctn]
        print(1000 * row + 4 * col + fac)

    def puzzle2(self):
        ex = False
        grid, walls, movement = self.get_data(ex)
        pos = get_start(grid)
        drctn = 1 + 0j
        print(f'Start at {pos}, {drctn}')
        for move in movement:
            if move.imag != 0:
                drctn *= move
            else:
                pos, drctn = move_pos_cube(pos, drctn, int(move.real), walls, ex)
            print(f'Move of {move} puts us at {pos}, {drctn}')
        row = int(pos.imag) + 1
        col = int(pos.real) + 1
        fac = DIRECTION_SCORE[drctn]
        print(row, col, fac)
        print(1000 * row + 4 * col + fac)
