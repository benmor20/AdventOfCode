from year2022.day2022 import Day2022


POINTS = {'R': 1, 'P': 2, 'S': 3}
RPS = {'A': 'R', 'B': 'P', 'C': 'S', 'X': 'R', 'Y': 'P', 'Z': 'S'}
XYZ = {'R': 'X', 'P': 'Y', 'S': 'Z'}
WIN = {'R': 'S', 'P': 'R', 'S': 'P'}
LOSE = {'R': 'P', 'P': 'S', 'S': 'R'}


class Day(Day2022):
    @property
    def num(self) -> int:
        return 2

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [(RPS[l[0]], RPS[l[2]]) for l in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        score = 0
        for other, you in data:
            score += POINTS[you]
            if WIN[you] == other:
                score += 6
            elif you == other:
                score += 3
        print(score)

    def puzzle2(self):
        data = self.get_data()
        score = 0
        for other, you in data:
            you = XYZ[you]
            if you == 'X':
                score += POINTS[WIN[other]]
            elif you == 'Y':
                score += POINTS[other] + 3
            elif you == 'Z':
                score += POINTS[LOSE[other]] + 6
        print(score)


def one_line():
    with open('year2022/data/day2data.txt', 'r') as file: print(*[(data := [l.strip().replace(' ', '') for l in file.readlines()]), sum({"AX": 3 + 1, "AY": 6 + 2, "AZ": 0 + 3, "BX": 0 + 1, "BY": 3 + 2, "BZ": 6 + 3, "CX": 6 + 1, "CY": 0 + 2, "CZ": 3 + 3}[d] for d in data), sum({"AX": 0 + 3, "AY": 3 + 1, "AZ": 6 + 2, "BX": 0 + 1, "BY": 3 + 2, "BZ": 6 + 3, "CX": 0 + 2, "CY": 3 + 3, "CZ": 6 + 1}[d] for d in data)][1:], sep='\n')
