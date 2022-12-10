import itertools

import numpy as np

from year2022.day2022 import Day2022


class CPU:
    def __init__(self):
        self.cycle = 0
        self.X = 1
        self._started_addx = False
        self.Xvals = []
        self.data = None
        self.index = -1

    def set_data(self, data):
        self.data = data
        self.index = 0

    def loop(self):
        self.cycle += 1
        self.Xvals.append(self.X)
        instr, num = self.data[self.index]
        if instr == 'noop':
            self.index += 1
        elif self._started_addx:
            self.X += num
            self.index += 1
            self._started_addx = False
        else:
            self._started_addx = True

    def run(self):
        while self.index < len(self.data):
            self.loop()


class Day(Day2022):
    @property
    def num(self) -> int:
        return 10

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            if line == 'noop':
                data.append((line, -1))
            else:
                splt = line.split(' ')
                data.append((splt[0], int(splt[1])))
        return data

    def puzzle1(self):
        data = self.get_data()
        cpu = CPU()
        cpu.set_data(data)
        cpu.run()
        print(sum(i * cpu.Xvals[i] for i in range(20, 221, 40)))

    def puzzle2(self):
        data = self.get_data()
        cpu = CPU()
        cpu.set_data(data)
        cpu.run()

        res = np.zeros((6, 40), dtype=bool)
        for cycle, X in enumerate(cpu.Xvals):
            row, pos = divmod(cycle, 40)
            res[row, pos] = abs(pos - X) <= 1

        print('\n'.join(''.join('#' if v else '.' for v in row) for row in res))
