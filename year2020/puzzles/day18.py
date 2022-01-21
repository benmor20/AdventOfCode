from year2020.day2020 import Day2020
from abc import ABC, abstractmethod



def add(a, b):
    return a + b

def mult(a, b):
    return a * b


class Calculable(ABC):
    @abstractmethod
    def evaluate(self):
        pass


class Number(Calculable):
    def __init__(self, val):
        self.val = val

    def evaluate(self):
        return self.val

    def __repr__(self):
        return str(self.val)


class Expression(Calculable):
    def __init__(self, op, left: Calculable, right: Calculable):
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self):
        return self.op(self.left.evaluate(), self.right.evaluate())

    def __repr__(self):
        op = '+' if self.op == add else '*'
        ls = str(self.left)
        if isinstance(self.left, Expression):
            ls = f'({ls})'
        rs = str(self.right)
        if isinstance(self.right, Expression):
            rs = f'({rs})'
        return f'{ls}{op}{rs}'


def parse_expression(s: str):
    s = s.replace(' ', '')
    if all(c in '0123456789' for c in s):
        return Number(int(s))
    parens = 0
    for rev_i, c in enumerate(s[::-1]):
        if c == ' ':
            continue
        i = len(s) - rev_i - 1
        if parens == 0 and c in '+*':
            op = add if c == '+' else mult
            left, right = s[:i], s[i+1:]
            return Expression(op, parse_expression(left), parse_expression(right))
        elif c == ')':
            parens += 1
        elif c == '(':
            assert parens > 0
            parens -= 1
    # Never exits parens
    return parse_expression(s[1:-1])


def parse_adv_expression(s):
    if all(c in '0123456789 ' for c in s):
        return Number(int(s.replace(' ', '')))
    queue = ['']
    parens = 0
    for c in s:
        if c == ' ':
            continue
        if c == '(':
            parens += 1
        elif c == ')':
            parens -= 1
        elif parens == 0 and c in '+*':
            if queue[-1][0] == '(':
                queue[-1] = queue[-1][1:-1]
            queue.append(c)
            queue.append('')
            continue
        queue[-1] += c
    if queue[-1][0] == '(':
        queue[-1] = queue[-1][1:-1]

    def combine(at):
        op = add if queue[at] == '+' else mult
        left = queue[at - 1]
        right = queue[at + 1]
        # print(f'left: {left}, right: {right}, queue: {queue}')
        if isinstance(left, str):
            left = parse_adv_expression(left)
        if isinstance(right, str):
            right = parse_adv_expression(right)
        del queue[at + 1]
        del queue[at]
        del queue[at - 1]
        queue.insert(at - 1, Expression(op, left, right))
    # print(f'queue is {queue}')

    i = 1
    finished_add = '+' not in queue
    while len(queue) > 1:
        if queue[i] == '+':
            combine(i)
            finished_add = '+' not in queue
            # print(f'new queue: {queue}, continuing at {i}')
        elif finished_add and queue[i] == '*':
            combine(i)
        else:
            i += 1
        if i >= len(queue):
            i = 0
    # print(f'Returning {queue[0]}')
    return queue[0]


class Day(Day2020):
    @property
    def num(self) -> int:
        return 18

    def puzzles(self):
        lines = self.get_data()

        total = 0
        for line in lines:
            exp = parse_adv_expression(line)
            val = exp.evaluate()
            print(f'{exp} evaluates to {val}')
            total += val
        print(f'Total is {total}')
