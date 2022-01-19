from year2020.day2020 import Day2020


def get_addresses(orig, rev_mask):
    if len(rev_mask) == 1:
        if rev_mask == 'X':
            yield 0
            yield 1
        else:
            yield orig | int(rev_mask)
    else:
        for a in get_addresses(orig // 2, rev_mask[1:]):
            if rev_mask[0] == 'X' or (rev_mask[0] == '0' and orig % 2 == 0):
                yield 2 * a
            if rev_mask[0] == 'X' or rev_mask[0] == '1' or orig % 2 == 1:
                yield 2 * a + 1


class Day(Day2020):
    @property
    def num(self) -> int:
        return 14

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            if line[:7] == 'mask = ':
                data.append(('mask', line[7:]))
            else:
                mem, val = tuple(line.split(' = '))
                address = int(mem[4:-1])
                data.append((address, int(val)))
        return data

    def puzzles(self):
        instr = self.get_data()

        # Puzzle 1
        overwrite0 = sum(2 ** i for i in range(36))
        overwrite1 = 0
        mem = {}
        for addr, val in instr:
            if addr == 'mask':
                overwrite0 = sum(2 ** i for i, v in enumerate(val[::-1]) if v != '0')
                overwrite1 = sum(2 ** i for i, v in enumerate(val[::-1]) if v == '1')
            else:
                res = (val & overwrite0) | overwrite1
                # print(f'Setting {addr} to {res}')
                mem[addr] = (val & overwrite0) | overwrite1
        print(f'Sum is {sum(mem.values())}')

        # Puzzle 2
        mask = 0
        mem = {}
        for addr, val in instr:
            if addr == 'mask':
                mask = val
            else:
                for a in get_addresses(addr, mask[::-1]):
                    mem[a] = val
        print(f'V2 sum is {sum(mem.values())}')
