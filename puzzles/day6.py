from puzzles.daybase import DayBase
import numpy as np
# from collections import deque     gives overflow errors


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Queue:
    def __init__(self, vals):
        prev = None
        for i, v in enumerate(vals):
            n = Node(int(v), left=prev)
            if i == 0:
                self.head = n
            else:
                prev.right = n
            prev = n
        self.tail = prev

    def pop(self):
        n, self.head = self.head, self.head.right
        self.head.left = None
        return n.value

    def push(self, val):
        n = Node(val, left=self.tail)
        self.tail.right = n
        self.tail = n

    def values(self):
        n = self.head
        while n:
            yield n.value
            n = n.right

    def __len__(self):
        return len(list(self.values()))

    def __getitem__(self, item):
        n = self.head
        for _ in range(item):
            n = n.right
        return n.value

    def __setitem__(self, key, value):
        n = self.head
        for _ in range(key):
            n = n.right
        n.value = value

    def __repr__(self):
        s = '['
        n = self.head
        while n:
            s += str(n.value)
            s += ','
            n = n.right
        s = s[:-1]
        s += ']'
        return s


class Day(DayBase):
    @property
    def num(self) -> int:
        return 6

    def get_data(self, example=False):
        return [int(i) for i in super().get_data(example)[0].split(',')]

    def puzzle1(self):
        return
        fish = np.array(self.get_data())
        for i in range(80):
            rep = fish == 0
            new = sum(rep)
            fish += 7 * rep
            fish = np.append(fish, [9] * new)
            fish -= 1
        print(len(fish))

    def puzzle2(self):
        fish_ages = np.array(self.get_data())
        fish = []
        for i in range(7):
            fish.append(sum(fish_ages == i))
        fish += [0, 0]
        # I am now realizing a list would effectively run constant time for this since the list size is only 9
        # but whatever
        fish = Queue(fish)
        for i in range(256):
            new = fish.pop()
            fish.push(new)
            fish[6] += new
            print(i, fish)
        print(sum(fish.values()))
