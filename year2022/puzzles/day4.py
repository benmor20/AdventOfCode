from year2022.day2022 import Day2022


class Day(Day2022):
    @property
    def num(self) -> int:
        return 4

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            astr, bstr = tuple(line.split(','))
            asplt = astr.split('-')
            bsplt = bstr.split('-')
            data.append((set(range(int(asplt[0]), int(asplt[1]) + 1)), set(range(int(bsplt[0]), int(bsplt[1]) + 1))))
        return data

    def puzzle1(self):
        print(sum(a.issuperset(b) or b.issuperset(a) for a, b in self.get_data()))

    def puzzle2(self):
        print(sum(len(a.intersection(b)) > 0 for a, b in self.get_data()))


def one_line():
    with open('year2022/data/day4data.txt', 'r') as file: print(*[data := [(set(range(int(l.split('-')[0]), int(l.split(',')[0].split('-')[1]) + 1)), set(range(int(l.split(',')[1].split('-')[0]), int(l.split('-')[-1].strip()) + 1))) for l in file.readlines()], sum(a.issuperset(b) or b.issuperset(a) for a, b in data), sum(len(a.intersection(b)) > 0 for a, b in data)][1:], sep='\n')
