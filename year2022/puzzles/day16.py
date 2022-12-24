import itertools

from year2022.day2022 import Day2022
import networkx as nx
from typing import *


def to_graph(data: Dict[str, Tuple[int, List[str]]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from([(n, {'rate': r}) for n, (r, _) in data.items()])
    for name, (_, cnxns) in data.items():
        graph.add_edges_from([(name, c, {'dist': 1}) for c in cnxns])
    return graph


def is_condensed(graph) -> bool:
    return all(len(graph[n]) <= 2 for n in graph)


def condense_graph(graph: nx.Graph) -> nx.Graph:
    res = graph.copy()
    for node in graph:
        if res.nodes[node]['rate'] == 0 and len(res[node]) == 2:
            a, b = tuple(res[node])
            new_dist = res[node][a]['dist'] + res[node][b]['dist']
            res.remove_node(node)
            res.add_edge(a, b, dist=new_dist)
    for u, v in itertools.combinations(res, r=2):
        if res.has_edge(u, v):
            continue
        res.add_edge(u, v, dist=nx.shortest_path_length(graph, u, v, 'dist'))
    return res


def path_length(graph: nx.Graph, path: List[str]) -> int:
    prev = path[0]
    total = 0
    for nxt in path[1:]:
        total += graph[prev][nxt]['dist']
        prev = nxt
    return total


def routes(nodes: Set[str], graph: nx.Graph, start: str = 'AA', time_left: int = 26) -> Generator[Tuple[str, ...], None, None]:
    og_nodes = nodes.copy()
    gave_empty = False
    for node in og_nodes:
        time_to_open = graph[start][node]['dist'] + 1
        new_time_left = time_left - time_to_open
        if new_time_left <= 0:
            if not gave_empty:
                yield tuple()
                gave_empty = True
            continue
        nodes.remove(node)
        yield from (tuple([node] + list(p)) for p in routes(nodes, graph, node, new_time_left))
        nodes.add(node)


def paired_routes(graph: nx.Graph) -> Generator[Tuple[Tuple[str, ...], Tuple[str, ...]], None, None]:
    ret = set()
    nodes = set(graph)
    nodes.remove('AA')
    for rte in routes(nodes, graph):
        for rte2 in routes(nodes - set(rte), graph):
            if (rte, rte2) in ret:
                continue
            # print(rte, rte2)
            yield rte, rte2
            ret.add((rte, rte2))


def flow_from_routes(graph: nx.Graph, *rtes: Tuple[str, ...]) -> int:
    if len(rtes) == 1:
        rte = rtes[0]
        flow = 0
        rate = 0
        prev = 'AA'
        time = 0
        for cave in rte:
            dist = graph[prev][cave]['dist']
            time += dist + 1
            flow += rate * (dist + 1)
            rate += graph.nodes[cave]['rate']
            prev = cave
        assert time <= 26
        return flow + rate * (26 - time)
    return sum(flow_from_routes(graph, r) for r in rtes)


def max_flow(graph: nx.Graph, current_pos: str, min_elapsed: int, open_valves: Set[str]) -> Tuple[int, List[Tuple[str, int]]]:
    current_flow = sum(graph.nodes[v]['rate'] for v in open_valves)
    if min_elapsed >= 30:
        return 0, []
    if min_elapsed == 29:
        return current_flow, []
    possible_flows = {}
    for node in set(graph) - open_valves:
        if graph.nodes[node]['rate'] == 0:
            continue
        shortest_path = nx.dijkstra_path(graph, current_pos, node, 'dist')
        length = path_length(graph, shortest_path)
        nxt_time = min_elapsed + length + 1
        if nxt_time > 29:
            continue
        open_valves.add(node)
        flow, path = max_flow(graph, node, min_elapsed + length + 1, open_valves)
        open_valves.remove(node)
        flow += current_flow * (length + 1)
        path.append((current_pos, min_elapsed))
        possible_flows[node] = (flow, path)
    # print(f'At {current_pos} after {min_elapsed} mins, valves {open_valves} are open. Possible flows are {possible_flows}')
    if len(possible_flows) == 0:
        return current_flow * (30 - min_elapsed), []
    best_flow, best_path = max(possible_flows.values(), key=lambda f: f[0])
    return best_flow, best_path


class Day(Day2022):
    @property
    def num(self) -> int:
        return 16

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = {}
        for line in lines:
            rate_str, connect_str = tuple(line.split('; '))
            name = rate_str[6:8]
            rate = int(rate_str.split('=')[-1])
            cnxns = [c[-2:] for c in connect_str.split(', ')]
            data[name] = (rate, cnxns)
        return data

    def puzzle1(self):
        data = self.get_data()
        # print(data)
        graph = to_graph(data)
        condensed = condense_graph(graph)
        print(f'Graph is condensed from {len(graph)} nodes to {len(condensed)} nodes')
        # nx.draw(condensed)
        # plt.show()
        # flow, path = max_flow(condensed, 'AA', 0, set())
        # path = path[::-1]
        # print(flow)
        # print(path)

    def puzzle2(self):
        data = self.get_data()
        graph = condense_graph(to_graph(data))
        assert all(graph.nodes[n]['rate'] > 0 or n == 'AA' for n in graph)
        print('Graph made')
        max_flow = 0
        max_rtes = None
        for i, rtes in enumerate(paired_routes(graph)):
            flow = flow_from_routes(graph, *rtes)
            # print(f'Done with {i+1}/?: {rtes} -> {flow}')
            if flow > max_flow:
                print(f'Found better flow of {flow}')
                max_flow = flow
                max_rtes = rtes
        print(max_flow)
        print(max_rtes)
