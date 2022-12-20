from year2022.day2022 import Day2022
from functools import cmp_to_key


def parse_list(lst):
    if lst[0] == '[':
        num_brackets = 0
        res = []
        curstr = ''
        for i, c in enumerate(lst):
            if i == 0:
                continue
            curstr += c
            if c == '[':
                num_brackets += 1
            elif c == ']':
                num_brackets -= 1
            if num_brackets == 0 and c == ',':
                res.append(parse_list(curstr[:-1]))
                curstr = ''
            elif num_brackets == -1 and c == ']' and len(curstr) > 1:
                res.append(parse_list(curstr[:-1]))
        return tuple(res)
    return int(lst)


def is_ordered(a, b):
    aint = isinstance(a, int)
    bint = isinstance(b, int)
    # print(a, b)
    if aint and bint:
        # print('Both ints', end='; ')
        if a == b:
            # print('Equal, giving None')
            return None
        # print(f'different, giving {a < b}')
        return a < b
    elif aint and not bint:
        # print('a is an int, recursing')
        return is_ordered([a], b)
    elif not aint and bint:
        # print('b is an int, recursing')
        return is_ordered(a, [b])

    # print('both are lists')
    for i, aval in enumerate(a):
        if i == len(b):
            # print('b ran out first')
            return False
        recres = is_ordered(aval, b[i])
        if recres is not None:
            return recres
    return None if len(a) == len(b) else True


class Day(Day2022):
    @property
    def num(self) -> int:
        return 13

    def get_data(self, example=False):
        with open(self.filepath(example), 'r') as file:
            lines = file.read()
        pairs = lines.split('\n\n')
        data = []
        for pair in pairs:
            astr, bstr = tuple(pair.split('\n'))
            data.append((parse_list(astr), parse_list(bstr)))
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for i, (a, b) in enumerate(data):
            res = is_ordered(a, b)
            assert res is not None
            if res:
                total += i + 1
        print(total)

    def puzzle2(self):
        pairs = self.get_data()
        div1, div2 = parse_list('[[2]]'), parse_list('[[6]]')
        data = [div1, div2]
        for a, b in pairs:
            data.extend([a, b])
        data_sorted = sorted(data, key=cmp_to_key(lambda a, b: -1 if is_ordered(a, b) else 1))
        # print('\n'.join(str(d) for d in data_sorted))
        print((data_sorted.index(div1) + 1) * (data_sorted.index(div2) + 1))
