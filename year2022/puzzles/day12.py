import itertools

from year2022.day2022 import Day2022
import numpy as np
import networkx as nx
from collections import deque


def construct_graph(heights: np.ndarray) -> nx.DiGraph:
    graph = nx.DiGraph()
    for x, y in itertools.product(range(heights.shape[0]), range(heights.shape[1])):
        graph.add_node(x + y*1j)

    for x, y in itertools.product(range(heights.shape[0]), range(heights.shape[1])):
        pos = x+y*1j
        for drctn in (1, -1, 1j, -1j):
            adj = pos + drctn
            newx = int(np.real(adj))
            newy = int(np.imag(adj))
            if newx < 0 or newx >= heights.shape[0] or newy < 0 or newy >= heights.shape[1]:
                continue
            if heights[newx, newy] - heights[x, y] <= 1:
                graph.add_edge(pos, adj)
    return graph


def find_nearest_start(graph, heights, end):
    lens = {end: 0}
    queue = deque()
    queue.append(end)
    while queue:
        node = queue.popleft()
        for neigh in graph[node]:
            if neigh not in lens:
                queue.append(neigh)
                lens[neigh] = lens[node] + 1
                if heights[int(np.real(neigh)), int(np.imag(neigh))] == 0:
                    return lens[neigh]
    assert False


class Day(Day2022):
    @property
    def num(self) -> int:
        return 12

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        start = -1-1j
        end = -1-1j
        for i1, line in enumerate(lines):
            row = []
            for i2, c in enumerate(line):
                if c == 'S':
                    row.append(0)
                    start = i1 + i2*1j
                elif c == 'E':
                    row.append(25)
                    end = i1 + i2*1j
                else:
                    row.append(ord(c) - ord('a'))
            data.append(row)
        return np.array(data), start, end

    def puzzle1(self):
        data, start, end = self.get_data()
        graph = construct_graph(data)
        print(len(nx.shortest_path(graph, start, end)) - 1)

    def puzzle2(self):
        data, start, end = self.get_data()
        graph = construct_graph(data).reverse()
        dist = find_nearest_start(graph, data, end)
        print(dist)
