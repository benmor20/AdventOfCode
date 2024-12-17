from year2024.day2024 import Day2024
import networkx as nx


DIRECTIONS = [1, -1j, -1, 1j]


def walls_to_graph(walls: set[complex], end: complex) -> nx.DiGraph:
    graph = nx.DiGraph()
    botleft = max(walls, key=lambda c: c.real + c.imag)
    for i in range(1, int(botleft.real)):
        for j in range(1, int(botleft.imag)):
            pos = i + j * 1j
            if pos in walls:
                continue
            for idx, drctn in enumerate(DIRECTIONS):
                graph.add_edge((pos, DIRECTIONS[idx - 1]), (pos, drctn), weight=1000)
                graph.add_edge((pos, DIRECTIONS[idx + 1 if idx < len(DIRECTIONS) - 1 else 0]), (pos, drctn), weight=1000)
                adj = pos + drctn
                if adj in walls:
                    continue
                graph.add_edge((pos, drctn), (adj, drctn), weight=1)
    for drctn in DIRECTIONS:
        graph.add_edge((end, drctn), (end, 0), weight=0)
    return graph


def print_path(start: complex, end: complex, walls: set[complex], path: list[tuple[complex, complex]]):
    botleft = max(walls, key=lambda c: c.real + c.imag)
    drctn_map = {p: d for p, d in path}
    drctn_to_char = {1: 'v', -1: '^', -1j: '<', 1j: '>'}
    for i in range(0, int(botleft.real) + 1):
        for j in range(0, int(botleft.imag) + 1):
            pos = i + j * 1j
            if pos in walls:
                print('#', end='')
            elif pos == start:
                print('S', end='')
            elif pos == end:
                print('E', end='')
            elif pos in drctn_map:
                print(drctn_to_char[drctn_map[pos]], end='')
            else:
                print('.', end='')
        print()


class Day(Day2024):
    @property
    def num(self) -> int:
        return 16

    def get_data(self, example=False):
        lines = super().get_data(example)
        start = None
        end = None
        walls = set()
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                pos = i + j * 1j
                if c == 'E':
                    assert end is None
                    end = pos
                elif c == 'S':
                    assert start is None
                    start = pos
                elif c == '#':
                    walls.add(pos)
        return walls, start, end

    def puzzle1(self):
        walls, start, end = self.get_data()
        graph = walls_to_graph(walls, end)
        # path = nx.shortest_path(graph, (start, 1j), (end, 0), weight='weight')
        # print_path(start, end, walls, path)
        length = nx.shortest_path_length(graph, (start, 1j), (end, 0), weight='weight')
        # print(path)
        print(length)

    def puzzle2(self):
        walls, start, end = self.get_data(2)
        graph = walls_to_graph(walls, end)
        paths = nx.all_shortest_paths(graph, (start, 1j), (end, 0), weight='weight')
        # print(paths)
        poses = set()
        for path in paths:
            for node in path:
                poses.add(node[0])
        print(len(poses))


def one_line():
    pass
