import itertools
from typing import *
from year2019.day2019 import Day2019
import numpy as np
from utils import utils, map_utils
from collections import deque


def char_to_int(c):
    if c == '#':
        return -1
    elif c == '.':
        return 0
    elif c == '@':
        return 1
    elif 'a' <= c <= 'z':
        return ord(c) - ord('a') + 2
    elif 'A' <= c <= 'Z':
        return -(ord(c) - ord('A') + 2)
    raise ValueError(f'Unknown character: {c}')


def int_to_char(i):
    if i == -1:
        return '#'
    elif i == 0:
        return '.'
    elif i == 1:
        return '@'
    elif 1 < i <= 27:
        return chr(i - 2 + ord('a'))
    elif -27 <= i < -1:
        return chr(-i - 2 + ord('A'))
    raise ValueError(f'No character corresponding to {i}')


def print_cave(cave):
    for row in cave:
        print(''.join(int_to_char(i) for i in row))
    print()


KERNEL = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
DIST_MEMO = {}
SHORTEST_DIST = 0
KEY_POSES = {}
ALL_KEYS = set()
DOOR_POSES = {}


def get_shortest(cave, start):
    map = cave < 0
    poss_dists = []
    current_shortest = None
    for key in ALL_KEYS:
        dist = map_utils.shortest_dist(map, start, KEY_POSES[key])
        print(f'Dist from start to {int_to_char(key)} is {dist}')
        if dist is not None:
            new_dist = get_shortest_from_key(key, {key}, dist, current_shortest)
            if new_dist is not None:
                poss_dists.append(new_dist)
                current_shortest = new_dist
    return min(poss_dists)


def get_shortest_from_key(last_key, keys, current_dist, current_shortest=None):
    if keys is None:
        keys = set()
    if len(keys) == len(ALL_KEYS):
        print(f'Found route of length {current_dist}')
        return current_dist
    poss_dists = []
    for key in sorted(ALL_KEYS - {last_key}, key=lambda k: (DIST_MEMO[last_key, k][0], len(DIST_MEMO[last_key, k][1]))):
        if key in keys:
            continue
        dist, keys_needed = DIST_MEMO[(last_key, key)]
        true_dist = dist + current_dist
        min_poss = true_dist + SHORTEST_DIST * (len(ALL_KEYS) - len(keys))
        if current_shortest is not None and min_poss >= current_shortest:
            # print(f'Skipping {int_to_char(key)}')
            continue

        # It was experimentally determined that doors do not speed up the routes between keys
        # i.e. if it is possible to get from a to b without any keys, there is no quicker way to do it with keys
        # I am extrapolating that that means exactly one set of keys gives fastest path
        # i.e. if a, b, c gives shortest then neither a, b, d nor d, e, f, g give shortest
        if len(keys_needed - keys) == 0:
            # print(f'Recursing to {int_to_char(key)}')
            keys.add(key)
            new_poss = get_shortest_from_key(key, keys, true_dist, current_shortest)
            keys.remove(key)
            if new_poss is not None:
                poss_dists.append(new_poss)
                current_shortest = new_poss
    if len(poss_dists) == 0:
        return None
    return min(poss_dists)


def populate_poses(cave):
    keyx, keyy = np.where(cave > 1)
    for key_pos in sorted(zip(keyx, keyy), key=lambda p: cave[p]):
        KEY_POSES[cave[key_pos]] = key_pos
        ALL_KEYS.add(cave[key_pos])
    doorx, doory = np.where(cave < -1)
    for door_pos in sorted(zip(doorx, doory), key=lambda p: -cave[p]):
        DOOR_POSES[cave[door_pos]] = door_pos


def dist_and_keys_needed(cave, posa, posb):
    seen = {}
    to_search = deque()
    to_search.append((posa, 0, None))
    map_no_doors = cave == -1
    done = False
    while len(to_search) > 0 and not done:
        pos, dist, prev = to_search.pop()
        seen[pos] = (dist, prev)
        for adj in map_utils.adjacent_poses(map_no_doors, pos):
            if adj == posb:
                seen[posb] = (dist + 1, pos)
                done = True
            if adj in seen:
                continue
            to_search.append((adj, dist + 1, pos))
    if not done:
        return None, []
    keys = set()
    dist, prev = seen[posb]
    while prev != posa:
        if cave[prev] < -1:
            keys.add(-cave[prev])
        _, prev = seen[prev]
    return dist, keys


def populate_dists(cave):
    for keya, keyb in itertools.combinations(KEY_POSES, 2):
        DIST_MEMO[(keya, keyb)] = dist_and_keys_needed(cave, KEY_POSES[keya], KEY_POSES[keyb])
        DIST_MEMO[(keyb, keya)] = DIST_MEMO[(keya, keyb)]
    global SHORTEST_DIST
    SHORTEST_DIST = min(v[0] for v in DIST_MEMO.values())


class Day(Day2019):
    @property
    def num(self) -> int:
        return 18

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            data.append([char_to_int(c) for c in line])
        return np.array(data)

    def puzzles(self):
        cave = self.get_data(5)
        x, y = np.where(cave == 1)
        start = x[0], y[0]
        cave[start] = 0
        populate_poses(cave)
        populate_dists(cave)
        print(f'Shortest path is of length {get_shortest(cave, start)}')
        # x, y = np.where(cave == 1)
        # start = x[0], y[0]
        # print(sorted(get_shortest_to_keys(cave, start).items(), key=lambda pd: pd[1]))
