from year2024.day2024 import Day2024
from typing import *
import re


class Day(Day2024):
    @property
    def num(self) -> int:
        return 3

    def get_data(self, example=False):
        lines = super().get_data(example)
        return ''.join(lines)

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for command in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', data):
            total += int(command[1]) * int(command[2])
        print(total)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        doing = True
        for command in re.finditer(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)", data):
            if command[0] == 'do()':
                doing = True
            elif command[0] == "don't()":
                doing = False
            elif doing:
                total += int(command[1]) * int(command[2])
        print(total)


def one_line():
    return '\n'.join([data := ''.join(open('year2024/data/day3data.txt', 'r').readlines()), doing := True, str(sum(int(m[1]) * int(m[2]) for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", data))), str(sum([doing := m[0] == 'do()' if m[0][0] == 'd' else doing, int(m[1]) * int(m[2]) if doing and m[0][0] == 'm' else 0][1] for m in re.finditer(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)", data)))][-2:])
