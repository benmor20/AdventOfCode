from typing import *


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class LinkedList:
    def __init__(self, vals=None):
        if vals is None:
            self.head = self.tail = None
        else:
            itr = iter(vals)
            self.head = self.tail = Node(next(itr))
            for v in itr:
                self.pushright(v)

    def popleft(self):
        n, self.head = self.head, self.head.right
        self.head.left = None
        return n.value

    def popright(self):
        n, self.tail = self.tail, self.tail.left
        self.tail.right = None
        return n.value

    def pushleft(self, val):
        if self.head is None:
            self.head = self.tail = Node(val)
            return
        n = Node(val, right=self.head)
        self.head.left = n
        self.head = n

    def pushright(self, val):
        if self.tail is None:
            self.head = self.tail = Node(val)
            return
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

    @staticmethod
    def _get_item_from(start, offset):
        n = start
        for i in range(abs(offset)):
            t = n.left if offset < 0 else n.right
            # print(f'at {i}, {n if n is None else n.value}, {t if t is None else t.value}')
            n = t
            if n is None:
                return None
        return n

    def _go_to_item(self, item):
        if item >= 0:
            return LinkedList._get_item_from(self.head, item)
        else:
            return LinkedList._get_item_from(self.tail, item + 1)

    def __getitem__(self, item):
        if isinstance(item, int):
            n = self._go_to_item(item)
            if n is None:
                raise IndexError(f'Index {item} out of bounds')
            return n.value
        elif isinstance(item, slice):
            start = item.start if item.start else 0
            stop = item.stop if item.stop else len(self)
            step = item.step if item.step else 1
            if start < 0:
                start = len(self) + start
            if stop < 0:
                stop = len(self) + stop
            res = LinkedList()
            n = self._go_to_item(start)
            res.pushright(n.value)
            for _ in range(start + step, stop, step):
                n = LinkedList._get_item_from(n, step)
                res.pushright(n.value)
            return res

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


class TriLinkedList(LinkedList):
    def __init__(self, vals: Optional[Iterable[Any]] = None,
                 key_nodes: Optional[Union[Node, Tuple[Node, ...]]] = None):
        if vals is None and key_nodes is None:
            super().__init__()
            self.mid = None
            self.offset = 0
        elif vals is None:
            super().__init__()
            if isinstance(key_nodes, Node) or len(key_nodes) == 1:
                self.head = key_nodes if isinstance(key_nodes, Node) else key_nodes[0]
                self.tail = self.mid = self.head
                cnt = 0
                while self.tail.right:
                    self.tail = self.tail.right
                    if cnt % 2 == 0:
                        self.mid = self.mid.right
                    cnt += 1
            elif len(key_nodes) == 2:
                self.head, self.tail = key_nodes[0]
                self.mid = self.head
                temp = self.head
                cnt = 0
                while temp != self.tail:
                    temp = self.head.right
                    if cnt % 2 == 0:
                        self.mid = self.mid.right
            elif len(key_nodes) == 3:
                self.head, self.tail, self.mid = key_nodes
        else:
            itr = iter(vals)
            self.head = self.tail = self.mid = Node(next(itr))
            self.offset = 0
            for v in itr:
                self.pushright(v)

    def popleft(self):
        res = super().popleft()
        self.offset -= 1
        if self.offset == -1:
            self.mid = self.mid.right
            self.offset = 1
        return res

    def popright(self):
        res = super().popright()
        self.offset += 1
        if self.offset == 2:
            self.mid = self.mid.left
            self.offset = 0
        return res

    def popmid(self):
        n = None
        if self.offset == 1:
            n, self.mid = self.mid, self.mid.left
            self.mid.right = n.right
            self.mid.right.left = self.mid
        else:
            n, self.mid = self.mid, self.mid.right
            self.mid.left = n.left
            self.mid.left.right = self.mid
        self.offset = 1 - self.offset
        return n.value

    def popleftmid(self):
        pass

    def poprightmid(self, val):
        pass

    def pushleft(self, val):
        super().pushleft(val)
        self.offset += 1
        if self.offset == 2:
            self.mid = self.mid.left
            self.offset = 0

    def pushright(self, val):
        super().pushright(val)
        self.offset -= 1
        if self.offset == -1:
            self.mid = self.mid.right
            self.offset = 1

    def pushmid(self, val):
        n = Node(val)
        if self.offset == 0:
            n.left, n.right = self.mid, self.mid.right
        else:
            n.left, n.right = self.mid.left, self.mid
        n.left.right = n
        n.right.left = n
        self.mid = n
        self.offset = 1 - self.offset

    def pushleftmid(self, val):
        pass

    def pushrightmid(self, val):
        pass


class BinaryTree:
    def __init__(self, root):
        self.root = root


def add_tuples(tuples):
    return tuple(sum(t[i] for t in tuples) for i in range(len(tuples)))


def signum(v):
    return 0 if v == 0 else abs(v) / v
