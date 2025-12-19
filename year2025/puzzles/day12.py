import re

import numpy as np

from year2025.day2025 import Day2025


class Day(Day2025):
    @property
    def num(self) -> int:
        return 12

    def get_data(self, example=False):
        all_text = super().get_raw_data(example)
        sections = all_text.strip().split("\n\n")

        region_sizes = []
        region_presents = []
        for line in sections[-1].split("\n"):
            line = line.strip()
            match = re.fullmatch(r"(\d+)x(\d+): (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)", line)
            assert match is not None, line
            region_sizes.append((int(match.group(1)), int(match.group(2))))
            region_presents.append([int(match.group(idx)) for idx in range(3, 9)])

        present_shapes = []
        for section in sections[:-1]:
            present = []
            for line in section.split("\n")[1:]:
                present.append([c == '#' for c in line.strip()])
            present_shapes.append(present)

        return present_shapes, region_sizes, region_presents

    def puzzle1(self):
        present_shapes, region_sizes, region_presents = self.get_data()
        present_amts = np.array([sum(sum(l) for l in p) for p in present_shapes])
        assert present_amts.shape == (6,)
        total = 0
        for region_size, num_presents in zip(region_sizes, region_presents):
            area = region_size[0] * region_size[1]
            sqs_needed = np.dot(present_amts, np.array(num_presents))
            if sqs_needed <= area:
                total += 1
        print(total)

    def puzzle2(self):
        data = self.get_data(True)


def one_line():
    pass
