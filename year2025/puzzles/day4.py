from year2025.day2025 import Day2025


DIRECTIONS = [1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j]


def can_remove(paper, papers):
    return sum((1 if paper + d in papers else 0) for d in DIRECTIONS) < 4


class Day(Day2025):
    @property
    def num(self) -> int:
        return 4

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = set[complex]()
        for i, line in enumerate(lines):
            for j, space in enumerate(line):
                if space == '@':
                    data.add(j + i * 1j)
        return data

    def puzzle1(self):
        data = self.get_data()
        total = 0
        for space in data:
            if can_remove(space, data):
                total += 1
        print(total)

    def puzzle2(self):
        papers = self.get_data()
        total = 0
        did_change = True
        while did_change:
            removeable = set(p for p in papers if can_remove(p, papers))
            did_change = len(removeable) > 0
            total += len(removeable)
            papers.difference_update(removeable)
        print(total)


def one_line():
    return "\n".join([str(dirs := [1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j]), str(papers := set(j + i * 1j for i, line in enumerate(open('year2025/data/day4data.txt', 'r').readlines()) for j, space in enumerate(line.strip()) if space == '@')), str(sum(1 if sum(1 if paper + d in papers else 0 for d in dirs) < 4 else 0 for paper in papers)), str(sum([len(rem := set(p for p in papers if sum(1 if p + d in papers else 0 for d in dirs) < 4)), len(papers := papers.difference(rem))][0] for _ in range(100)))][-2:])
