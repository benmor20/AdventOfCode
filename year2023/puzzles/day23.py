import itertools

from year2023.day2023 import Day2023
from typing import *
import networkx as nx
import numpy as np
from scipy.signal import correlate2d
from matplotlib import pyplot as plt


DIRECTIONS = {
    '>': [1j],
    '<': [-1j],
    'v': [1],
    '^': [-1],
    '.': [1, -1, 1j, -1j]
}


class Day(Day2023):
    @property
    def num(self) -> int:
        return 23

    def get_data(self, example=False):
        lines = super().get_data(example)
        # graph = nx.DiGraph()
        # nrows = len(lines)
        # ncols = len(lines[0])
        # graph.add_nodes_from(r + c * 1j for r, c in itertools.product(range(nrows), range(ncols)) if lines[r][c] != '#')
        # start = -1
        # end = -1
        # for row, line in enumerate(lines):
        #     for col, c in enumerate(line):
        #         if c == '#':
        #             continue
        #         pos = row + col * 1j
        #         if row == 0:
        #             assert start == -1
        #             start = pos
        #         if row == nrows - 1:
        #             assert end == -1
        #             end = pos
        #         for drctn in DIRECTIONS['.']:
        #             new_pos = pos + drctn
        #             if new_pos in graph:
        #                 graph.add_edge(pos, new_pos)
        # assert start != -1
        # assert end != -1
        # return graph, start, end
        return np.array([[0 if c == '#' else 1 for c in l] for l in lines])

    def puzzle1(self):
        return
        graph, start, end = self.get_data()  # uses the commented out get_data cause I didnt expect them to remove the slopes
        paths = nx.all_simple_paths(graph, start, end)
        maxlen = max(len(p) for p in paths)
        print(maxlen - 1)

    def puzzle2(self):
        data = self.get_data()
        start = np.argmax(data[0, :]) * 1j
        end = data.shape[0] - 1 + np.argmax(data[-1, :]) * 1j
        print(start, end)
        kernel = np.array([[0, 1, 0], [1, 5, 1], [0, 1, 0]])
        nadj = correlate2d(data, kernel, mode='same')
        intersections = nadj > 7
        graph = nx.Graph()
        graph.add_nodes_from(r + c * 1j for r, c in itertools.product(range(data.shape[0]), range(data.shape[1])) if intersections[r, c])
        graph.add_nodes_from([start, end])

        accounted_for = set()
        for start_node in graph:
            for orig_drctn in (1, -1, 1j, -1j):
                if (start_node, orig_drctn) in accounted_for:
                    # print(f'{start_node}, {orig_drctn} is accounted for')
                    continue
                accounted_for.add((start_node, orig_drctn))
                new_pos = start_node + orig_drctn
                row = int(new_pos.real)
                col = int(new_pos.imag)
                if row < 0 or row >= data.shape[0] or col < 0 or col >= data.shape[1] or data[row, col] == 0:
                    continue
                last_move = orig_drctn
                dead_end = False
                path_length = 1
                while new_pos not in graph:
                    new_drctns = [d for d in (1, -1, 1j, -1j) if d != -last_move and data[int((p := new_pos + d).real), int(p.imag)] == 1]
                    if len(new_drctns) == 0:
                        dead_end = True
                        break
                    assert len(new_drctns) == 1
                    new_pos += new_drctns[0]
                    last_move = new_drctns[0]
                    path_length += 1
                if dead_end:
                    # print(f'Moving from {start_node} in direction {orig_drctn} hits a dead end')
                    continue
                graph.add_edge(start_node, new_pos, weight=path_length)
                accounted_for.add((new_pos, -last_move))
        print('Made graph')
        nx.drawing.spring_layout
        nx.draw(graph, with_labels=True, pos={n: (n.real, n.imag) for n in graph})
        plt.show()  # its a square which you can definitely do things with but just running it was faster than figuring that out
        paths = list(nx.all_simple_paths(graph, start, end))
        print(f'Found {len(paths)} paths')
        maxlen = 0
        for i, path in enumerate(paths):
            print(i)
            prev = path[0]
            length = 0
            for nxt in path[1:]:
                length += graph[prev][nxt]['weight']
                prev = nxt
            if length > maxlen:
                maxlen = length
        print(maxlen)


def one_line():
    pass
