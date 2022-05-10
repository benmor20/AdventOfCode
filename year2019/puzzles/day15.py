import itertools
from typing import *
from year2019.day2019 import Day2019
from year2019.intcode import Intcode
from collections import defaultdict, Counter
from utils import utils
import networkx as nx
import matplotlib.pyplot as plt


TILE_CHARS = {
    -1: ' ',
    0: '#',
    1: '.',
    2: 'x'
}


def print_tiles(tile_map, pos):
    maxx = max(t[0] for t in tile_map) + 1
    minx = min(t[0] for t in tile_map)
    maxy = max(t[1] for t in tile_map) + 1
    miny = min(t[1] for t in tile_map)
    print()
    for y in range(miny, maxy):
        for x in range(minx, maxx):
            if (x, y) == pos:
                print('D', end='')
            elif (x, y) == (0, 0):
                print('*', end='')
            else:
                print(TILE_CHARS[tile_map[(x, y)]], end='')
        print()
    print()


DIR_MAP = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0)
}


CODE_MAP = {
    (0, -1): 1,
    (0, 1): 2,
    (-1, 0): 3,
    (1, 0): 4
}


DIR_CODES = [1, 2, 3, 4]


def rev_code(code):
    if code == 1:
        return 2
    if code == 2:
        return 1
    if code == 3:
        return 4
    if code == 4:
        return 3
    raise ValueError(f'Unrecognized code: {code}')


def get_ordered_positions(current_pos):
    for code in DIR_CODES:
        yield utils.add_tuples(current_pos, DIR_MAP[code])


def convert_to_graph(tile_map):
    graph = nx.Graph()
    graph.add_nodes_from(n for n, t in tile_map.items() if t > 0)
    for u, v in itertools.combinations(graph, 2):
        diff = utils.tuple_diff(u, v)
        if abs(diff[0]) + abs(diff[1]) == 1:
            graph.add_edge(u, v)
    return graph


class Day(Day2019):
    def __init__(self):
        super().__init__()
        self.intcode = Intcode([99])
        self.tile_map = defaultdict(lambda: -1)
        self.pos = (0, 0)
        self.tile_map[self.pos] = 1
        self.last_dir = -1
        self.times_visited = Counter()
        self.to_revisit = []
        self.state = 'explore'
        self.surroundings = []
        self.path_route = []
        self.o2_location = None
        self.done = False

    @property
    def num(self) -> int:
        return 15

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = [int(i) for i in lines[0].split(',')]
        return data

    def sense(self):
        res = []
        for code in range(1, 5):
            assert not self.intcode.run_until_io()
            self.intcode.inputs.append(code)
            out = self.intcode.run_until_output()
            res.append(1 if out > 0 else 0)
            test_pos = utils.add_tuples(self.pos, DIR_MAP[code])
            self.tile_map[test_pos] = out
            if out > 0:
                if out == 2:
                    self.o2_location = test_pos
                assert not self.intcode.run_until_io()
                self.intcode.inputs.append(rev_code(code))
                assert self.intcode.run_until_output() > 0
        self.surroundings = res

    def think_explore(self):
        num_paths = sum(self.surroundings)
        if num_paths == 1:
            if self.pos != (0, 0):
                if len(self.to_revisit) == 0:
                    self.done = True
                else:
                    g = convert_to_graph(self.tile_map)
                    target = self.to_revisit.pop()
                    print(f'Seeking new location: choosing {target}')
                    self.path_route = nx.shortest_path(g, self.pos, target)[::-1]
                    self.path_route.pop()
                    print(f'Setting route to {self.path_route}')
                    self.state = 'new_location'
            return DIR_CODES[self.surroundings.index(1)]
        if num_paths == 2:
            for i, val in enumerate(self.surroundings):
                if DIR_CODES[i] == rev_code(self.last_dir):
                    continue
                if val == 1:
                    return DIR_CODES[i]
            assert False
        if num_paths in (3, 4):
            viable_moves = [DIR_CODES[i] for i, t in enumerate(self.surroundings) if t == 1
                            and DIR_CODES[i] != rev_code(self.last_dir)]
            print(f'Surroundings are {self.surroundings}, viable moves are {viable_moves}')
            drctn = viable_moves[0]
            other_locations = [utils.add_tuples(self.pos, DIR_MAP[c]) for c in viable_moves[1:]]
            print(f'Adding {other_locations} to PoI')
            self.to_revisit.extend(other_locations)
            print(f'PoI is now {self.to_revisit}')
            return drctn
        assert False

    def think_new_location(self):
        print(f'pos is {self.pos}, route is {self.path_route}')
        assert self.pos == self.path_route.pop()
        drctn = CODE_MAP[utils.tuple_diff(self.path_route[-1], self.pos)]
        if len(self.path_route) == 1:
            self.path_route.pop()
            self.state = 'explore'
        return drctn

    def act(self, drctn):
        assert not self.intcode.run_until_io()
        self.intcode.inputs.append(drctn)
        out = self.intcode.run_until_output()
        assert out > 0
        self.times_visited[self.pos] += 1
        self.pos = utils.add_tuples(self.pos, DIR_MAP[drctn])
        self.last_dir = drctn

    def step(self):
        print_tiles(self.tile_map, self.pos)

        self.sense()
        print(f'State is {self.state}, pos is {self.pos}')
        if self.state == 'explore':
            drctn = self.think_explore()
        elif self.state == 'new_location':
            print(f'Target path is {self.path_route}')
            drctn = self.think_new_location()
        else:
            raise ValueError(f'Unknown state: {self.state}')
        self.act(drctn)
        return self.done

    def puzzles(self):
        self.intcode = Intcode(self.get_data())
        while not self.step():
            pass
        print(f'O2 is at {self.o2_location}')
        print_tiles(self.tile_map, self.pos)
        g = convert_to_graph(self.tile_map)
        num_steps = nx.shortest_path_length(g, (0, 0), self.o2_location)
        print(f'It takes {num_steps} steps to get from the start to the O2')

        max_steps = num_steps
        for node in g:
            if node == self.o2_location or node == (0, 0):
                continue
            num_steps = nx.shortest_path_length(g, node, self.o2_location)
            if num_steps > max_steps:
                max_steps = num_steps
        print(f'It takes {max_steps} minutes for the sector to fill with O2')
