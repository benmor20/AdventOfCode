from typing import *
import networkx as nx
from collections import deque
from year2019.day2019 import Day2019


def create_graph(orbits):
    graph = nx.DiGraph()
    for inner, outer in orbits:
        graph.add_edge(inner, outer)
    return graph


def bfs(graph, start, end):
    seen = set()
    todo = deque()
    todo.append((start, 0))
    while len(todo) > 0:
        node, dist = todo.pop()
        seen.add(node)
        if node == end:
            return dist
        todo.extend([(nxt, dist+1) for nxt in set(graph[node]) - seen])
    return -1


def get_depth(graph: nx.DiGraph, obj: str):
    if obj == 'COM':
        return 0
    return get_depth(graph, list(graph.neighbors(obj))[0]) + 1


class Day(Day2019):
    @property
    def num(self) -> int:
        return 6

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = [tuple(l.split(')')) for l in lines]
        return data

    def puzzles(self):
        orbits = self.get_data()
        graph = create_graph(orbits)
        rev_graph = graph.reverse()
        num_orbits = sum(map(lambda o: get_depth(rev_graph, o), graph.nodes))
        print(f'There are {num_orbits} orbits')
        print(f'Dist to Santa is {bfs(graph.to_undirected(), "YOU", "SAN") - 2}')
