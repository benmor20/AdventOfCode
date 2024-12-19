from year2024.day2024 import Day2024
import networkx as nx


DIRECTIONS = [1, -1j, -1, 1j]


def make_graph(fallen, max_val):
    graph = nx.Graph()
    for i in range(max_val + 1):
        for j in range(max_val + 1):
            pos = i + j * 1j
            if pos in fallen:
                continue
            for drctn in DIRECTIONS:
                adj = pos + drctn
                if adj in fallen:
                    continue
                graph.add_edge(pos, adj)
    return graph


class Day(Day2024):
    @property
    def num(self) -> int:
        return 18

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [int((splt := line.split(','))[0]) + int(splt[1]) * 1j for line in lines]
        return data

    def puzzle1(self):
        example = False
        data = self.get_data(example)
        max_val = 6 if example else 70
        nbytes = 12 if example else 1024
        fallen = set(data[:nbytes])
        graph = make_graph(fallen, max_val)
        print(nx.shortest_path_length(graph, 0, max_val * (1 + 1j)))

    def puzzle2(self):
        example = False
        data = self.get_data(example)
        max_val = 6 if example else 70
        graph = make_graph(set(), max_val)
        for fall in data:
            for neighbor in graph[fall].copy():
                graph.remove_edge(fall, neighbor)
            try:
                nx.shortest_path_length(graph, 0, max_val * (1 + 1j))
            except nx.NetworkXNoPath:
                print(f'{int(fall.real)},{int(fall.imag)}')
                break


def one_line():
    pass
