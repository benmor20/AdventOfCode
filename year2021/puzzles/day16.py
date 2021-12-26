from year2021.day2021 import Day2021


hex_to_bin = {'0': '0000',
'1': '0001',
'2': '0010',
'3': '0011',
'4': '0100',
'5': '0101',
'6': '0110',
'7': '0111',
'8': '1000',
'9': '1001',
'A': '1010',
'B': '1011',
'C': '1100',
'D': '1101',
'E': '1110',
'F': '1111'}


def product(lst):
    res = 1
    for v in lst:
        res *= v
    return res


def greater_than(lst):
    return 1 if lst[0] > lst[1] else 0


def less_than(lst):
    return 1 if lst[0] < lst[1] else 0


def equal(lst):
    return 1 if lst[0] == lst[1] else 0


operations = [sum, product, min, max, None, greater_than, less_than, equal]


def binary_to_dec(binary):
    val = 0
    for b in binary:
        val *= 2
        val += int(b)
    return val


def get_version_sum(binary):
    version = binary_to_dec(binary[:3])
    typeid = binary_to_dec(binary[3:6])
    if typeid == 4:
        for i in range(6, len(binary), 5):
            if binary[i] == '0':
                return version, i + 5
        return version, len(binary)
    else:
        total = version
        lenid = binary_to_dec(binary[6])
        if lenid == 0:
            len_packages = binary_to_dec(binary[7:22])
            index = 22
            while index - 22 < len_packages and index < len(binary):
                v, i = get_version_sum(binary[index:])
                index += i
                total += v
        else:
            num_packages = binary_to_dec(binary[7:18])
            index = 18
            for _ in range(num_packages):
                v, i = get_version_sum(binary[index:])
                index += i
                total += v
        return total, index


def get_value(binary):
    typeid = binary_to_dec(binary[3:6])
    # print('Num' if typeid == 4 else operations[typeid])
    if typeid == 4:
        num_bin = ''
        for i in range(6, len(binary), 5):
            num_bin += binary[i+1:i+5]
            if binary[i] == '0':
                return binary_to_dec(num_bin), i + 5
        return binary_to_dec(num_bin), len(binary)
    else:
        values = []
        lenid = binary_to_dec(binary[6])
        if lenid == 0:
            len_packages = binary_to_dec(binary[7:22])
            index = 22
            while index - 22 < len_packages and index < len(binary):
                v, i = get_value(binary[index:])
                index += i
                values.append(v)
        else:
            num_packages = binary_to_dec(binary[7:18])
            index = 18
            for _ in range(num_packages):
                v, i = get_value(binary[index:])
                index += i
                values.append(v)
        # print(typeid)
        # print(operations[typeid])
        return operations[typeid](values), index


class Day(Day2021):
    @property
    def num(self) -> int:
        return 16

    def get_data(self, example=False):
        hexes = super().get_data(example)
        data = []
        for h in hexes:
            data.append(''.join(hex_to_bin[v] for v in h))
        return data

    def puzzle1(self):
        data = self.get_data()
        for binary in data:
            total = get_version_sum(binary)[0]
            print(total)

    def puzzle2(self):
        data = self.get_data()
        for binary in data:
            total = get_value(binary)[0]
            print(total)
            break
