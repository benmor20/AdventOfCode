import itertools
from typing import *
from scipy.signal import correlate2d

from year2020.day2020 import Day2020

import numpy as np
from collections import Counter


def print_tile(tile):
    for row in tile:
        print(''.join('#' if i == 1 else '.' for i in row))
    print()


def convert_from_bin(arr):
    return int(''.join(str(v) for v in arr.reshape(-1)), 2)


def reverse_binary(num):
    bin_str = bin(num)[2:]
    bin_str = ('0' * (10 - len(bin_str))) + bin_str
    return int(bin_str[::-1], 2)


def flatten(lst):
    for ele in lst:
        if isinstance(ele, list) or isinstance(ele, tuple):
            yield from flatten(ele)
        else:
            yield ele


def rot0(edges):
    return edges

def rot90(edges):
    return edges[1], edges[2], edges[3], edges[0]

def rot180(edges):
    return rot90(rot90(edges))

def rot270(edges):
    return rot180(rot90(edges))

def flip_horz(edges):
    return reverse_binary(edges[2]), reverse_binary(edges[1]), reverse_binary(edges[0]), reverse_binary(edges[3])

def flip_vert(edges):
    return flip_horz(rot180(edges))

def flip_diag(edges):
    return flip_horz(rot90(edges))

def flip_diag2(edges):
    return rot90(flip_horz(edges))

D4_EDGES = [rot0, rot90, rot180, rot270, flip_horz, flip_vert, flip_diag, flip_diag2]

def rot0grid(grid):
    return grid

def rot180grid(grid):
    return np.rot90(np.rot90(grid))

def rot270grid(grid):
    return np.rot90(rot180grid(grid))

def flip_horz_grid(grid):
    return np.flip(grid, 0)

def flip_vert_grid(grid):
    return np.flip(grid, 1)

def flip_diag_grid(grid):
    return flip_horz_grid(np.rot90(grid))

def flip_diag2_grid(grid):
    return np.rot90(flip_horz_grid(grid))

D4 = [rot0grid, np.rot90, rot180grid, rot270grid, flip_horz_grid, flip_vert_grid, flip_diag_grid, flip_diag2_grid]


def get_transformed_tile(tiles, tile_info):
    return D4[tile_info[1]](tiles[tile_info[0]])


MONSTER_STR = ("                  # "
               "#    ##    ##    ###"
               " #  #  #  #  #  #   ")
KERNEL = np.array([1 if c == '#' else 0 for c in MONSTER_STR]).reshape((3, -1))


class Day(Day2020):
    @property
    def num(self) -> int:
        return 20

    def get_data(self, example=False):
        tile_strs = '\n'.join(super().get_data(example)).split('\n\n')
        tiles = {}
        for tile_str in tile_strs:
            lines = tile_str.split('\n')
            num = int(lines[0][5:-1])
            lines = lines[1:]
            tile = [[1 if c == '#' else 0 for c in row] for row in lines]
            tiles[num] = np.array(tile)
        return tiles

    def puzzles(self):
        tiles = self.get_data()

        # Convert tiles to 4 binary numbers based on edges
        # The edges can be reversed, so also note those
        # Since can always reverse, give each edge unique id based on lower binary
        tiles_to_bin_edges: Dict[int, Tuple[int, int, int, int]] = {}
        tiles_to_all_edge_nums: Dict[int, Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]] = {}
        tiles_to_min_edge: Dict[int, Tuple[int, int, int, int]] = {}
        edges_to_tiles: Dict[int, List[int]] = {}
        for num, tile in tiles.items():
            default_edges = tuple(convert_from_bin(row) for row in
                                  (tile[0, :], tile[:, -1], tile[-1, :][::-1], tile[:, 0][::-1]))
            tiles_to_bin_edges[num] = default_edges
            tiles_to_all_edge_nums[num] = tuple(zip(list(default_edges), [reverse_binary(e) for e in default_edges]))
            tiles_to_min_edge[num] = set(min(p) for p in tiles_to_all_edge_nums[num])
            for e in tiles_to_all_edge_nums[num]:
                if e[0] in edges_to_tiles:
                    edges_to_tiles[e[0]].append(num)
                    edges_to_tiles[e[1]].append(num)
                else:
                    edges_to_tiles[e[0]] = [num]
                    edges_to_tiles[e[1]] = [num]
        print(edges_to_tiles)

        # Count the number of times each edge appears
        edge_counts = Counter()
        for edges in tiles_to_all_edge_nums.values():
            edge_counts.update([min(e) for e in edges])
        print(edge_counts)
        # These two combined will make the entirety of counter
        # Edges with only one instance must be on the border of the puzzle
        # Rest on the interior
        two_inst = set(v for v, c in edge_counts.items() if c == 2)
        one_inst = set(v for v, c in edge_counts.items() if c == 1)

        # The tiles with two edges that only appear once must be corners
        prod = 1
        corners = []
        for num in tiles:
            if len(tiles_to_min_edge[num] & one_inst) == 2:
                corners.append(num)
                prod *= num
        assert len(corners) == 4
        print(f'Puzzle 1 ans: {prod}\n')

        # Choose first corner to put in top left. Can transform later
        grid_size = int(len(tiles) ** 0.5)
        grid_by_num: List[List[Optional[Tuple[int, int]]]] = [[None] * grid_size for _ in range(grid_size)]
        for i, transform in enumerate(D4_EDGES):
            flipped = transform(tiles_to_bin_edges[corners[0]])
            if flipped[0] in one_inst and flipped[-1] in one_inst:
                grid_by_num[0][0] = (corners[0], i)
                break

        # Place the remaining pieces L-R across the top then down from there
        to_place = set(tiles) - {corners[0]}
        for i, j in itertools.product(range(grid_size), repeat=2):
            if (i, j) == (0, 0):
                continue
            if i == 0:
                prev_num, prev_transform_id = grid_by_num[i][j - 1]
                prev_edge_index = 1
                target_edge_index = 3
            else:
                prev_num, prev_transform_id = grid_by_num[i - 1][j]
                prev_edge_index = 2
                target_edge_index = 0
            prev_edges = D4_EDGES[prev_transform_id](tiles_to_bin_edges[prev_num])
            target_edge = prev_edges[prev_edge_index]

            print(f'Prev is {prev_num} ({"left" if i == 0 else "above"}):')
            print_tile(get_transformed_tile(tiles, (prev_num, prev_transform_id)))
            print(f'Target edge is {target_edge} ({bin(target_edge)})')
            print(f'Possibilities are {edges_to_tiles[target_edge]}')
            tile_id = [i for i in edges_to_tiles[target_edge] if i != prev_num][0]
            print(f'{i, j} goes to {tile_id}')
            to_place.remove(tile_id)
            for trans_id, transform in enumerate(D4_EDGES):
                new_edges = transform(tiles_to_bin_edges[tile_id])
                if reverse_binary(new_edges[target_edge_index]) == target_edge:
                    print(f'{transform.__name__} puts {target_edge} in position {target_edge_index} to match with position {prev_edge_index}')
                    print([bin(e) for e in new_edges])
                    grid_by_num[i][j] = (tile_id, trans_id)
                    break
        print()
        for row in rot0grid(np.array(grid_by_num)[:, :, 0]):
            for info in row:
                print(info, end=' ')
            print()
        print()

        # Create the grid
        grid = np.zeros((grid_size * 8, grid_size * 8))
        for i, j in itertools.product(range(grid_size), repeat=2):
            print(f'Placing {grid_by_num[i][j][0]} at {i, j} with transform {D4[grid_by_num[i][j][1]].__name__}')
            trans_tile = get_transformed_tile(tiles, grid_by_num[i][j])
            if i > 0:
                above_tile = get_transformed_tile(tiles, grid_by_num[i - 1][j])
                assert all(above_tile[-1, :] == trans_tile[0, :])
            if j > 0:
                left_tile = get_transformed_tile(tiles, grid_by_num[i][j - 1])
                assert all(left_tile[:, -1] == trans_tile[:, 0])
            tile_cut = trans_tile[1:-1, 1:-1]
            grid[i*8:i*8+8, j*8:j*8+8] = tile_cut

        # Apply all transforms to the grid and note the number of sea monsters in each
        print_tile(grid)
        print_tile(KERNEL)
        trans_to_monsters = {}
        for transform in D4:
            trans_to_monsters[transform] = np.sum(correlate2d(transform(grid), KERNEL) == np.sum(KERNEL))

        # Number of monsters is the max across the transforms
        num_monsters = max(trans_to_monsters.values())
        print(f'There are {num_monsters} monsters')

        # Assume no overlap between monsters - roughness is number of # in grid minus number of # in monsters
        # Evidently this works (at least for the input I got)
        est_rough = np.sum(grid) - np.sum(KERNEL) * num_monsters
        print(f'Estimated roughness is {est_rough}')
