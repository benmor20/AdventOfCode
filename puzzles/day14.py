from puzzles.daybase import DayBase
from collections import Counter
from utils import LinkedList, Node


def step_str(start, rules):
    res = []
    c2 = ''
    for i, c1 in enumerate(start[:-1]):
        c2 = start[i + 1]
        pair = c1 + c2
        if pair in rules:
            res.extend([c1, rules[pair]])
        else:
            res.append(c1)
    res.append(c2)
    return ''.join(res)

    # lst = step_rec(start, rules)
    # return ''.join(lst)

def step_cnt(start, rules):
    counter = Counter()
    for pair in start:
        if pair in rules:
            mid = rules[pair]
            left, right = tuple(pair)
            counter.update({left + mid: start[pair],
                            mid + right: start[pair]})
        else:
            counter.update({pair: start[pair]})
    return counter


# def step_rec(start, rules):
#     if len(start) == 1:
#         return LinkedList([start])
#     mid = len(start) // 2
#     left, right = step_rec(start[:mid], rules), step_rec(start[mid:], rules)
#     pair = left.tail.value + right.head.value
#     if pair in rules:
#         n = Node(rules[pair], left=left.tail, right=right.head)
#         left.tail.right = n
#         right.head.left = n
#         left.tail = right.tail
#         return left
#     else:
#         left.tail.right = right.head
#         right.head.left = left.tail
#         left.tail = right.tail
#         return left


class Day(DayBase):
    @property
    def num(self) -> int:
        return 14

    def get_data(self, example=False):
        lines = super().get_data(example)
        start = lines[0]
        rules = dict([tuple(l.split(' -> ')) for l in lines[2:]])
        return start, rules

    def puzzle1(self):
        start, rules = self.get_data(True)
        for _ in range(10):
            start = step_str(start, rules)
        counter = Counter(start)
        print(max(counter.values()) - min(counter.values()))

    def puzzle2(self):
        start, rules = self.get_data()

        counter = Counter()
        for i, c1 in enumerate(start[:-1]):
            c2 = start[i + 1]
            counter.update([c1 + c2])

        for _ in range(40):
            counter = step_cnt(counter, rules)

        res = Counter()
        res.update(start[0] + start[-1])
        for pair, cnt in counter.items():
            res.update({pair[0]: cnt})
            res.update({pair[1]: cnt})  # separate for the case of repeats

        vals = res.values()
        print((max(vals) - min(vals)) // 2)
