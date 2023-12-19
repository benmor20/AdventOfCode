from year2023.day2023 import Day2023
from typing import *
import numpy as np
import re


ORDER = 'xmas'


def find_next_workflow(rules, part):
    for idx, gt, val, nxt in rules:
        check = (lambda v: v > val) if gt == '>' else (lambda v: v < val)
        if check(part[idx]):
            return nxt
    assert False


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


def step(rules, part_map):
    new_part_map = {}
    for part_ranges, workflow in part_map.items():
        # print(f'{part_ranges} is in {workflow} --------------------')
        if workflow in ('A', 'R'):
            new_part_map[part_ranges] = workflow
            continue
        remaining = part_ranges
        for idx, gt, val, nxt in rules[workflow]:
            to_overlap = range(val + 1, 5000) if gt == '>' else range(-100, val)
            overlap, new_remaining = range_overlap(remaining[idx], to_overlap)
            # print(f'Overlap between {remaining[idx]} and {to_overlap} is {overlap} with remainder')
            if overlap is not None:
                new_ranges = list(remaining)
                new_ranges[idx] = overlap
                new_part_map[tuple(new_ranges)] = nxt
                # print(f'Rule {idx, gt, val, nxt} has overlap; sending {tuple(new_ranges)} to {nxt}')
                # print(new_part_map)
            if len(new_remaining) > 0:
                assert len(new_remaining) == 1
                new_rem = list(remaining)
                new_rem[idx] = new_remaining[0]
                remaining = tuple(new_rem)
                # print(f'Rule {idx, gt, val, nxt} has a remainder; continuing with {remaining}')
            else:
                break
    return new_part_map


class Day(Day2023):
    @property
    def num(self) -> int:
        return 19

    def get_data(self, example=False):
        rdata = super().get_raw_data(example)
        rules_str, parts_str = tuple(rdata.split('\n\n'))
        rules = {}
        for rule in rules_str.split('\n'):
            match1 = re.fullmatch(r'([a-z]+)\{([a-zAR\d,:<>]+)}', rule)
            assert match1 is not None
            rule_name = match1.group(1)
            interior = match1.group(2)
            end = False
            checks = []
            for check in interior.split(','):
                assert not end
                if ':' not in check:
                    end = True
                    checks.append((0, '>', 0, check))
                    continue
                match2 = re.fullmatch(r'([xmas])([<>])(\d+):([a-z]+|A|R)', check)
                assert match2 is not None
                checks.append((ORDER.index(match2.group(1)), match2.group(2), int(match2.group(3)), match2.group(4)))
            rules[rule_name] = checks
        parts = []
        for part_str in parts_str.split('\n'):
            match = re.fullmatch(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', part_str)
            parts.append(np.array([int(match.group(i)) for i in range(1, 5)]))
        return rules, parts

    def puzzle1(self):
        rules, parts = self.get_data()
        total = 0
        for part in parts:
            workflow = 'in'
            while workflow not in ('A', 'R'):
                workflow = find_next_workflow(rules[workflow], part)
            if workflow == 'A':
                total += int(np.sum(part))
        print(total)

    def puzzle2(self):
        rules, _ = self.get_data()
        parts_to_flow = {tuple([range(1, 4001)] * 4): 'in'}
        while set(parts_to_flow.values()) != {'A', 'R'}:
            parts_to_flow = step(rules, parts_to_flow)
        total = 0
        for ranges, workflow in parts_to_flow.items():
            if workflow != 'A':
                continue
            prod = 1
            for rng in ranges:
                prod *= rng.stop - rng.start
            total += prod
        print(total)


def one_line():
    pass
