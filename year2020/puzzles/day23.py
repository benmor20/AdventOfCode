from year2020.day2020 import Day2020
from utils.data_structures import Node, LinkedList


def print_circle(lnk_lst):
    current = lnk_lst.head
    start_val = current.value
    first = True
    s = '['
    while first or current.value != start_val:
        first = False
        s += str(current.value) + ','
        current = current.right
    print(f'{s[:-1]}]')


class Day(Day2020):
    @property
    def num(self) -> int:
        return 23

    def get_data(self, example=False):
        cup_str = '389125467' if example else '476138259'
        return [int(i) for i in cup_str]

    def puzzles(self):
        cups = LinkedList(self.get_data())
        cups_by_num = {}
        current = cups.head
        while current is not None:
            cups_by_num[current.value] = current
            current = current.right
        ncups = 1000000
        for c in range(10, ncups+1):
            cups.pushright(c)
            cups_by_num[c] = cups.tail

        current = cups.head
        cups.tail.right = cups.head
        cups.head.left = cups.tail
        n = ncups * 10
        perc = 100
        for i in range(n):
            if i % (n // perc) == 0:
                print(f'{i // (n // perc)}%')
            first_up = current.right
            all_up = LinkedList()
            all_up.head = first_up
            all_up.tail = first_up.right.right
            current.right = current.right.right.right.right
            current.right.right.right.right.left = current
            all_up.head.left = None
            all_up.tail.right = None
            target = current.value - 1 if current.value > 1 else ncups
            while target in all_up:
                target -= 1
                if target == 0:
                    target = ncups

            target_node = cups_by_num[target]
            target_node.right.left = all_up.tail
            all_up.tail.right = target_node.right
            target_node.right = all_up.head
            all_up.head.left = target_node

            current = current.right

        while True:
            if current.value == 1:
                prod = current.right.value * current.right.right.value
                print(f'{current.right.value}*{current.right.right.value} is {prod}')
                return
            current = current.right
