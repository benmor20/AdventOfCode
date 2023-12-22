import itertools
import re

from year2023.day2023 import Day2023
from typing import *
import numpy as np


def range_overlap(r1: range, r2: range) -> Tuple[Optional[range], List[range]]:
    if r2.stop <= r1.start or r2.start >= r1.stop:
        return None, [r1]
    if r2.start <= r1.start < r1.stop <= r2.stop:
        return r1, []
    if r2.start <= r1.start < r2.stop <= r1.stop:
        overlap, rem = range(r1.start, r2.stop), [range(r2.stop, r1.stop)]
        return overlap, rem
    if r1.start <= r2.start < r2.stop < r1.stop:
        overlap, rem = r2, [range(r1.start, r2.start), range(r2.stop, r1.stop)]
        return overlap, rem
    if r1.start <= r2.start < r1.stop <= r2.stop:
        overlap, rem = range(r2.start, r1.stop), [range(r1.start, r2.start)]
        return overlap, rem
    assert False


Block = Tuple[range, range, range]


def do_blocks_overlap(b1: Block, b2: Block):
    return all(range_overlap(r1, r2)[0] is not None for r1, r2 in zip(b1, b2))


def drop(block: Block, settled: List[Block], check_idxs: Optional[Set[int]] = None, verbose = False) -> Block:
    if verbose: print(f'Dropping {block} with {check_idxs = }')
    if check_idxs is None:
        check_idxs = set(range(len(settled)))
    if block[2].start <= 0:
        if verbose: print(f'Started on ground, returning')
        return block
    max_height = 0
    max_block = None
    for idx in check_idxs:
        if idx >= len(settled):
            continue
        set_block = settled[idx]
        if set_block[2].start >= block[2].stop:
            continue
        if do_blocks_overlap(block[:-1], set_block[:-1]) and max_height < set_block[2].stop:
            max_height = set_block[2].stop
            max_block = set_block
    drop_dist = block[2].start - max_height
    if verbose: print(f'Max height is {max_height} (from {max_block}), drop dist is {drop_dist}')
    assert drop_dist >= 0
    return block[0], block[1], range(block[2].start - drop_dist, block[2].stop - drop_dist)


class Day(Day2023):
    @property
    def num(self) -> int:
        return 22

    def get_data(self, example=False) -> List[Block]:
        lines = super().get_data(example)
        data = []
        for line in lines:
            match = re.fullmatch(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line)
            assert all(int(match.group(i)) <= int(match.group(i + 3)) for i in range(1, 4))
            data.append(tuple(range(int(match.group(i)), int(match.group(i + 3)) + 1) for i in range(1, 4)))
        return data

    def puzzle1(self):
        return
        data: List[Block] = self.get_data()
        data = sorted(data, key=lambda d: d[2].start)

        relevant_idxs = [
            set(
                i2
                for i2, b2 in enumerate(data)
                if i1 != i2 and do_blocks_overlap(b1[:-1], b2[:-1])
            ) for i1, b1 in enumerate(data)
        ]
        assert all(i not in relevant_idxs[i] for i in range(len(relevant_idxs)))
        print('Got relevant idxs')

        settled = []
        for block, idxs in zip(data, relevant_idxs):
            settled.append(drop(block, settled, idxs))
        print('Done settling')

        load_bearing = 0
        for disint_idx in range(len(settled)):
            # print(f'Disintegrating {disint_idx}')
            for fall_idx in relevant_idxs[disint_idx]:
                fall_block = settled[fall_idx]
                idxs = relevant_idxs[fall_idx] - {disint_idx}
                dropped = drop(fall_block, settled, idxs)
                if dropped != fall_block:
                    # print(f'{disint_idx} is load bearing on block {fall_idx}')
                    load_bearing += 1
        print(load_bearing)

    def puzzle2(self):
        data: List[Block] = self.get_data()
        data = sorted(data, key=lambda d: d[2].start)

        relevant_idxs_below = [
            set(
                i2
                for i2, b2 in enumerate(data)
                if i1 != i2 and b2[2].stop <= b1[2].start and do_blocks_overlap(b1[:-1], b2[:-1])
            ) for i1, b1 in enumerate(data)
        ]
        relevant_idxs_above = [
            set(
                i2
                for i2, b2 in enumerate(data)
                if i1 != i2 and b2[2].start >= b1[2].stop and do_blocks_overlap(b1[:-1], b2[:-1])
            ) for i1, b1 in enumerate(data)
        ]
        relevant_idxs = [a.union(b) for a, b in zip(relevant_idxs_above, relevant_idxs_below)]
        print('Got relevant idxs')

        settled = []
        for block, idxs in zip(data, relevant_idxs_below):
            settled.append(drop(block, settled, idxs))
        print('Done settling')

        load_bearing = 0
        for block_idx in range(len(settled)):
            print(f'Disintegrating {block_idx}')
            to_disint = [block_idx]
            gone_idxs = set()
            while len(to_disint) > 0:
                disint_idx = to_disint.pop()
                gone_idxs.add(disint_idx)
                # print(f'{disint_idx} fell')
                for fall_idx in relevant_idxs_above[disint_idx]:
                    if fall_idx in gone_idxs:
                        continue
                    fall_block = settled[fall_idx]
                    idxs = relevant_idxs_below[fall_idx] - gone_idxs
                    dropped = drop(fall_block, settled, idxs)
                    if dropped != fall_block:
                        # print(f'{disint_idx} is load bearing on block {fall_idx}')
                        load_bearing += 1
                        to_disint.append(fall_idx)
        print(load_bearing)


def one_line():
    pass
