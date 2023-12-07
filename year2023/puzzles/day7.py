from year2023.day2023 import Day2023
from typing import *
from collections import Counter


CARD_RANKS = {c: idx for idx, c in enumerate('AKQJT98765432')}
CARD_RANKS2 = {c: idx for idx, c in enumerate('AKQT98765432J')}
HANDS = [
    Counter({5: 1}),
    Counter({4: 1, 1: 1}),
    Counter({3: 1, 2: 1}),
    Counter({3: 1, 1: 2}),
    Counter({2: 2, 1: 1}),
    Counter({2: 1, 1: 3}),
    Counter({1: 5})
]


def get_value(hand, part1=True):
    cnt_cnt = Counter()
    ranking = CARD_RANKS if part1 else CARD_RANKS2
    if part1:
        cnt = Counter(hand)
        cnt_cnt = Counter(cnt.values())
    else:
        if hand == 'JJJJJ':
            jindx = CARD_RANKS2['J']
            return 0, jindx, jindx, jindx, jindx, jindx
        cnt = Counter(c for c in hand if c != 'J')
        most_nums = max(cnt, key=lambda c: cnt[c])
        cnt[most_nums] += sum(1 for c in hand if c == 'J')
        cnt_cnt = Counter(cnt.values())
    hand_val = HANDS.index(cnt_cnt)
    return tuple([hand_val] + [ranking[c] for c in hand])


class Day(Day2023):
    @property
    def num(self) -> int:
        return 7

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [(line.split(' ')[0], int(line.split(' ')[1])) for line in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        sorted_hands = sorted(data, key=lambda d: get_value(d[0]), reverse=True)
        print(sorted_hands)
        total = 0
        for idx, (_, bid) in enumerate(sorted_hands):
            total += (idx + 1) * bid
        print(total)

    def puzzle2(self):
        data = self.get_data()
        sorted_hands = sorted(data, key=lambda d: get_value(d[0], False), reverse=True)
        print(sorted_hands)
        total = 0
        for idx, (_, bid) in enumerate(sorted_hands):
            total += (idx + 1) * bid
        print(total)


def one_line():
    pass
