from year2024.day2024 import Day2024


KEYPAD = {
    'A': 3 + 2j,
    '0': 3 + 1j,
    '1': 2 + 0j,
    '2': 2 + 1j,
    '3': 2 + 2j,
    '4': 1 + 0j,
    '5': 1 + 1j,
    '6': 1 + 2j,
    '7': 0 + 0j,
    '8': 0 + 1j,
    '9': 0 + 2j,
}
CONTROLLER = {
    'A': 0 + 2j,
    '^': 0 + 1j,
    '<': 1 + 0j,
    'v': 1 + 1j,
    '>': 1 + 2j,
}
DIRECTIONS = {
    1: 'v',
    -1: '^',
    1j: '>',
    -1j: '<'
}


PATH_MEMO = {}
def get_path_from_code(code, positions):
    if code in PATH_MEMO:
        return PATH_MEMO[code]
    current_pos = 'A'
    path = ''
    for next_pos in code:
        diff = positions[next_pos] - positions[current_pos]
        lr = DIRECTIONS[1j if diff.imag > 0 else -1j] * abs(int(diff.imag))
        ud = DIRECTIONS[1 if diff.real > 0 else -1] * abs(int(diff.real))
        if current_pos in '0A^' and next_pos in '147<':
            path += f'{ud}{lr}A'
        elif current_pos in '147<' and next_pos in '0A^':
            path += f'{lr}{ud}A'
        else:
            # Evidently the order of this sort is very important
            # <v>^ works for P1 but not P2
            path += ''.join(sorted(f'{lr}{ud}', key=lambda c: '<v^>'.index(c))) + 'A'
        current_pos = next_pos
    PATH_MEMO[code] = path
    return path


def guess_at_path(code):
    return ''.join(get_path_from_code(move + 'A', CONTROLLER) for move in code.split('A')[:-1])


NUM_MEMO = {}
def num_moves(code, repeats):
    if (code, repeats) in NUM_MEMO:
        return NUM_MEMO[(code, repeats)]
    if repeats == 0:
        NUM_MEMO[(code, repeats)] = len(code)
        return len(code)
    path = get_path_from_code(code, CONTROLLER)
    ans = sum(num_moves(sec + 'A', repeats - 1) for sec in path.split('A')[:-1])
    NUM_MEMO[(code, repeats)] = ans
    return ans


class Day(Day2024):
    @property
    def num(self) -> int:
        return 21

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for code in data:
            path = get_path_from_code(code, KEYPAD)
            for i in range(2):
                path = get_path_from_code(path, CONTROLLER)
            # print(f'path for {code} is {path}')
            to_add = len(path) * int(code[:-1])
            total += to_add
            # print(f'Score is {len(path)} * {int(code[:-1])} = {to_add}, total of {total}')
        print(total)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        for code in data:
            path = get_path_from_code(code, KEYPAD)
            path_len = num_moves(path, 25)
            to_add = path_len * int(code[:-1])
            total += to_add
        print(total)


def one_line():
    pass
