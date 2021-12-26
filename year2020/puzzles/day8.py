from year2020.day2020 import Day2020_3


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example: bool = False):
        code = []
        lines = super().get_data(example)
        for line in lines:
            splt = line.split(' ')
            code.append((splt[0], int(splt[1][1:]) * (-1 if splt[1][0] == '-' else 1)))
        return code

    def puzzle(self, num=1):
        code = self.get_data()
        for flip in range(len(code)):
            if code[flip][0] == 'acc':
                continue
            code[flip] = 'jmp' if code[flip][0] == 'nop' else 'nop', code[flip][1]
            acc = 0
            seen = set()
            line = 0
            while line not in seen:
                if line >= len(code):
                    print(f'Reached end with acc {acc}, flipping line {line}')
                    return
                seen.add(line)
                instr, val = code[line]
                if instr == 'acc':
                    acc += val
                    line += 1
                elif instr == 'nop':
                    line += 1
                elif instr == 'jmp':
                    line += val
                # if num == 2:
                #     print(f'{instr} {val}: moves to line {line}')
            print(acc)
            code[flip] = 'jmp' if code[flip][0] == 'nop' else 'nop', code[flip][1]
