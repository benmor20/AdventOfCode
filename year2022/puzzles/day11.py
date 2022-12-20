from year2022.day2022 import Day2022
from typing import *
from collections import deque


class Worry:
    def __init__(self, val: int, bases: Tuple[int] = (2, 3, 5, 7, 11, 13, 17, 19, 23)):
        self.remainders = {b: val % b for b in bases}
        self.bases = bases

    def __add__(self, other):
        res = Worry(0, self.bases)
        res.remainders = {b: (r + other) % b for b, r in self.remainders.items()}
        return res

    def __sub__(self, other):
        res = Worry(0, self.bases)
        res.remainders = {b: (r - other) % b for b, r in self.remainders.items()}
        return res

    def __mul__(self, other):
        res = Worry(0, self.bases)
        res.remainders = {b: (r * other) % b for b, r in self.remainders.items()}
        return res

    def __floordiv__(self, other):
        res = Worry(0, self.bases)
        if any(other == b for b in self.bases):
            assert False
        res.remainders = {b: (r * (pow(other, b - 2, b))) % b for b, r in self.remainders}
        return res

    def __pow__(self, power, modulo=None):
        res = Worry(0, self.bases)
        res.remainders = {b: (r ** power) % b for r, b in self.remainders}
        return res

    def __mod__(self, other):
        if other not in self.bases:
            assert False
        return self.remainders[other]


class Monkey:
    def __init__(self, items: Deque[Worry], operation: str, op_val: int, test: int, true_monk: int, false_monk: int):
        self.items = items
        self.operation = operation
        self.op_val = op_val
        self.test = test
        self.true_monkey = true_monk
        self.false_monkey = false_monk
        self.num_inspected = 0

    def do_test(self, worry):
        return worry % self.test == 0

    def do_operation(self, worry):
        if self.operation == '*':
            if self.op_val == -1:
                return worry ** 2
            return worry * self.op_val
        return worry + self.op_val

    def do_turn(self, third: bool = True) -> List[Tuple[Worry, int]]:
        res = []
        while len(self.items) > 0:
            worry = self.items.popleft()
            self.num_inspected += 1
            worry = self.do_operation(worry)
            if third:
                worry = worry // 3
            res.append((worry, self.true_monkey if self.do_test(worry) else self.false_monkey))
        return res

    def __str__(self):
        return f'Items: {", ".join(str(i) for i in self.items)}\nOperation: new = old {self.operation} {"old" if self.op_val == -1 else self.op_val}\nTest: divisible by {self.test}\n\tIf true: throw to monkey {self.true_monkey}\n\tIf false: throw to monkey {self.false_monkey}'

    def __repr__(self):
        return str(self)


def do_round(monkies: List[Monkey], third: bool = True):
    for monkey in monkies:
        throws = monkey.do_turn(third)
        for worry, index in throws:
            monkies[index].items.append(worry)


class Day(Day2022):
    @property
    def num(self) -> int:
        return 11

    def get_data(self, example=False):
        with open(self.filepath(example), 'r') as file:
            text = file.read()
        monktext = text.split('\n\n')
        monkies = []
        for monkey_text in monktext:
            lines = monkey_text.split('\n')
            items = deque([Worry(int(i)) for i in lines[1].split(': ')[1].split(', ')])
            opstr = '*' if '*' in lines[2] else '+'
            rhs = lines[2].split(f' {opstr} ')[-1]
            divnum = int(lines[3].split(' ')[-1])
            truemonk = int(lines[4].split(' ')[-1])
            falsemonk = int(lines[5].split(' ')[-1])
            monkies.append(Monkey(items, opstr, -1 if rhs == 'old' else int(rhs), divnum, truemonk, falsemonk))
        return monkies

    def puzzle1(self):
        monkies = self.get_data()
        for _ in range(20):
            do_round(monkies)
        top = max(monkies, key=lambda m: m.num_inspected)
        nxt = max(monkies, key=lambda m: m.num_inspected if m != top else 0)
        print(top.num_inspected * nxt.num_inspected)

    def puzzle2(self):
        monkies = self.get_data()
        for _ in range(10000):
            do_round(monkies, False)
        top = max(monkies, key=lambda m: m.num_inspected)
        nxt = max(monkies, key=lambda m: m.num_inspected if m != top else 0)
        print([m.num_inspected for m in monkies])
        print(top.num_inspected * nxt.num_inspected)
