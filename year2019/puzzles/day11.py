from typing import *
from year2019.day2019 import Day2019
from year2019.intcode import Intcode


def new_pos(old_pos, heading):
    if heading == 0:
        return old_pos[0], old_pos[1] - 1
    elif heading == 90:
        return old_pos[0] + 1, old_pos[1]
    elif heading == 180:
        return old_pos[0], old_pos[1] + 1
    elif heading == 270:
        return old_pos[0] - 1, old_pos[1]
    raise ValueError


class Day(Day2019):
    @property
    def num(self) -> int:
        return 11

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = [int(i) for i in lines[0].split(',')]
        return data

    def puzzles(self):
        intcode = Intcode(self.get_data())
        seen = set()
        white_tiles = set()
        robot_pos = (0, 0)
        white_tiles.add(robot_pos)
        robot_heading = 0
        running = True
        while running:
            seen.add(robot_pos)
            current_color = int(robot_pos in white_tiles)
            intcode.inputs.append(current_color)

            new_color = intcode.run_until_output()
            if new_color is None:
                break
            if current_color and not new_color:
                white_tiles.remove(robot_pos)
            elif not current_color and new_color:
                white_tiles.add(robot_pos)

            drctn = intcode.run_until_output()
            robot_heading += 90 * (1 if drctn else -1)
            if robot_heading < 0:
                robot_heading += 360
            elif robot_heading > 270:
                robot_heading -= 360
            robot_pos = new_pos(robot_pos, robot_heading)
        print(f'Saw {len(seen)} tiles')

        minx = min(t[0] for t in white_tiles)
        maxx = max(t[0] for t in white_tiles) + 1
        miny = min(t[1] for t in white_tiles)
        maxy = max(t[1] for t in white_tiles) + 1
        final = []
        for y in range(miny, maxy):
            row = ''
            for x in range(minx, maxx):
                row += '#' if (x, y) in white_tiles else '.'
            final.append(row)
        print('\n'.join(final))
