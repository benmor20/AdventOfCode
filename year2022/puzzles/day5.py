from year2022.day2022 import Day2022
from collections import deque


class Day(Day2022):
    @property
    def num(self) -> int:
        return 5

    def get_data(self, example=False):
        with open(self.filepath(example), 'r') as file:
            text = file.read()
        crates, moves = tuple(text.split('\n\n'))

        crates_by_lines = crates.split('\n')
        num_stacks = (len(crates_by_lines[-1]) + 2) // 4
        stacks = [deque() for _ in range(num_stacks)]
        for row in crates_by_lines[:-1]:
            for i in range(0, len(row), 4):
                letter = row[i + 1]
                if letter == ' ':
                    continue
                stacks[i // 4].append(letter)

        moves_by_lines = moves.split('\n')
        parsed_moves = []
        for move in moves_by_lines:
            splt = move.split(' ')
            parsed_moves.append(tuple(int(splt[i]) for i in (1, 3, 5)))
        return stacks, parsed_moves

    def puzzle1(self):
        stacks, moves = self.get_data()

        # print(stacks)
        for amt, start, end in moves:
            start -= 1
            end -= 1
            picked_up = deque()
            for _ in range(amt):
                picked_up.append(stacks[start].popleft())
            for _ in range(amt):
                stacks[end].appendleft(picked_up.popleft())
            # print(stacks)
        print(''.join(s.popleft() for s in stacks))

    def puzzle2(self):
        stacks, moves = self.get_data()

        # print(stacks)
        for amt, start, end in moves:
            start -= 1
            end -= 1
            picked_up = deque()
            for _ in range(amt):
                picked_up.append(stacks[start].popleft())
            for _ in range(amt):
                stacks[end].appendleft(picked_up.pop())
            # print(stacks)
        print(''.join(s.popleft() for s in stacks))
