import networkx as nx
from matplotlib import pyplot as plt

from year2025.day2025 import Day2025


def num_paths_between(graph, start, end):
    return sum(1 for _ in nx.all_simple_paths(graph, start, end))


def num_paths_between_pt2(graph: nx.DiGraph, start: str, end: str, allowed_nodes: set[str]) -> int:
    queue = [start]
    num_paths = {start: 1}
    while len(queue) > 0:
        node = queue.pop()
        for cnxn in graph[node]:
            if cnxn not in allowed_nodes:
                continue
            num_paths[cnxn] = num_paths.get(cnxn, 0) + 1
            queue.append(cnxn)
    return num_paths[end]


def nodes_reachable_from(graph, source) -> set[str]:
    queue = [source]
    nodes = {source}
    while len(queue) > 0:
        node = queue.pop()
        nodes.add(node)
        for cnxn in graph[node]:
            if cnxn not in nodes:
                queue.append(cnxn)
    return nodes


class Day(Day2025):
    @property
    def num(self) -> int:
        return 11

    def get_data(self, example=False):
        lines = super().get_data(example)
        graph = nx.DiGraph()
        for line in lines:
            splt = line.split(": ")
            start, conn_str = splt
            for conn in conn_str.split(" "):
                graph.add_edge(start, conn)
        return graph

    def puzzle1(self):
        graph = self.get_data()
        print(num_paths_between(graph, "you", "out"))

    def puzzle2(self):
        # Already verified - no loops
        # Also already verified - no path from SVR to DAC that doesnt pass thru FFT
        # Only possible path is SVR -> FFT -> DAC -> OUT
        graph = self.get_data()
        inverse = graph.reverse()

        fft_backward = nodes_reachable_from(inverse, "fft")
        dac_backward = nodes_reachable_from(inverse, "dac")
        out_backward = nodes_reachable_from(inverse, "out")

        svr_fft_nodes = fft_backward
        fft_dac_nodes = dac_backward - fft_backward
        dac_out_nodes = out_backward - dac_backward

        svr_to_fft = num_paths_between_pt2(graph, "svr", "fft", svr_fft_nodes)
        fft_to_dac = num_paths_between_pt2(graph, "fft", "dac", fft_dac_nodes)
        dac_to_out = num_paths_between_pt2(graph, "dac", "out", dac_out_nodes)
        total = svr_to_fft * fft_to_dac * dac_to_out
        print(total)


def one_line():
    pass
