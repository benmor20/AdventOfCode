from year2021.day2021 import Day2021
import numpy as np


class Board:
    def __init__(self, board):
        self.board = board
        self.found = [[False for _ in row] for row in board]

    def update(self, num):
        for i, row in enumerate(self.board):
            if num in row:
                self.found[i][row.index(num)] = True

    def won(self):
        dr = True
        ur = True
        for i in range(len(self.board)):
            if all(self.found[i]):
                # print(f'row {i} is true')
                return True
            if all([b[i] for b in self.found]):
                # print(f'col {i} is true')
                return True
            dr = dr and self.found[i][i]
            ur = ur and self.found[4 - i][i]
        # if dr:
        #     print(f'dr is true')
        # if ur:
        #     print('ur is true')
        return False # dr or ur

    def __repr__(self):
        s = ''
        for row in self.board:
            s += str(row)
            s += '\n'
        return s[:-1]

    def found_str(self):
        s = ''
        for row in self.found:
            s += str(row)
            s += '\n'
        return s[:-1]


class Day(Day2021):
    @property
    def num(self) -> int:
        return 4

    def get_data(self, example=False):
        data = super().get_data(example)
        nums = [int(i) for i in data[0].split(',')]
        boards = []
        board = []
        index = 0
        for line in data[2:]:
            if index == 5:
                boards.append(Board(board))
                board = []
                index = 0
                continue
            board.append([int(i) for i in line.split(' ') if len(i) > 0 and i != '\n'])
            index += 1
        boards.append(Board(board))
        return nums, boards

    def puzzle1(self):
        nums, boards = self.get_data()
        for j, num in enumerate(nums):
            for i, board in enumerate(boards):
                board.update(num)
                if board.won():
                    print(board)
                    print(j, num)
                    print(board.found_str())
                    s = sum([sum([n for j, n in enumerate(row) if not board.found[i][j]]) for i, row in enumerate(board.board)])
                    print(s, num, s * num)
                    return

    def puzzle2(self):
        nums, boards = self.get_data()
        all_boards = set(range(len(boards)))
        done_boards = set()
        for j, num in enumerate(nums):
            for i, board in enumerate(boards):
                if i in done_boards:
                    continue
                board.update(num)
                if board.won():
                    done_boards.add(i)
                    if len(done_boards) == len(all_boards):
                        s = sum([sum([n for j, n in enumerate(row) if not board.found[i][j]]) for i, row in
                                 enumerate(board.board)])
                        print(s, num, s * num)
                        return
