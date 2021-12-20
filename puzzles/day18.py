from puzzles.daybase import DayBase
from utils import *


def parse_snailfish(s):
    return parse_snailfish_rec(s, 0)[0]


def parse_snailfish_rec(s, i):
    if s[i] == '[':
        i += 1
        left, i = parse_snailfish_rec(s, i)
        i += 1
        right, i = parse_snailfish_rec(s, i)
        return SnailfishNumber(0, left, right), i + 1
    else:
        val = 0
        while s[i] in '0123456789':
            val *= 10
            val += int(s[i])
            i += 1
        return SnailfishNumber(val), i


class SnailfishNumber(Node):
    def __init__(self, value=0, left: 'SnailfishNumber' = None, right: 'SnailfishNumber' = None,
                 parent: 'SnailfishNumber' = None):
        super().__init__(value, left, right)
        self.parent = parent
        if left is not None:
            left.parent = self
        if right is not None:
            right.parent = self

    @property
    def is_leaf(self):
        return self.left is None

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_left(self):
        return not self.is_root and self.parent.left is self

    @property
    def is_right(self):
        return not self.is_root and self.parent.right is self

    @property
    def depth(self):
        if self.is_root:
            return 0
        return self.parent.depth + 1

    def max_depth(self):
        if self.is_leaf:
            return 0
        return max(self.left.max_depth(), self.right.max_depth()) + 1

    def leftmost(self):
        if self.is_leaf:
            return self
        return self.left.leftmost()

    def rightmost(self):
        if self.is_leaf:
            return self
        return self.right.rightmost()

    def linear_left(self):
        node = self
        while node.is_left:
            node = node.parent
            if node is None:
                return None
        if node.parent is None:
            return None
        return node.parent.left.rightmost()

    def linear_right(self):
        node = self
        while node.is_right:
            node = node.parent
            if node is None:
                return None
        if node.parent is None:
            return None
        return node.parent.right.leftmost()

    def explode(self):
        if self.is_leaf:
            return False
        if self.depth >= 4:
            left = self.linear_left()
            if left is not None:
                left.value += self.left.value
            right = self.linear_right()
            if right is not None:
                right.value += self.right.value
            self.value = 0
            self.left = self.right = None
            return True
        return self.left.explode() or self.right.explode()  # Won't call right if left is True

    def split(self):
        if self.is_leaf:
            if self.value > 9:
                self.left = SnailfishNumber(self.value // 2)
                self.left.parent = self
                self.right = SnailfishNumber(self.value // 2 + self.value % 2)
                self.right.parent = self
                self.value = 0
                return True
            return False
        return self.left.split() or self.right.split()  # Won't call right if left is True

    def __int__(self):
        if self.is_leaf:
            return self.value
        return 3 * int(self.left) + 2 * int(self.right)

    def copy(self):
        if self.is_leaf:
            return SnailfishNumber(self.value)
        return SnailfishNumber(self.value, self.left.copy(), self.right.copy())

    def __add__(self, other):
        res = SnailfishNumber(0, left=self.copy(), right=other.copy())
        reduced = False
        # print(f'Original: {res}')
        while not reduced:
            while res.explode():
                # print(f'Exploded: {res}')
                pass
            reduced = not res.split()
            # if not reduced:
            #     print(f'Split: {res}')
        # print(f'Final: {res}')
        return res

    def __repr__(self):
        if self.is_leaf:
            return str(self.value)
        return f'[{self.left},{self.right}]'


class Day(DayBase):
    @property
    def num(self) -> int:
        return 18

    def get_data(self, example=False):
        return [parse_snailfish(s) for s in super().get_data(example)]

    def puzzle1(self):
        nums = self.get_data(True)
        total = sum(nums[1:], start=nums[0])
        print(total)
        print(int(total))

    def puzzle2(self, num=None):
        nums = self.get_data()
        highest = 0
        for i, n1 in enumerate(nums):
            for j, n2 in enumerate(nums):
                if i != j:
                    highest = max(highest, int(n1 + n2))
        print(highest)
