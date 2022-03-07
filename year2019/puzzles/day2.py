from year2019.day2019 import Day2019


def step(pos, intcode):
    opcode = intcode[pos]
    if opcode == 99:
        return True, intcode
    if opcode == 1:
        intcode[intcode[pos+3]] = intcode[intcode[pos+1]] + intcode[intcode[pos+2]]
        return False, intcode
    if opcode == 2:
        intcode[intcode[pos+3]] = intcode[intcode[pos+1]] * intcode[intcode[pos+2]]
        return False, intcode
    raise ValueError(f'Opcode at position {pos} is {opcode}')


def run(intcode, noun, verb):
    runcode = intcode.copy()
    runcode[1] = noun
    runcode[2] = verb
    end = False
    pos = 0
    while not end:
        end, runcode = step(pos, runcode)
        pos += 4
    return runcode


class Day(Day2019):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example=False):
        lines = super().get_data(type(example) is int or example)  # bool is int
        data = lines[0 if isinstance(example, bool) else example].split(',')
        data = [int(i) for i in data]
        return data

    def puzzles(self):
        intcode = self.get_data()
        p1code = run(intcode, 12, 2)
        print(f'Result is {p1code[0]}')

        for i in range(9999):
            noun, verb = divmod(i, 100)
            p2code = run(intcode, noun, verb)
            if p2code[0] == 19690720:
                print(f'noun {noun}, verb {verb}, res {i}')
