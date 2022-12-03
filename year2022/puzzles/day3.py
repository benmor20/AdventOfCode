from year2022.day2022 import Day2022


def get_priority(item):
    if item.lower() == item:
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27


class Day(Day2022):
    @property
    def num(self) -> int:
        return 3

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for sack in data:
            first, last = set(sack[:len(sack) // 2]), set(sack[len(sack) // 2:])
            overlap = first.intersection(last).pop()
            total += get_priority(overlap)
        print(total)

    def puzzle2(self):
        data = self.get_data()
        total = 0
        for sacknum in range(0, len(data), 3):
            sacks = [set(d) for d in data[sacknum:sacknum + 3]]
            badge = sacks[0].intersection(*sacks[1:]).pop()
            total += get_priority(badge)
        print(total)


def one_line():
    with open('year2022/data/day3data.txt', 'r') as file: print(*[priority := lambda c: ord(c) - ord('a') + 1 if c.islower() else ord(c) - ord('A') + 27, data := [d.strip() for d in file.readlines()], sum(priority(set(d[:len(d) // 2]).intersection(set(d[len(d) // 2:])).pop()) for d in data), sum(priority(set(data[i]).intersection(set(data[i+1]), set(data[i+2])).pop()) for i in range(0, len(data), 3))][2:], sep='\n')
