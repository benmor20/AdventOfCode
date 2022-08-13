from collections import deque
from utils import utils


MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def adjacent_poses(map, pos):
    for move in MOVES:
        adj = utils.add_tuples(pos, move)
        if map[adj] == 0:
            yield adj


def shortest_dist(map, start, end):
    seen = set()
    to_search = deque()
    to_search.append((start, 0))
    while len(to_search) > 0:
        pos, dist = to_search.pop()
        seen.add(pos)
        for adj in adjacent_poses(map, pos):
            if adj == end:
                return dist + 1
            if adj not in seen:
                to_search.appendleft((adj, dist + 1))
    return None
