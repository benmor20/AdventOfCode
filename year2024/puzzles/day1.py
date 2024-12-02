from year2024.day2024 import Day2024
from collections import Counter


class Day(Day2024):
    @property
    def num(self) -> int:
        return 1

    def get_data(self, example=False):
        lines = super().get_data(example)
        l1 = []
        l2 = []
        for line in lines:
            vals = line.split()
            l1.append(int(vals[0]))
            l2.append(int(vals[1]))
        return l1, l2

    def puzzle1(self):
        list1, list2 = self.get_data()
        total = 0
        for a, b in zip(sorted(list1), sorted(list2)):
            total += abs(a - b)
        print(total)

    def puzzle2(self):
        list1, list2 = self.get_data()
        right_count = Counter(list2)
        score = 0
        for val in list1:
            score += val * right_count[val]
        print(score)


def one_line():
    return '\n'.join([ls := list(zip(*[tuple(int(i) for i in line.strip().split()) for line in open('year2024/data/day1data.txt', 'r').readlines()])), right_cnt := Counter(ls[1]), str(sum(abs(a - b) for a, b in zip(sorted(ls[0]), sorted(ls[1])))), str(sum(val * right_cnt[val] for val in ls[0]))][-2:])
