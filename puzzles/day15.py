from puzzles.daybase import DayBase
import networkx as nx
from heapq import heappush, heappop
import numpy as np


def shortest_path(g, start, end):
    node_info = {}
    heap = [(0, start, None)]
    while len(heap) > 0:
        l, node, prev = heappop(heap)
        for n, info in g[node].items():
            length = l + info['weight']
            if n not in node_info or node_info[n][1] > length:
                node_info[n] = (node, length)
                heappush(heap, (length, n, node))
        if len(node_info) == (end[0] + 1) * (end[1] + 1):
            return node_info[end][1]
    return node_info[end][1]


class Day(DayBase):
    @property
    def num(self) -> int:
        return 15

    def get_data(self, example=False, num=1):
        arr = np.array([[int(i) for i in row] for row in super().get_data(example)])
        if num == 2:
            orig = arr.copy()
            for i in range(1, 5):
                arr = np.concatenate((arr, orig.copy() + i), 1)
            orig = arr.copy()
            for i in range(1, 5):
                arr = np.concatenate((arr, orig.copy() + i))
            arr[arr > 9] -= 9
        g = nx.DiGraph()
        for i, row in enumerate(arr):
            for j, val in enumerate(row):
                if i + 1 < len(arr):
                    g.add_edge((i, j), (i + 1, j), weight=arr[i + 1][j])
                if j + 1 < len(arr[0]):
                    g.add_edge((i, j), (i, j + 1), weight=arr[i][j + 1])
                if i > 0:
                    g.add_edge((i, j), (i - 1, j), weight=arr[i - 1][j])
                if j > 0:
                    g.add_edge((i, j), (i, j - 1), weight=arr[i][j - 1])
        return g, (len(arr), len(arr[0]))

    def puzzle1(self):
        g, size = self.get_data(True)
        end = (size[0] - 1, size[1] - 1)
        print(nx.dijkstra_path_length(g, (0, 0), end))  # only remembered this after :(
        print(shortest_path(g, (0, 0), end))

    def puzzle2(self):
        g, size = self.get_data(False, 2)
        end = (size[0] - 1, size[1] - 1)
        print(nx.dijkstra_path_length(g, (0, 0), end))  # only remembered this after :(
        print(shortest_path(g, (0, 0), (size[0] - 1, size[1] - 1)))
