import itertools

from year2023.day2023 import Day2023
from typing import *
import networkx as nx


SYMS_TO_DIRS = {
    '|': [-1 + 0j, 1 + 0j],
    '-': [0 - 1j, 0 + 1j],
    'L': [-1 + 0j, 0 + 1j],
    'J': [-1 + 0j, 0 - 1j],
    '7': [0 - 1j, 1 + 0j],
    'F': [0 + 1j, 1 + 0j],
    'S': [-1 + 0j, 1 + 0j, 0 - 1j, 0 + 1j],
    '.': [],
}


class Day(Day2023):
    @property
    def num(self) -> int:
        return 10

    def get_data(self, example=False):
        lines = super().get_data(example)
        num_rows = len(lines)
        num_cols = len(lines[0])
        graph = nx.DiGraph()
        graph.add_nodes_from(row + col * 1j for row, col in itertools.product(range(num_rows), range(num_cols)))
        start = -1 + 0j
        for row, line in enumerate(lines):
            for col, c in enumerate(line):
                pos = row + col * 1j
                if c == 'S':
                    start = pos
                dirs = SYMS_TO_DIRS[c]
                connections = [pos + d for d in dirs]
                for cxn in connections:
                    if cxn.real < 0 or cxn.real >= num_rows or cxn.imag < 0 or cxn.imag >= num_cols:
                        continue
                    graph.add_edge(pos, cxn)
        return graph, start, lines

    def puzzle1(self):
        digraph, start, _ = self.get_data()
        graph = digraph.to_undirected(True)
        cycles = [c for c in nx.cycle_basis(graph) if start in c]
        assert len(cycles) == 1
        cycle = cycles[0]
        print(len(cycle) // 2)

    def puzzle2(self):
        digraph, start, raw_strs = self.get_data()
        graph = digraph.to_undirected(True)
        cycles = [c for c in nx.cycle_basis(graph) if start in c]
        cycle = cycles[0]
        cycle_set = set(cycle)

        just_loop = []
        nrows = int(max(n.real for n in graph))
        ncols = int(max(n.imag for n in graph))
        for row in range(nrows):
            just_loop_str = ''
            for col in range(ncols):
                pos = row + col * 1j
                if pos == start:
                    just_loop_str += '-'  # specific to my input
                elif pos in cycle_set:
                    just_loop_str += raw_strs[row][col]
                else:
                    just_loop_str += '.'
            just_loop.append(just_loop_str)

        in_loop_cnt = 0
        for row in range(nrows):
            for col in range(ncols):
                if just_loop[row][col] != '.':
                    continue
                cur_col = col - 1
                in_loop = False
                curve_seen = ''
                while cur_col >= 0:
                    c = just_loop[row][cur_col]
                    if c == '|':
                        in_loop = not in_loop
                    elif curve_seen == '7' and c == 'L':
                        in_loop = not in_loop
                        curve_seen = ''
                    elif curve_seen == '7' and c == 'F' or curve_seen == 'J' and c == 'L':
                        curve_seen = ''
                    elif curve_seen == 'J' and c == 'F':
                        in_loop = not in_loop
                        curve_seen = ''
                    elif c in '7J':
                        curve_seen = c
                    cur_col -= 1
                if in_loop:
                    # print(f'{row}, {col} is in the loop')
                    in_loop_cnt += 1
        print(in_loop_cnt)


def one_line():
    pass
