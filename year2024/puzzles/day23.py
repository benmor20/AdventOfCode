from year2024.day2024 import Day2024
import networkx as nx


class Day(Day2024):
    @property
    def num(self) -> int:
        return 23

    def get_data(self, example=False):
        lines = super().get_data(example)
        graph = nx.Graph()
        for line in lines:
            graph.add_edge(*line.split('-'))
        return graph

    def puzzle1(self):
        graph = self.get_data()
        subgraphs = set()
        for node in graph:
            for neighbor in graph[node]:
                for nxt in graph[neighbor]:
                    if nxt == node or nxt not in graph[node]:
                        continue
                    subgraph = tuple(sorted((node, neighbor, nxt)))
                    subgraphs.add(subgraph)
        print(sum(1 for subgraph in subgraphs if any(node.startswith('t') for node in subgraph)))

    def puzzle2(self):
        print(','.join(sorted(max(nx.find_cliques(self.get_data()), key=len))))


def one_line():
    pass
