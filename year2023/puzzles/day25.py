from year2023.day2023 import Day2023
from typing import *
import networkx as nx
import re
from matplotlib import pyplot as plt


class Day(Day2023):
    @property
    def num(self) -> int:
        return 25

    def get_data(self, example=False):
        lines = super().get_data(example)
        graph = nx.Graph()
        for line in lines:
            match = re.fullmatch(r'([a-z]+): ([a-z ]+)', line)
            assert match is not None
            start = match.group(1)
            graph.add_edges_from((start, n) for n in match.group(2).split(' '))
        return graph

    def puzzle1(self):
        graph = self.get_data()
        print(len(graph.edges))
        to_remove = nx.minimum_edge_cut(graph)
        for edge in to_remove:
            graph.remove_edge(*edge)
        c1, c2 = nx.connected_components(graph)
        print(len(c1) * len(c2))

    def puzzle2(self):
        # Push the big red button!
        pass


def one_line():
    pass
