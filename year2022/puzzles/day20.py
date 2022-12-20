from year2022.day2022 import Day2022


class Node:
    def __init__(self, value: int, left: 'Node', right: 'Node', uid: int, nvals: int):
        self.value = value
        self.left = left
        self.right = right
        self.uid = uid
        self.nvals = nvals

    def move_pos(self, new_right: 'Node'):
        self.right.left = self.left
        self.left.right = self.right
        new_right.left.right = self
        self.left = new_right.left
        new_right.left = self
        self.right = new_right

    def move(self):
        if self.value == 0:
            return
        val = abs(self.value)
        if self.value > 0:
            new_right = self.right
            for _ in range(val % (self.nvals - 1)):
                new_right = new_right.right
                if new_right.uid == self.uid:
                    new_right = new_right.right
            self.move_pos(new_right)
        else:
            new_right = self
            for _ in range(val % (self.nvals - 1)):
                new_right = new_right.left
                if new_right.uid == self.uid:
                    new_right = new_right.left
            self.move_pos(new_right)


def construct_circle(data) -> Node:
    first_node = Node(data[0], None, None, 0, len(data))
    node = first_node
    for i, val in enumerate(data):
        if i == 0:
            continue
        new_node = Node(val, None, None, i, len(data))
        new_node.left = node
        node.right = new_node
        node = new_node
    first_node.left = node
    node.right = first_node

    node = first_node
    for val in data:
        assert node.value == val
        assert node.left is not None
        assert node.right is not None
        node = node.right
    assert node.value == data[0]

    node = first_node.left
    for val in data[::-1]:
        assert node.value == val
        assert node.left is not None
        assert node.right is not None
        node = node.left
    assert node.value == data[-1]

    return first_node


def find_node(start: Node, uid: int) -> Node:
    node = start
    while node.uid != uid:
        node = node.right
    return node


def find_number(start: Node, num: int) -> Node:
    node = start
    while node.value != num:
        node = node.right
    return node


def get_coords(circle: Node) -> int:
    node = find_number(circle, 0)
    total = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.right
        # print(node.value)
        total += node.value
    return total


class Day(Day2022):
    @property
    def num(self) -> int:
        return 20

    def get_data(self, example=False):
        return [int(i) for i in super().get_data(example)]

    def puzzle1(self):
        return
        data = self.get_data()
        circle = construct_circle(data)
        for uid in range(len(data)):
            find_node(circle, uid).move()
        print(get_coords(circle))

    def puzzle2(self):
        data = self.get_data()
        decrypt_key = 811589153
        data = [i * decrypt_key for i in data]

        circle = construct_circle(data)
        for _ in range(10):
            for uid in range(len(data)):
                find_node(circle, uid).move()
        print(get_coords(circle))
