from year2025.day2025 import Day2025


class Day(Day2025):
    @property
    def num(self) -> int:
        return 7

    def get_data(self, example=False):
        lines = super().get_data(example)
        start = -1j
        splitters = set()
        for i, line in enumerate(lines):
            for j, space in enumerate(line):
                if space == 'S':
                    start = j + i * 1j
                elif space == '^':
                    splitters.add(j + i * 1j)
        return start, splitters, len(lines)

    def puzzle1(self):
        start, splitters, nlines = self.get_data()
        beams = {start}
        nsplits = 0
        for line in range(nlines):
            beams = {beam + 1j for beam in beams}
            split_beams = beams.intersection(splitters)
            beams.difference_update(split_beams)
            for beam in split_beams:
                beams.add(beam + 1)
                beams.add(beam - 1)
                nsplits += 1
        print(nsplits)

    def puzzle2(self):
        start, splitters, nlines = self.get_data()
        beams = {start: 1}
        for line in range(nlines):
            beams = {beam + 1j: amt for beam, amt in beams.items()}
            split_beams = splitters.intersection(beams.keys())
            for beam in split_beams:
                beams[beam + 1] = beams.get(beam + 1, 0) + beams[beam]
                beams[beam - 1] = beams.get(beam - 1, 0) + beams[beam]
                del beams[beam]
        print(sum(beams.values()))


def one_line():
    pass
