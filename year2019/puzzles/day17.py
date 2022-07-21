from typing import *
from year2019.day2019 import Day2019
from year2019.intcode import Intcode
import numpy as np
from scipy.signal import correlate


CHR_TO_INT = {'.': -1, '#': 0, '^': 1, '>': 2, 'v': 3, '<': 4}
INT_TO_CHR = {-1: '.', 0: '#', 1: '^', 2: '>', 3: 'v', 4: '<'}


def get_map(intcode):
    map = [[]]
    while intcode.run_until_io():
        out = chr(intcode.outputs.pop())
        if out == '\n':
            map.append([])
        else:
            map[-1].append(CHR_TO_INT[out])
    map = [r for r in map if len(r) > 0]
    # print(', '.join(str(len(r)) for r in map))
    return np.array(map)


def print_map(map):
    for row in map:
        print(''.join(INT_TO_CHR[i] for i in row))
    print()


class Day(Day2019):
    @property
    def num(self) -> int:
        return 17

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        return Intcode([int(i) for i in lines[0].split(',')])

    def puzzles(self):
        intcode = self.get_data()
        start_map = get_map(intcode)
        # print_map(start_map)

        scaffold = start_map > -1
        print_map(start_map)
        kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        intersections = np.where(correlate(scaffold, kernel, mode='same') == 5)
        alignment_params = np.array(intersections).prod(axis=0)
        print(f'Sum of APs is: {np.sum(alignment_params)}\n')

        intcode = self.get_data()
        intcode.code[0] = 2
        inp = (
                'A,B,A,B,A,C,B,C,A,C\n'
                'L,10,L,12,R,6\n'
                'R,10,L,4,L,4,L,12\n'
                'L,10,R,10,R,6,L,4\n'
                'n\n'
              )[::-1]
        intcode.inputs = [ord(c) for c in inp]
        intcode.run()
        out = ''.join(chr(c) for c in intcode.outputs[:-1])
        print(out)
        print(intcode.outputs[-1])
