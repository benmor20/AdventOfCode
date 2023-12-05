from year2023.day2023 import Day2023
from typing import *
import re


def range_overlap(r1: range, r2: range) -> Tuple[Optional[range], List[range]]:
    # print(f'Overlap {r1} {r2}')
    if r2.stop <= r1.start or r2.start >= r1.stop:
        # print(f'No overlap: None, {[r1]}')
        return None, [r1]
    if r2.start <= r1.start < r1.stop <= r2.stop:
        # print(f'Entirely overlapped: {r1}, []')
        return r1, []
    if r2.start <= r1.start < r2.stop <= r1.stop:
        overlap, rem = range(r1.start, r2.stop), [range(r2.stop, r1.stop)]
        # print(f'Beginning overlap: {overlap}, {rem}')
        return overlap, rem
    if r1.start <= r2.start < r2.stop < r1.stop:
        overlap, rem = r2, [range(r1.start, r2.start), range(r2.stop, r1.stop)]
        # print(f'Middle overlap: {overlap}, {rem}')
        return overlap, rem
    if r1.start <= r2.start < r1.stop <= r2.stop:
        overlap, rem = range(r2.start, r1.stop), [range(r1.start, r2.start)]
        # print(f'End overlap: {overlap}, {rem}')
        return overlap, rem
    assert False


class Day(Day2023):
    @property
    def num(self) -> int:
        return 5

    def get_data(self, example=False):
        text = super().get_raw_data(example)
        sections = text.split('\n\n')
        seeds = [int(i) for i in re.findall(r'\d+', sections[0])]
        data = []
        for section in sections[1:]:
            data.append([tuple(int(i) for i in re.findall(r'\d+', line)) for line in section.split('\n')[1:]])
        return seeds, data

    def puzzle1(self):
        seeds, maps = self.get_data()
        for mappings in maps:
            new_seeds = []
            for seed in seeds:
                found_map = False
                for dest, src, rng in mappings:
                    if src <= seed < src + rng:
                        new_seeds.append(dest + seed - src)
                        found_map = True
                        break
                if not found_map:
                    new_seeds.append(seed)
            seeds = new_seeds
        print(min(seeds))

    def puzzle2(self):
        seeds, maps = self.get_data()
        ranges = []
        for idx in range(0, len(seeds), 2):
            ranges.append(range(seeds[idx], seeds[idx] + seeds[idx + 1]))
        for idx, mappings in enumerate(maps):
            # print(f'\n{idx}: {mappings}')
            new_ranges = []
            for rng in ranges:
                # print(rng)
                rem_rngs = {rng}
                for dest, src, ln in mappings:
                    # print(f'Attempting mapping {dest}, {src}, {ln}')
                    adj_amt = dest - src
                    src_range = range(src, src + ln)
                    new_rem = set()
                    for rem_rng in rem_rngs:
                        overlap, rem = range_overlap(rem_rng, src_range)
                        new_rem.update(set(rem))
                        if overlap is not None:
                            adj_range = range(overlap.start + adj_amt, overlap.stop + adj_amt)
                            # print(f'Found overlap with {src_range}. Adjusting to {range(dest, dest + ln)} to get {adj_range}')
                            new_ranges.append(adj_range)
                    rem_rngs = new_rem
                    # print(f'Remaining ranges: {rem_rngs}')
                new_ranges.extend(rem_rngs)
                # print(f'New ranges is now {new_ranges}')
            ranges = new_ranges
            # print(f'Ranges is now {ranges}')
        print(min(r.start for r in ranges))


def one_line():
    pass
