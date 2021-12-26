from year2021.day2021 import Day2021
from math import floor, ceil


def operate(instr, a, b):
    if instr == 'add':
        return a + b
    elif instr == 'mul':
        return a * b
    elif instr == 'div':
        assert b != 0
        res = a / b
        if res > 0:
            return floor(res)
        return ceil(res)
    elif instr == 'mod':
        assert a >= 0
        assert b > 0
        return a % b
    elif instr == 'eql':
        return 1 if a == b else 0


# Got too excited with parsing to realize that I won't be able to search 10^13 values
# Keeping this anyways
def get_program(lines):
    if len(lines) == 0:
        return lambda inp, vars: vars
    line = lines[0]
    next_prgm = get_program(lines[1:])
    ins = line[:3]
    v1 = line[4]
    if ins == 'inp':
        def func(inp, vars):
            vars[v1] = inp[0]
            return next_prgm(inp[1:], vars)
        return func
    try:
        v2 = int(line[6:])
    except:
        v2 = line[6]
    if ins == 'add':
        def func(inp, vars):
            vars[v1] = vars[v1] + vars.get(v2, v2)
            return next_prgm(inp, vars)
    elif ins == 'mul':
        def func(inp, vars):
            vars[v1] = vars[v1] * vars.get(v2, v2)
            return next_prgm(inp, vars)
    elif ins == 'div':
        def func(inp, vars):
            res = vars[v1] / vars.get(v2, v2)
            vars[v1] = floor(res) if res > 0 else ceil(res)
            return next_prgm(inp, vars)
    elif ins == 'mod':
        def func(inp, vars):
            vars[v1] = vars[v1] % vars.get(v2, v2)
            return next_prgm(inp, vars)
    elif ins == 'eql':
        def func(inp, vars):
            vars[v1] = 1 if vars[v1] == vars.get(v2, v2) else 0
            return next_prgm(inp, vars)
    else:
        raise ValueError(f'Unknown command: {ins}')
    return func


def to_word(z):
    if z == 0:
        return ()
    div, mod = divmod(z, 26)
    return to_word(div) + (mod, )


ays = [11, 14, 13, -4, 11, 10, -4, -12, 10, -11, 12, -1, 0, -11]
bes = [3, 7, 1, 6, 14, 7, 9, 9, 6, 4, 0, 7, 12, 1]
divs = [1, 1, 1, 26, 1, 1, 26, 26, 1, 26, 1, 26, 26, 26]
def effective_monad(n):
    lst = [int(i) for i in str(n)]
    lst.extend([0] * (14 - len(lst)))
    z = 0
    for i, (w, a, b, d) in enumerate(zip(lst, ays, bes, divs)):
        x = (z % 26 + a) != w
        z //= d
        y = 26 if x else 1
        z = z * y + (w + b if x else 0)
        word = to_word(z)
        print(f'X is {x}, letter: {w}, a: {a}, b: {b}, going up: {d == 1}, base 26: {word}')
    return z


class Day(Day2021):
    @property
    def num(self) -> int:
        return 24

    def get_data(self, example=False):
        lines = super().get_data(example)
        prgm = get_program(lines)
        return lambda inp: prgm(inp, {v: 0 for v in 'wxyz'})

    def puzzle1(self):
        # Guess and check approach
        # Was using it to get a feel for what I need to code but got it before I really got a feel
        # So just kept guess and check
        print(effective_monad(92967699949891))
        print()

    def puzzle2(self):
        print(effective_monad(91411143612181))
