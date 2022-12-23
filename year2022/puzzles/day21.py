from year2022.day2022 import Day2022
from typing import *
import networkx as nx
import matplotlib.pyplot as plt


def do_job(m1: int, op: str, m2: int):
    if op == '+':
        return m1 + m2
    if op == '-':
        return m1 - m2
    if op == '*':
        return m1 * m2
    if op == '/':
        return m1 // m2
    assert False


def do_rev_job(op: str, operand: int, goal: int, operand_left: bool):
    if op == '+':
        return goal - operand
    if op == '*':
        return goal // operand
    if op == '-':
        if operand_left:
            return operand - goal
        return goal + operand
    if op == '/':
        if operand_left:
            return operand // goal
        return goal * operand
    assert False


def make_digraph(monkies: Dict[str, Union[int, Tuple[str, str, str]]], part1: bool = True):
    graph = nx.DiGraph()
    graph.add_nodes_from(monkies)
    before_root = None
    for monkey, job in monkies.items():
        if isinstance(job, int):
            continue
        graph.add_edge(job[0], monkey)
        graph.add_edge(job[2], monkey)
        if monkey == 'root':
            before_root = job[0], job[2]
    if not part1:
        path = nx.shortest_path(graph, 'humn', 'root')
        for i, n in enumerate(path[:-1]):
            graph.remove_edge(n, path[i + 1])
            graph.add_edge(path[i + 1], n)
        # one_then_two = graph.has_edge(before_root[0], 'root')
        # graph.remove_node('root')
        # graph.add_edge(*before_root[::1 if one_then_two else -1])
    return graph


class Day(Day2022):
    @property
    def num(self) -> int:
        return 21

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = {}
        for line in lines:
            name, job = tuple(line.split(': '))
            if ' ' in job:
                data[name] = tuple(job.split(' '))
            else:
                data[name] = int(job)
        return data

    def puzzle1(self):
        monkies = self.get_data()
        solved = {m for m, j in monkies.items() if isinstance(j, int)}
        while 'root' not in solved:
            for monkey, job in monkies.items():
                if monkey in solved:
                    continue
                if job[0] in solved and job[2] in solved:
                    solved.add(monkey)
                    monkies[monkey] = do_job(monkies[job[0]], job[1], monkies[job[2]])
        print(monkies['root'])

    def puzzle2(self):
        monkies = self.get_data()
        values = {m: j for m, j in monkies.items() if isinstance(j, int) and m != 'humn'}
        change = True
        while change:
            change = False
            for monkey in monkies:
                if monkey in values or monkey == 'humn':
                    continue
                m1, op, m2 = monkies[monkey]
                if m1 in values and m2 in values:
                    change = True
                    values[monkey] = do_job(values[m1], op, values[m2])

        root_left, _, root_right = monkies['root']
        assert (root_left in values) ^ (root_right in values)
        og_left = root_left in values
        if og_left:
            values['root'] = values[root_right] = values[root_left]
        else:
            values['root'] = values[root_left] = values[root_right]

        nxt_monkey = root_right if og_left else root_left
        while 'humn' not in values:
            m1, op, m2 = monkies[nxt_monkey]
            if m1 in values:
                values[m2] = do_rev_job(op, values[m1], values[nxt_monkey], True)
                nxt_monkey = m2
            else:
                values[m1] = do_rev_job(op, values[m2], values[nxt_monkey], False)
                nxt_monkey = m1
        print(values['humn'])
