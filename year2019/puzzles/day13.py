from typing import *
from year2019.day2019 import Day2019
from year2019.intcode import Intcode
import numpy as np


def get_input(grid):
    # while True:
    #     inp = input('Enter L to move left, R to move right, or nothing to remain still. ').replace('\n', '')
    #     if len(inp) == 0:
    #         return 0
    #     if inp.lower() == 'l':
    #         return -1
    #     elif inp.lower() == 'r':
    #         return 1
    #     print(f'Invalid input: {inp}')

    ind = np.indices(grid.shape)[0, :, :]
    xball = ind[grid == 4]
    xbounce = ind[grid == 3]
    move = np.sign(xball - xbounce)
    if move == 0:
        print('Staying still')
    else:
        drctn = 'L' if move == -1 else 'R'
        print(f'Moving {drctn}')
    return move


SQUARES = [' ', '#', 'x', '-', 'o']


def print_grid(grid):
    for row in grid.transpose():
        print(''.join(SQUARES[v] for v in row))


def update_grid(intcode, grid, score):
    while True:
        finished = intcode.run_until_io()
        if not finished:
            return grid, score, finished is None
        x = intcode.outputs.pop()
        y = intcode.get_output()
        v = intcode.get_output()
        if x == -1 and y == 0:
            print('Score updated')
            score = v
        else:
            grid[x, y] = v


def step(intcode, grid, score):
    grid, score, end = update_grid(intcode, grid, score)
    print_grid(grid)
    print(f'Your score is {score}.')
    if end:
        print('Game over')
        return grid, score, True
    intcode.give_input(get_input(grid))
    if np.all(grid != 2):
        return grid, score, True
    return grid, score, False


class Day(Day2019):
    @property
    def num(self) -> int:
        return 13

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        return [int(i) for i in lines[0].split(',')]

    def puzzles(self):
        intcode = Intcode(self.get_data())
        counter = 0
        num_blocks = 0
        maxx = -1
        maxy = -1
        while intcode.run_until_io():
            counter += 1
            if counter % 3 == 0:
                if intcode.outputs[-1] == 2:
                    num_blocks += 1
            elif counter % 3 == 1:
                if intcode.outputs[-1] > maxx:
                    maxx = intcode.outputs[-1]
            elif counter % 3 == 2:
                if intcode.outputs[-1] > maxy:
                    maxy = intcode.outputs[-1]
        maxx += 1
        maxy += 1
        print(f'The game starts with {num_blocks} blocks')
        print(f'The game is {maxx} x {maxy}')

        intcode = Intcode(self.get_data())
        intcode[0] = 2
        grid = np.zeros((maxx, maxy), dtype=int)
        score = 0
        while True:
            grid, score, end = step(intcode, grid, score)
            if end:
                break
        print(f'Final score is {score}')
