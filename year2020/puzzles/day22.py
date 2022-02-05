import itertools
from collections import deque

from year2020.day2020 import Day2020


def play_round(p1hand, p2hand, cards=None, metric=lambda h1, h2, c1, c2: c1 > c2):
    if cards is None:
        p1card = p1hand.popleft()
        p2card = p2hand.popleft()
    else:
        p1card, p2card = cards
    if metric(p1hand, p2hand, p1card, p2card):
        p1hand.append(p1card)
        p1hand.append(p2card)
    else:
        p2hand.append(p2card)
        p2hand.append(p1card)
    return p1hand, p2hand


def calculate_score(hand):
    score = 0
    ncards = len(hand)
    for i, val in enumerate(hand):
        score += (ncards - i) * val
    return score


def recursive_metric(h1, h2, c1, c2, level):
    h1c = deque(list(h1)[:c1])
    h2c = deque(list(h2)[:c2])
    return play_recursive(h1c, h2c, level+1)[0] == 1


def play_recursive(p1hand, p2hand, game_level=1):
    prev_states = set()

    for i in itertools.count(1):
        game_state = tuple(p1hand), tuple(p2hand)
        if game_state in prev_states:
            return 1, calculate_score(p1hand)
        prev_states.add(game_state)
        p1card, p2card = p1hand.popleft(), p2hand.popleft()
        if p1card <= len(p1hand) and p2card <= len(p2hand):
            metric = lambda h1, h2, c1, c2: recursive_metric(h1, h2, c1, c2, game_level)
            play_round(p1hand, p2hand, (p1card, p2card), metric)
        else:
            play_round(p1hand, p2hand, (p1card, p2card))
        if len(p1hand) == 0:
            winner = 2
            break
        elif len(p2hand) == 0:
            winner = 1
            break

    winner_hand = p1hand if winner == 1 else p2hand
    return winner, calculate_score(winner_hand)


class Day(Day2020):
    @property
    def num(self) -> int:
        return 22

    def get_data(self, example=False):
        lines = super().get_data(example)
        p1hand, p2hand = deque(), deque()
        current = p1hand
        for line in lines:
            if len(line) == 0:
                current = p2hand
            elif line[0] == 'P':
                continue
            else:
                current.append(int(line))
        return p1hand, p2hand

    def puzzles(self):
        p1hand, p2hand = self.get_data()

        while len(p1hand) > 0 and len(p2hand) > 0:
            p1hand, p2hand = play_round(p1hand, p2hand)

        winner = max([p1hand, p2hand], key=len)
        num_cards = len(winner)
        score = 0
        for i, val in enumerate(winner):
            score += (num_cards - i) * val
        print(f'Win with score {score}')

        p1hand, p2hand = self.get_data()
        winner, score = play_recursive(p1hand, p2hand)
        print(f'Winner is player {winner} with a score of {score}')
