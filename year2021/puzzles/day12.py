from year2021.day2021 import Day2021
import networkx as nx
from string import ascii_lowercase


def get_paths(g, start, seen=(), got_repeat=False):
    # print(f'Counting paths from {start} having passed through {seen}')
    if start == 'end':
        return 1
    if (start == 'start' and len(seen) > 0) or (got_repeat and start[0] in ascii_lowercase and start in seen):
        return 0
    total = 0
    for n in g[start]:
        total += get_paths(g, n, seen + (start, ), got_repeat or (start[0] in ascii_lowercase and start in seen))
    return total


class Day(Day2021):
    @property
    def num(self) -> int:
        return 12

    def get_data(self, example=False):
        lines = super().get_data(example)
        g = nx.Graph()
        for line in lines:
            splt = line.split('-')
            g.add_edge(splt[0], splt[1])
        return g

    def puzzle1(self):
        g = self.get_data()
        print(get_paths(g, 'start', got_repeat=True))

    def puzzle2(self):
        g = self.get_data()
        print(get_paths(g, 'start'))
