from year2019.puzzles.day14 import Counter
from year2024.day2024 import Day2024


MOVES = {
    '^': -1,
    'v': +1,
    '<': -1j,
    '>': +1j,
}


def step(robot, boxes, walls, move):
    new_pos = robot + move
    if new_pos in walls:
        return robot, boxes
    if new_pos in boxes:
        new_boxes = set(boxes)
        new_boxes.remove(new_pos)
        box_pos = new_pos
        while box_pos in boxes:
            box_pos += move
        if box_pos in walls:
            return robot, boxes
        new_boxes.add(box_pos)
        return new_pos, new_boxes
    return new_pos, boxes


def print_board(robot, boxes, walls):
    size = max(walls, key=lambda p: p.real + p.imag) + 1 + 1j
    for i in range(int(size.real)):
        for j in range(int(size.imag)):
            pos = i + j * 1j
            if pos == robot:
                print('@', end='')
            elif pos in boxes:
                print('O', end='')
            elif pos in walls:
                print('#', end='')
            else:
                print('.', end='')
        print()


def print_board2(robot, boxes, walls):
    size = max(walls, key=lambda p: p.real + p.imag) + 1 + 1j
    for i in range(int(size.real)):
        for j in range(int(size.imag)):
            pos = i + j * 1j
            if pos == robot:
                print('@', end='')
            elif pos in boxes:
                print('[', end='')
            elif pos - 1j in boxes:
                print(']', end='')
            elif pos in walls:
                print('#', end='')
            else:
                print('.', end='')
        print()


def sum_gps(boxes):
    return sum(100 * int(box.real) + int(box.imag) for box in boxes)


def part2_translation(robot, boxes, walls):
    new_robot = robot.real + robot.imag * 2j
    new_walls = set()
    for wall in walls:
        new_walls.add(wall.real + wall.imag * 2j)
        new_walls.add(wall.real + wall.imag * 2j + 1j)
    new_boxes = set(box.real + box.imag * 2j for box in boxes)
    return new_robot, new_boxes, new_walls


def step2(robot, boxes, walls, move):
    new_pos = robot + move
    if new_pos in walls:
        return robot, boxes
    if new_pos not in boxes and new_pos - 1j not in boxes:
        return new_pos, boxes
    box_pos = new_pos if new_pos in boxes else new_pos - 1j
    new_boxes = Counter(boxes)
    new_boxes[box_pos] -= 1
    queue = [box_pos]
    moved = set()
    while len(queue) > 0:
        box_pos = queue.pop()
        if box_pos in moved:
            continue
        moved.add(box_pos)
        new_boxes[box_pos] = max(0, new_boxes[box_pos] - 1)
        new_box = box_pos + move
        new_boxes[new_box] += 1
        if new_box in walls or new_box + 1j in walls:
            return robot, boxes
        if new_box in boxes:
            queue.append(new_box)
        if new_box - 1j in boxes:
            queue.append(new_box - 1j)
        if new_box + 1j in boxes:
            queue.append(new_box + 1j)
    return new_pos, {box for box in new_boxes if new_boxes[box] > 0}


class Day(Day2024):
    @property
    def num(self) -> int:
        return 15

    def get_data(self, example=False):
        lines = super().get_raw_data(example)
        warehouse_str, move_str = lines.split('\n\n')
        robot = None
        boxes = set()
        walls = set()
        for i, row in enumerate(warehouse_str.splitlines()):
            for j, c in enumerate(row):
                pos = i + j * 1j
                if c == '#':
                    walls.add(pos)
                elif c == 'O':
                    boxes.add(pos)
                elif c == '@':
                    assert robot is None
                    robot = pos
        moves = [MOVES[c] for c in ''.join(move_str.splitlines())]
        return robot, boxes, walls, moves

    def puzzle1(self):
        robot, boxes, walls, moves = self.get_data()
        for move in moves:
            robot, boxes = step(robot, boxes, walls, move)
        print(sum_gps(boxes))

    def puzzle2(self):
        robot, boxes, walls, moves = self.get_data()
        robot, boxes, walls = part2_translation(robot, boxes, walls)
        for move in moves:
            robot, left_boxes = step2(robot, boxes, walls, move)
        print(sum_gps(boxes))


def one_line():
    pass
