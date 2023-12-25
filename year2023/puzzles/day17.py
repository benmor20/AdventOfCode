import itertools

from year2023.day2023 import Day2023
from typing import *
import networkx as nx


def print_path(data, path, nrows, ncols):
    for row in range(nrows):
        for col in range(ncols):
            pos = row + col * 1j
            try:
                _, _, drctn = next(n for n in path if n[0] == pos)
                c = '>'
                if drctn == 1:
                    c = 'v'
                elif drctn == -1:
                    c = '^'
                elif drctn == -1j:
                    c = '<'
                print(c, end='')
            except:
                print(data[pos], end='')
        print()


def make_graph(data, nrows, ncols, part2: bool = False):
    graph = nx.DiGraph()
    poss_lens = range(10) if part2 else range(3)
    graph.add_nodes_from((r + c * 1j, s, d) for r, c, s, d in
                         itertools.product(range(nrows), range(ncols), poss_lens, (1, -1, 1j, -1j)) if
                         r != 0 or c != 0 or (s == 0 and d == 1j))
    for node in graph:
        pos, nstraight, drctn = node
        for new_drctn in (1, -1, 1j, -1j):
            if new_drctn == -drctn or (new_drctn != drctn and nstraight < 3):
                continue
            new_pos = pos + new_drctn
            new_straight = (nstraight + 1) if new_drctn == drctn else 0
            new_node = new_pos, new_straight, new_drctn
            if new_node in graph:
                graph.add_weighted_edges_from([(node, new_node, data[new_pos])])
    return graph


def num_in_line(dists, current):
    res = 0
    prev = dists[current][1]
    if prev is None:
        return 1
    drctn = current - prev
    new_drctn = drctn
    while new_drctn == drctn:
        res += 1
        current = prev
        prev = dists[current][1]
        if prev is None:
            break
        new_drctn = current - prev
    return res


class Day(Day2023):
    @property
    def num(self) -> int:
        return 17

    def get_data(self, example=False):
        lines = super().get_data(example)
        nrows = len(lines)
        ncols = len(lines[0])
        data = {r + c * 1j: int(lines[r][c]) for r, c in itertools.product(range(nrows), range(ncols))}
        nrows = len(lines)
        ncols = len(lines[0])
        return data, nrows, ncols

    def puzzle1(self):
        return
        data, nrows, ncols = self.get_data()
        graph = make_graph(data, nrows, ncols)
        min_heat = -1
        for nstraight, drctn in itertools.product(range(3), (1, -1, 1j, -1j)):
            pos = (nrows - 1) + (ncols - 1) * 1j
            node = pos, nstraight, drctn
            assert node in graph
            try:
                path = nx.shortest_path(graph, (0, 0, 1j), node, 'weight')
                heat_to_pos = sum(data[pos] for pos, _, _ in path[1:])
                if min_heat == -1 or heat_to_pos < min_heat:
                    min_heat = heat_to_pos
                # print_path(data, path, nrows, ncols)
                # print(heat_to_pos)
                # print()
            except nx.exception.NetworkXNoPath:
                pass
        print(min_heat)

    def puzzle2(self):
        data, nrows, ncols = self.get_data(2)

        graph = nx.DiGraph()
        graph.add_nodes_from(r + c * 1j for r, c in itertools.product(range(nrows), range(ncols)))
        for node in graph:
            for drctn in (1, -1, 1j, -1j):
                nxt = node + drctn
                if nxt not in graph:
                    continue
                graph.add_edge(node, nxt, weight=data[nxt])

        src = 0
        dst = nrows + ncols * 1j - 1 - 1j
        print(f'{src = } {dst = }')
        unvisited = set(graph.nodes)
        dists = {src: (0, None)}
        current_node = src
        while current_node != dst:
            print(f'{current_node = }')
            neighbors = graph.neighbors(current_node)
            for neighbor in neighbors:
                print(f'{neighbor = }')
                if neighbor not in unvisited:
                    print('Visited')
                    continue
                if dists[current_node][1] is not None and neighbor - current_node != current_node - dists[current_node][1]:
                    len_pushed = num_in_line(dists, current_node)
                    if len_pushed < 1 or len_pushed > 10:
                        print(f'Didnt push far enough: {len_pushed}')
                        print(dists)
                        continue
                if neighbor == dst:
                    dists[neighbor] = (0, current_node)
                    len_pushed = num_in_line(dists, neighbor)
                    del dists[neighbor]
                    if len_pushed < 4 or len_pushed > 10:
                        continue
                new_dist = dists[current_node][0] + graph[current_node][neighbor]['weight']
                if neighbor not in dists or dists[neighbor][0] > new_dist:
                    print(f'Setting {neighbor} to {new_dist}, {current_node}')
                    dists[neighbor] = new_dist, current_node
                else:
                    print(f'{neighbor}\'s orig dist was {dists[neighbor][0]}, better than {new_dist}')
            unvisited.remove(current_node)
            try:
                current_node = min((node for node in unvisited if node in dists), key=lambda n: dists[n][0])
            except ValueError:
                print('No path found')
                return
        print(dists[dst][0])
        path = []
        node = dst
        while node is not None:
            path.append(node)
            node = dists[node][1]
        path = path[::-1]
        print(path)


def one_line():
    pass
