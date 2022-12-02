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
