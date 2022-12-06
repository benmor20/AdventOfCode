from year2022.day2022 import Day2022
from collections import deque


class Day(Day2022):
    @property
    def num(self) -> int:
        return 6

    def get_data(self, example=False):
        return super().get_data(example)[0]

    def puzzle1(self):
        data = self.get_data()
        len_needed = 4
        for i, c in enumerate(data):
            if len(set(data[i:i+len_needed])) == len_needed:
                print(i+len_needed)
                break

    def puzzle2(self):
        data = self.get_data()
        len_needed = 14
        for i, c in enumerate(data):
            if len(set(data[i:i+len_needed])) == len_needed:
                print(i+len_needed)
                break


def one_line():
    with open('year2022/data/day6exdata.txt', 'r') as file: print(*[data := file.readline().strip(), min(i+4 for i in range(len(data)) if len(set(data[i:i+4])) == 4), min(i+14 for i in range(len(data)) if len(set(data[i:i+14])) == 14)][1:], sep='\n')
