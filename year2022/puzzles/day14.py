from year2022.day2022 import Day2022
from collections import deque


def print_layout(walls, settled, falling):
    all_pts = walls.union(settled, falling)
    minx = int(min(p.real for p in all_pts))
    maxx = int(max(p.real for p in all_pts))
    miny = 0
    maxy = int(max(p.imag for p in all_pts))

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            pt = x + y*1j
            if pt in walls:
                print('█', end='')
            elif pt in settled:
                print('o', end='')
            elif pt in falling:
                print('~', end='')
            else:
                print(' ', end='')
        print()


def pts_from_edges(a, b):
    drctn = (b - a) / abs(b - a)
    pt = a
    while pt != b:
        yield pt
        pt += drctn
    yield pt


def pts_from_wall(line_pts):
    prev = line_pts[0]
    for cur in line_pts[1:]:
        yield from pts_from_edges(prev, cur)
        prev = cur


class Day(Day2022):
    @property
    def num(self) -> int:
        return 14

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            ptstrs = line.split(' -> ')
            pts = [tuple(p.split(',')) for p in ptstrs]
            data.append([int(a) + int(b)*1j for a, b in pts])
        return data

    def puzzle1(self):
        data = self.get_data()
        settled_sand = set()
        falling_sand = deque()
        walls = set()

        for line in data:
            walls.update(pts_from_wall(line))
        lowest = max(w.imag for w in walls)

        while True:
            # print_layout(walls, settled_sand, falling_sand)
            num_falling = len(falling_sand)
            abyss = False
            for _ in range(num_falling):
                sand = falling_sand.popleft()
                if sand.imag > lowest:
                    abyss = True
                    break
                settled = True
                for drctn in (1j, -1+1j, 1+1j):
                    new_pos = sand + drctn
                    if new_pos not in walls and new_pos not in settled_sand:
                        settled = False
                        falling_sand.append(new_pos)
                        break
                if settled:
                    settled_sand.add(sand)
            falling_sand.append(500)
            if abyss:
                break
        print(len(settled_sand))

    def puzzle2(self):
        data = self.get_data()
        settled_sand = set()
        falling_sand = deque()
        walls = set()

        for line in data:
            walls.update(pts_from_wall(line))
        lowest = max(w.imag for w in walls)
        floor = lowest + 2

        while True:
            num_falling = len(falling_sand)
            for _ in range(num_falling):
                sand = falling_sand.popleft()
                if sand.imag == floor - 1:
                    settled_sand.add(sand)
                    continue
                settled = True
                for drctn in (1j, -1+1j, 1+1j):
                    new_pos = sand + drctn
                    if new_pos not in walls and new_pos not in settled_sand:
                        settled = False
                        falling_sand.append(new_pos)
                        break
                if settled:
                    settled_sand.add(sand)
            falling_sand.append(500)
            if 500 in settled_sand:
                break
        print(len(settled_sand))
