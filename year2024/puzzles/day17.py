import itertools
import re

from year2024.day2024 import Day2024


class Computer:
    def __init__(self, areg: int, breg: int, creg: int, program: list[int]):
        self.areg = areg
        self.breg = breg
        self.creg = creg
        self.program = program
        self.pointer = 0
        self.output = []

    def combo_to_literal(self, combo: int) -> int:
        assert 0 <= combo <= 6
        if combo == 4:
            return self.areg
        elif combo == 5:
            return self.breg
        elif combo == 6:
            return self.creg
        return combo

    def adv(self, operand: int):
        self.areg //= 2 ** self.combo_to_literal(operand)

    def bxl(self, operand: int):
        self.breg ^= operand

    def bst(self, operand: int):
        self.breg = self.combo_to_literal(operand) % 8

    def jnz(self, operand: int):
        if self.areg != 0:
            self.pointer = operand
            return True

    def bxc(self, _: int):
        self.breg ^= self.creg

    def out(self, operand: int):
        self.output.append(self.combo_to_literal(operand) % 8)

    def bdv(self, operand: int):
        self.breg = self.areg // (2 ** self.combo_to_literal(operand))

    def cdv(self, operand: int):
        self.creg = self.areg // (2 ** self.combo_to_literal(operand))

    OPERATIONS = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

    def step(self):
        opcode = self.program[self.pointer]
        operand = self.program[self.pointer + 1]
        # print(f'Executing {self.OPERATIONS[opcode].__name__} with operand {operand}')
        pointer_was_moved = self.OPERATIONS[opcode](self, operand)
        # print(f'Registers are now {bin(self.areg)}, {bin(self.breg)}, {bin(self.creg)}')
        if pointer_was_moved is None:
            self.pointer += 2

    def run(self) -> list[int]:
        while self.pointer < len(self.program):
            self.step()
        return self.output

    def reset(self):
        self.areg = self.breg = self.creg = 0
        self.pointer = 0
        self.output = []

    def calc_ideal_a(self):
        for val in itertools.count():
            self.reset()
            self.areg = val
            while self.pointer < len(self.program):
                self.step()
                if len(self.output) > 0 and self.output[-1] != self.program[len(self.output) - 1]:
                    break
            if self.output == self.program:
                return val
            if val % 100 == 0:
                print(val)


def simplified_step(a):
    b = a % 8
    b = b ^ 2
    c = a // (2 ** b)
    b = b ^ c
    b = b ^ 7
    b = b % 8
    return b


def simplified_program(a):
    res = []
    while a > 0:
        res.append(simplified_step(a))
        a //= 8
    return res


def find_solutions(program, current_a=0):
    if len(program) == 0:
        return current_a
    for b in range(8):
        atest = current_a * 8 + b
        res = simplified_step(atest)
        if res == program[-1]:
            ans = find_solutions(program[:-1], atest)
            if ans is not None:
                return ans
    return None


class Day(Day2024):
    @property
    def num(self) -> int:
        return 17

    def get_data(self, example=False):
        lines = super().get_raw_data(example)
        match = re.match(r'Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: ([\d,]+)', lines)
        return Computer(int(match[1]), int(match[2]), int(match[3]), [int(i) for i in match[4].split(',')])

    def puzzle1(self):
        computer = self.get_data()
        print(','.join(str(i) for i in computer.run()))

    def puzzle2(self):
        computer = self.get_data()
        print(find_solutions(computer.program))


def one_line():
    pass
