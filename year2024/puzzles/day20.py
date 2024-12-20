from collections import Counter

from year2024.day2024 import Day2024


DIRECTIONS = [1, -1j, -1, 1j]


def generate_final_pos(start, max_dist):
    seen = set()
    for dist in range(1, max_dist + 1):
        for real in range(dist + 1):
            imag = dist - real
            for pos in (start + real + 1j * imag, start + real - 1j * imag, start - real + 1j * imag, start - real - 1j * imag):
                if pos not in seen:
                    yield pos, dist
                    seen.add(pos)


class Day(Day2024):
    @property
    def num(self) -> int:
        return 20

    def get_data(self, example=False):
        lines = super().get_data(example)
        start = None
        end = None
        walls = set()
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                pos = i + j * 1j
                if c == '#':
                    walls.add(pos)
                elif c == 'S':
                    assert start is None
                    start = pos
                elif c == 'E':
                    assert end is None
                    end = pos
        return start, end, walls

    def do_puzzle(self, example, max_dist):
        start, end, walls = self.get_data(example)
        dist_to_end = {end: 0}
        pos_to_drctn = {end: 0}
        prev_node = end
        while prev_node != start:
            next_node = None
            for drctn in DIRECTIONS:
                if (adj := prev_node + drctn) not in walls and adj not in dist_to_end:
                    assert next_node is None
                    next_node = adj
            assert next_node is not None
            dist_to_end[next_node] = dist_to_end[prev_node] + 1
            pos_to_drctn[next_node] = prev_node - next_node
            prev_node = next_node
        assert pos_to_drctn[start] + start in pos_to_drctn

        time_save = Counter()
        queue = [start]
        while len(queue) > 0:
            pos = queue.pop()
            if pos != end:
                queue.append(pos + pos_to_drctn[pos])
            for back_on, dist in generate_final_pos(pos, max_dist):
                if back_on not in dist_to_end:
                    continue
                saved = dist_to_end[pos] - dist - dist_to_end[back_on]
                if saved > 0:
                    time_save[saved] += 1
        print(sum(amt for save, amt in time_save.items() if save >= 100))

    def puzzle1(self):
        self.do_puzzle(False, 2)

    def puzzle2(self):
        self.do_puzzle(False, 20)


def one_line():
    pass
